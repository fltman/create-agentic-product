---
name: gemini-imagegen
description: Generate AI images using Google Gemini via OpenRouter. Use when the user wants to create images, generate pictures, make AI art, edit images, or transform photos. Supports both text-to-image and image-to-image generation.
---

# Gemini Image Generation

Generate high-quality AI images using Google's Gemini model via OpenRouter API.

## Capabilities

- **Text-to-image**: Create images from text descriptions
- **Image-to-image**: Transform existing images based on prompts (style transfer, editing, variations)

## Requirements

Before using this skill, ensure:

1. **Python packages** are installed:
   ```bash
   pip install openai python-dotenv
   ```

2. **API key** is set:
   ```bash
   export OPENROUTER_API_KEY="your-openrouter-api-key"
   ```
   
   Get your key at: https://openrouter.ai/keys

## Usage

### Text-to-Image

Generate an image from a text description:

```bash
python scripts/generate_image.py --prompt "A serene Japanese garden with cherry blossoms" --output garden.png
```

### Image-to-Image

Transform an existing image:

```bash
python scripts/generate_image.py --input photo.jpg --prompt "Transform into a watercolor painting style" --output watercolor.png
```

## Script Arguments

| Argument | Short | Required | Description |
|----------|-------|----------|-------------|
| `--prompt` | `-p` | Yes | Text description of the desired image |
| `--output` | `-o` | No | Output file path (default: `generated_image.png`) |
| `--input` | `-i` | No | Input image for image-to-image mode |
| `--model` | `-m` | No | Model ID (default: `google/gemini-3-pro-image-preview`) |

## Prompt Tips

For best results:

1. **Be specific**: Include details about style, lighting, composition, and mood
2. **Reference art styles**: "in the style of impressionism", "photorealistic", "anime style"
3. **Describe lighting**: "soft morning light", "dramatic shadows", "golden hour"
4. **Include atmosphere**: "mysterious", "cheerful", "melancholic"

### Example Prompts

**Portrait:**
```
A portrait of an elderly fisherman with weathered skin and kind eyes, 
wearing a knit cap, soft natural lighting, shallow depth of field, 
photorealistic style
```

**Landscape:**
```
A misty mountain valley at dawn, pine forests in the foreground, 
snow-capped peaks in the distance, rays of sunlight breaking through 
clouds, epic cinematic composition
```

**Abstract:**
```
Abstract fluid art with deep ocean blues and metallic gold, 
swirling patterns resembling galaxies, high contrast, 
luxurious and elegant mood
```

## Workflow

1. Understand what the user wants to create
2. Craft a detailed, descriptive prompt
3. Run the generation script
4. If the user provides an image, use image-to-image mode
5. Present the generated image to the user
6. Offer to iterate or adjust based on feedback

## Troubleshooting

**"OPENROUTER_API_KEY not set"**
- Set the environment variable: `export OPENROUTER_API_KEY="your-key"`

**"openai package not installed"**
- Install it: `pip install openai`

**"No images found in response"**
- The model may have returned text instead of an image
- Try rephrasing the prompt to be more visual/descriptive
- Check if your API key has credits available

## Output

The script will:
1. Print progress messages
2. Save the image to the specified output path
3. Print "SUCCESS" with the file path on success
4. Return exit code 0 on success, 1 on failure
