#!/usr/bin/env python3
"""
Generate videos using OpenAI's Sora API.
Supports text-to-video and image-to-video generation.
"""

import argparse
import os
import sys
import time

try:
    from openai import OpenAI
except ImportError:
    print("ERROR: openai package not installed. Run: pip install openai")
    sys.exit(1)


VALID_MODELS = ["sora-2", "sora-2-pro"]
VALID_SECONDS = ["4", "8", "12"]
VALID_SIZES = ["1280x720", "720x1280", "1792x1024", "1024x1792"]
PRO_ONLY_SIZES = ["1792x1024", "1024x1792"]


def get_client():
    """Initialize OpenAI client."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY environment variable not set.")
        print("Set it with: export OPENAI_API_KEY='your-key-here'")
        print("Get your key at: https://platform.openai.com/api-keys")
        sys.exit(1)
    return OpenAI(api_key=api_key)


def validate_params(model, seconds, size):
    """Validate generation parameters."""
    if model not in VALID_MODELS:
        print(f"ERROR: Invalid model '{model}'. Valid: {', '.join(VALID_MODELS)}")
        return False

    if seconds not in VALID_SECONDS:
        print(f"ERROR: Invalid seconds '{seconds}'. Valid: {', '.join(VALID_SECONDS)}")
        return False

    if size not in VALID_SIZES:
        print(f"ERROR: Invalid size '{size}'. Valid: {', '.join(VALID_SIZES)}")
        return False

    if size in PRO_ONLY_SIZES and model != "sora-2-pro":
        print(f"ERROR: Size '{size}' requires model 'sora-2-pro'.")
        return False

    return True


def generate_video(prompt, output_path, model="sora-2", seconds="8",
                   size="1280x720", input_image=None, timeout=600):
    """Generate a video using the Sora API."""
    client = get_client()

    # Build creation kwargs
    create_kwargs = {
        "model": model,
        "prompt": prompt,
        "seconds": seconds,
        "size": size,
    }

    img_file = None
    if input_image:
        if not os.path.exists(input_image):
            print(f"ERROR: Input image not found: {input_image}")
            return False
        print(f"Using reference image: {input_image}")
        img_file = open(input_image, "rb")
        create_kwargs["input_reference"] = img_file

    try:
        # Step 1: Create the generation job
        print(f"Creating video generation job...")
        print(f"  Model: {model}")
        print(f"  Duration: {seconds}s")
        print(f"  Size: {size}")
        print(f"  Prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")

        video = client.videos.create(**create_kwargs)
        job_id = video.id
        print(f"Job created: {job_id}")

        # Step 2: Poll for completion
        start_time = time.time()
        poll_interval = 10

        while (time.time() - start_time) < timeout:
            video = client.videos.retrieve(job_id)
            elapsed = int(time.time() - start_time)
            progress = getattr(video, "progress", 0) or 0
            print(f"  [{elapsed}s] Status: {video.status} | Progress: {progress}%")

            if video.status == "completed":
                break
            elif video.status == "failed":
                error_msg = str(video.error) if video.error else "Unknown error"
                print(f"ERROR: Video generation failed: {error_msg}")
                return False

            time.sleep(poll_interval)
        else:
            print(f"ERROR: Video generation timed out after {timeout} seconds.")
            print(f"Job ID {job_id} may still be processing.")
            return False

        # Step 3: Download the video
        print("Downloading video...")
        content = client.videos.download_content(job_id, variant="video")

        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        with open(output_path, "wb") as f:
            f.write(content.content)

        elapsed = int(time.time() - start_time)
        print(f"SUCCESS: Video saved to {output_path} ({elapsed}s total)")
        return True

    finally:
        if img_file:
            img_file.close()


def main():
    parser = argparse.ArgumentParser(
        description="Generate videos using OpenAI Sora",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Text-to-video:
  python generate_video.py --prompt "A sunset over mountains" --output sunset.mp4

  # Image-to-video:
  python generate_video.py --input photo.jpg --prompt "The scene comes alive" --output animated.mp4

  # Pro model, HD, longer:
  python generate_video.py --prompt "Cinematic drone shot" --model sora-2-pro --size 1792x1024 --seconds 12 --output hd.mp4

Environment:
  OPENAI_API_KEY  Your OpenAI API key (required)
        """
    )

    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="Text prompt describing the video to generate"
    )
    parser.add_argument(
        "--output", "-o",
        default="generated_video.mp4",
        help="Output file path (default: generated_video.mp4)"
    )
    parser.add_argument(
        "--input", "-i",
        help="Optional reference image for image-to-video generation"
    )
    parser.add_argument(
        "--model", "-m",
        default="sora-2",
        choices=VALID_MODELS,
        help="Model to use (default: sora-2)"
    )
    parser.add_argument(
        "--seconds", "-s",
        default="8",
        choices=VALID_SECONDS,
        help="Video duration in seconds (default: 8)"
    )
    parser.add_argument(
        "--size",
        default="1280x720",
        choices=VALID_SIZES,
        help="Video resolution WxH (default: 1280x720)"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=600,
        help="Max wait time in seconds (default: 600)"
    )

    args = parser.parse_args()

    if not validate_params(args.model, args.seconds, args.size):
        sys.exit(1)

    success = generate_video(
        prompt=args.prompt,
        output_path=args.output,
        model=args.model,
        seconds=args.seconds,
        size=args.size,
        input_image=args.input,
        timeout=args.timeout,
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
