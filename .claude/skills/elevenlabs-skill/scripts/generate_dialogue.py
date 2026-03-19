#!/usr/bin/env python3
"""
Generate dialogue audio using ElevenLabs Text-to-Dialogue API.
Automatically splits long dialogues into chunks and concatenates the results.
"""

import argparse
import json
import os
import sys
import tempfile

try:
    from elevenlabs import ElevenLabs
except ImportError:
    print("ERROR: elevenlabs package not installed. Run: pip install elevenlabs")
    sys.exit(1)

# Try to import pydub for audio concatenation, fall back to ffmpeg if not available
PYDUB_AVAILABLE = False
try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    pass

MAX_CHARS_PER_CHUNK = 2000


def get_client():
    """Get ElevenLabs client."""
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        print("ERROR: ELEVENLABS_API_KEY environment variable not set.")
        print("Set it with: export ELEVENLABS_API_KEY='your-key-here'")
        print("Get your key at: https://elevenlabs.io/api")
        sys.exit(1)
    
    return ElevenLabs(api_key=api_key)


def calculate_chunk_chars(inputs: list) -> int:
    """Calculate total characters in a list of inputs."""
    return sum(len(item["text"]) for item in inputs)


def split_into_chunks(inputs: list, max_chars: int = MAX_CHARS_PER_CHUNK) -> list:
    """
    Split dialogue inputs into chunks of approximately max_chars.
    Never splits in the middle of a single input.
    """
    chunks = []
    current_chunk = []
    current_chars = 0
    
    for item in inputs:
        item_chars = len(item["text"])
        
        # If adding this item would exceed limit and we have items, start new chunk
        if current_chars + item_chars > max_chars and current_chunk:
            chunks.append(current_chunk)
            current_chunk = []
            current_chars = 0
        
        current_chunk.append(item)
        current_chars += item_chars
    
    # Don't forget the last chunk
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks


def generate_dialogue_chunk(client: ElevenLabs, inputs: list) -> bytes:
    """
    Generate dialogue audio for a single chunk.
    Returns the audio bytes on success, None on failure.
    """
    try:
        response = client.text_to_dialogue.convert(inputs=inputs)
        
        # Response is a generator of audio chunks, collect them all
        audio_data = b""
        for chunk in response:
            audio_data += chunk
        
        return audio_data
    except Exception as e:
        print(f"ERROR: API call failed: {e}")
        return None


def concatenate_audio_pydub(audio_files: list, output_path: str) -> bool:
    """Concatenate audio files using pydub."""
    try:
        combined = AudioSegment.empty()
        for audio_file in audio_files:
            segment = AudioSegment.from_mp3(audio_file)
            combined += segment
        
        combined.export(output_path, format="mp3")
        return True
    except Exception as e:
        print(f"ERROR: Failed to concatenate with pydub: {e}")
        return False


def concatenate_audio_ffmpeg(audio_files: list, output_path: str) -> bool:
    """Concatenate audio files using ffmpeg."""
    import subprocess
    
    # Create a temporary file list for ffmpeg
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        for audio_file in audio_files:
            f.write(f"file '{audio_file}'\n")
        list_file = f.name
    
    try:
        cmd = [
            'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
            '-i', list_file, '-c', 'copy', output_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"ERROR: ffmpeg failed: {result.stderr}")
            return False
        return True
    except FileNotFoundError:
        print("ERROR: ffmpeg not found. Install with: apt install ffmpeg / brew install ffmpeg")
        return False
    finally:
        os.unlink(list_file)


def concatenate_audio(audio_files: list, output_path: str) -> bool:
    """Concatenate audio files using best available method."""
    if PYDUB_AVAILABLE:
        return concatenate_audio_pydub(audio_files, output_path)
    else:
        return concatenate_audio_ffmpeg(audio_files, output_path)


