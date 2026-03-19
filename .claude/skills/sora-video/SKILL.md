---
name: sora-video
description: Generates AI videos from text prompts or reference images using OpenAI Sora. Use when the user wants to create videos, generate video clips, make AI films, animate images, or produce motion content. Supports text-to-video, image-to-video, and video remixing.
---

# Sora Video Generation

Generate high-quality AI videos using OpenAI's Sora model.

## Capabilities

- **Text-to-video**: Create video clips from text descriptions
- **Image-to-video**: Animate a reference image into a video clip
- **Remix**: Create variations of previously generated videos

## Requirements

Before using this skill, ensure:

1. **Python packages** are installed:
   ```bash
   pip install openai
   ```

2. **API key** is set:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   ```

   Get your key at: https://platform.openai.com/api-keys

## Usage

### Text-to-Video

Generate a video from a text description:

```bash
python skills/sora-video/scripts/generate_video.py --prompt "A drone shot flying over a misty forest at sunrise" --output forest.mp4
```

### Image-to-Video

Animate a reference image:

```bash
python skills/sora-video/scripts/generate_video.py --prompt "The scene comes to life with gentle wind" --input photo.jpg --output animated.mp4
```

### Higher Quality (Pro)

Use the pro model for production-grade quality:

```bash
python skills/sora-video/scripts/generate_video.py --prompt "A cinematic sunset over mountains" --model sora-2-pro --size 1792x1024 --seconds 12 --output cinematic.mp4
```

## Script Arguments

| Argument | Short | Required | Default | Description |
|----------|-------|----------|---------|-------------|
| `--prompt` | `-p` | Yes | -- | Text description of the desired video |
| `--output` | `-o` | No | `generated_video.mp4` | Output file path |
| `--input` | `-i` | No | -- | Reference image for image-to-video mode |
| `--model` | `-m` | No | `sora-2` | Model: `sora-2` or `sora-2-pro` |
| `--seconds` | `-s` | No | `8` | Duration: `4`, `8`, or `12` |
| `--size` | | No | `1280x720` | Resolution (see table below) |
| `--timeout` | | No | `600` | Max wait time in seconds |

### Available Sizes

| Size | Orientation | Models |
|------|-------------|--------|
| `1280x720` | Landscape | sora-2, sora-2-pro |
| `720x1280` | Portrait | sora-2, sora-2-pro |
| `1792x1024` | Landscape HD | sora-2-pro only |
| `1024x1792` | Portrait HD | sora-2-pro only |

## Prompt Tips

For best results:

1. **Be cinematic**: Describe camera movement, lighting, and atmosphere
2. **Specify style**: "photorealistic", "anime style", "watercolor animation"
3. **Describe motion**: "slowly panning", "time-lapse", "tracking shot"
4. **Set the mood**: "dramatic lighting", "golden hour", "neon-lit"

### Example Prompts

**Nature:**
```
A drone shot flying over a misty forest at sunrise, golden light filtering through
the trees, birds rising from the canopy, cinematic quality
```

**Urban:**
```
A time-lapse of a busy Tokyo intersection at night, neon signs reflecting on wet
pavement, crowds crossing in all directions, cyberpunk atmosphere
```

**Abstract:**
```
Liquid metal flowing and morphing into geometric shapes, iridescent reflections,
dark background, smooth motion, high-end product visualization style
```

## Pricing

| Model | Resolution | Per Second | 4s Clip | 8s Clip | 12s Clip |
|-------|-----------|------------|---------|---------|----------|
| sora-2 | 720p | $0.10 | $0.40 | $0.80 | $1.20 |
| sora-2-pro | 720p | $0.30 | $1.20 | $2.40 | $3.60 |
| sora-2-pro | 1024p | $0.50 | $2.00 | $4.00 | $6.00 |

Note: You are charged for every generation attempt, including failed ones.

## Workflow

1. Understand what the user wants to create
2. Craft a detailed, cinematic prompt (camera angles, lighting, mood, motion)
3. Choose appropriate model, duration, and resolution
4. Run the generation script
5. If the user provides an image, use image-to-video mode with `--input`
6. Present the generated video to the user
7. Offer to iterate or adjust based on feedback

## Troubleshooting

**"OPENAI_API_KEY not set"**
- Set the environment variable: `export OPENAI_API_KEY="your-key"`

**"openai package not installed"**
- Install it: `pip install openai`

**"Video generation failed: content_policy_violation"**
- The prompt was flagged by content moderation
- Remove references to real people, copyrighted characters, or inappropriate content
- Rephrase the prompt and try again

**"Video generation timed out"**
- Pro model and higher resolutions take longer (up to 5 minutes)
- Increase timeout: `--timeout 900`
- Try with `sora-2` (faster) instead of `sora-2-pro`

**"Rate limit exceeded"**
- Wait a moment and try again
- Standard API tier allows ~10 requests per minute

## Output

The script will:
1. Print progress messages with status and percentage
2. Save the MP4 video to the specified output path
3. Print "SUCCESS" with the file path on success
4. Return exit code 0 on success, 1 on failure
