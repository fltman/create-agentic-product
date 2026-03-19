#!/usr/bin/env python3
"""
Generate images using Google Gemini via OpenRouter API.
Supports both text-to-image and image-to-image generation.
"""

import argparse
import base64
import os
import sys
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print("ERROR: openai package not installed. Run: pip install openai")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional


def get_client():
    """Initialize OpenAI client with OpenRouter configuration."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY environment variable not set.")
        print("Set it with: export OPENROUTER_API_KEY='your-key-here'")
        sys.exit(1)
    
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )


def encode_image(image_path: str) -> str:
    """Encode an image file to base64."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def get_image_mime_type(image_path: str) -> str:
    """Get MIME type based on file extension."""
    ext = Path(image_path).suffix.lower()
    mime_types = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    return mime_types.get(ext, "image/jpeg")


def generate_from_text(prompt: str, output_path: str, model: str = "google/gemini-3-pro-image-preview") -> bool:
    """Generate an image from a text prompt."""
    client = get_client()
    
    print(f"Generating image from prompt: {prompt[:100]}...")
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
    )
    
    return extract_and_save_image(response, output_path)


def generate_from_image(input_image: str, prompt: str, output_path: str, model: str = "google/gemini-3-pro-image-preview") -> bool:
    """Generate an image based on an input image and prompt."""
    client = get_client()
    
    if not os.path.exists(input_image):
        print(f"ERROR: Input image not found: {input_image}")
        return False
    
    print(f"Generating image from: {input_image}")
    print(f"Prompt: {prompt[:100]}...")
    
    base64_image = encode_image(input_image)
    mime_type = get_image_mime_type(input_image)
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Generate an image: {prompt}"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
    )
    
    return extract_and_save_image(response, output_path)


def extract_and_save_image(response, output_path: str) -> bool:
    """Extract image from API response and save to file."""
    if not response.choices or not response.choices[0].message:
        print("ERROR: No response received from API")
        return False
    
    message = response.choices[0].message
    
    # Print any textual content
    if message.content:
        print(f"Model response: {message.content}")
    
    # Check if there are images in the message
    if hasattr(message, 'images') and message.images:
        for image_data in message.images:
            if image_data["type"] == "image_url" and image_data["image_url"]["url"].startswith("data:image"):
                # Extract base64 data from data URL
                data_url = image_data["image_url"]["url"]
                # Format: data:image/png;base64,<base64_data>
                base64_data = data_url.split(',', 1)[1]
                
                # Ensure output directory exists
                output_dir = os.path.dirname(output_path)
                if output_dir:
                    os.makedirs(output_dir, exist_ok=True)
                
                # Decode and save the image
                with open(output_path, "wb") as f:
                    f.write(base64.b64decode(base64_data))
                
                print(f"SUCCESS: Image saved to {output_path}")
                return True
    
    print("ERROR: No images found in response")
    return False


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using Google Gemini via OpenRouter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Text-to-image:
  python generate_image.py --prompt "A sunset over mountains" --output sunset.png

  # Image-to-image:
  python generate_image.py --input photo.jpg --prompt "Make it look like a watercolor painting" --output watercolor.png

Environment:
  OPENROUTER_API_KEY  Your OpenRouter API key (required)
        """
    )
    
    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="Text prompt describing the image to generate"
    )
    parser.add_argument(
        "--output", "-o",
        default="generated_image.png",
        help="Output file path (default: generated_image.png)"
    )
    parser.add_argument(
        "--input", "-i",
        help="Optional input image for image-to-image generation"
    )
    parser.add_argument(
        "--model", "-m",
        default="google/gemini-3-pro-image-preview",
        help="Model to use (default: google/gemini-3-pro-image-preview)"
    )
    
    args = parser.parse_args()
    
    if args.input:
        success = generate_from_image(args.input, args.prompt, args.output, args.model)
    else:
        success = generate_from_text(args.prompt, args.output, args.model)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