def generate_dialogue(inputs: list, output_path: str, max_chars: int = MAX_CHARS_PER_CHUNK) -> bool:
    """
    Generate dialogue audio from a list of voice inputs.
    Automatically chunks long dialogues and concatenates results.
    """
    client = get_client()
    total_chars = calculate_chunk_chars(inputs)
    
    # Check if we need to split
    if total_chars <= max_chars:
        # Single chunk, simple case
        print(f"Generating dialogue ({total_chars} chars, {len(inputs)} lines)...")
        audio_data = generate_dialogue_chunk(client, inputs)
        
        if audio_data:
            output_dir = os.path.dirname(output_path)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
            
            with open(output_path, "wb") as f:
                f.write(audio_data)
            
            print(f"SUCCESS: Audio saved to {output_path}")
            return True
        return False
    
    # Multiple chunks needed
    chunks = split_into_chunks(inputs, max_chars)
    print(f"Dialogue is {total_chars} chars, splitting into {len(chunks)} chunks...")
    
    temp_files = []
    temp_dir = tempfile.mkdtemp()
    
    try:
        for i, chunk in enumerate(chunks):
            chunk_chars = calculate_chunk_chars(chunk)
            print(f"  Generating chunk {i+1}/{len(chunks)} ({chunk_chars} chars, {len(chunk)} lines)...")
            
            audio_data = generate_dialogue_chunk(client, chunk)
            if not audio_data:
                print(f"ERROR: Failed to generate chunk {i+1}")
                return False
            
            temp_file = os.path.join(temp_dir, f"chunk_{i:03d}.mp3")
            with open(temp_file, "wb") as f:
                f.write(audio_data)
            temp_files.append(temp_file)
        
        # Concatenate all chunks
        print(f"Concatenating {len(temp_files)} audio files...")
        
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        if concatenate_audio(temp_files, output_path):
            print(f"SUCCESS: Audio saved to {output_path}")
            return True
        else:
            # Fallback: if concatenation fails, at least save the parts
            print("WARNING: Concatenation failed. Saving individual parts...")
            base, ext = os.path.splitext(output_path)
            for i, temp_file in enumerate(temp_files):
                part_path = f"{base}_part{i+1}{ext}"
                os.rename(temp_file, part_path)
                print(f"  Saved: {part_path}")
            return False
            
    finally:
        # Cleanup temp files
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
        if os.path.exists(temp_dir):
            os.rmdir(temp_dir)


def main():
    parser = argparse.ArgumentParser(
        description="Generate dialogue audio using ElevenLabs API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # From JSON file:
  python generate_dialogue.py --input dialogue.json --output conversation.mp3

  # From inline JSON:
  python generate_dialogue.py --json '[{"text": "Hello!", "voice_id": "abc123"}]' --output hello.mp3

JSON Format:
  [
    {"text": "First line", "voice_id": "voice_id_1"},
    {"text": "Second line", "voice_id": "voice_id_2"}
  ]

Long Dialogues:
  Dialogues over 2000 characters are automatically split into chunks,
  generated separately, and concatenated into a single output file.
  Requires either pydub (pip install pydub) or ffmpeg installed.

Environment:
  ELEVENLABS_API_KEY  Your ElevenLabs API key (required)

Popular Voice IDs:
  Rachel (female):     21m00Tcm4TlvDq8ikWAM
  Domi (female):       AZnzlk1XvdvUeBnXmlld
  Bella (female):      EXAVITQu4vr4xnSDxMaL
  Antoni (male):       ErXwobaYiN019PkySvjV
  Josh (male):         TxGEqnHWrfWFTfGW9XjX
  Arnold (male):       VR6AewLTigWG4xSOukaG
  Adam (male):         pNInz6obpgDQGcFmaJgB
  Sam (male):          yoZ06aMxZJJ28mfd3POQ
        """
    )
    
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "--input", "-i",
        help="Path to JSON file containing dialogue inputs"
    )
    input_group.add_argument(
        "--json", "-j",
        help="Inline JSON array of dialogue inputs"
    )
    
    parser.add_argument(
        "--output", "-o",
        default="dialogue.mp3",
        help="Output file path (default: dialogue.mp3)"
    )
    
    parser.add_argument(
        "--max-chars", "-m",
        type=int,
        default=MAX_CHARS_PER_CHUNK,
        help=f"Max characters per chunk (default: {MAX_CHARS_PER_CHUNK})"
    )
    
    args = parser.parse_args()
    
    # Parse inputs
    if args.input:
        try:
            with open(args.input, "r") as f:
                inputs = json.load(f)
        except FileNotFoundError:
            print(f"ERROR: File not found: {args.input}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"ERROR: Invalid JSON in file: {e}")
            sys.exit(1)
    else:
        try:
            inputs = json.loads(args.json)
        except json.JSONDecodeError as e:
            print(f"ERROR: Invalid JSON: {e}")
            sys.exit(1)
    
    # Validate inputs
    if not isinstance(inputs, list):
        print("ERROR: Inputs must be a JSON array")
        sys.exit(1)
    
    for i, item in enumerate(inputs):
        if not isinstance(item, dict):
            print(f"ERROR: Item {i} must be an object")
            sys.exit(1)
        if "text" not in item:
            print(f"ERROR: Item {i} missing 'text' field")
            sys.exit(1)
        if "voice_id" not in item:
            print(f"ERROR: Item {i} missing 'voice_id' field")
            sys.exit(1)
    
    # Generate dialogue
    success = generate_dialogue(inputs, args.output, args.max_chars)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
