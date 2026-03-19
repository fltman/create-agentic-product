---
name: elevenlabs-voice-style
description: Create voice style descriptions for ElevenLabs. Use when the user wants to describe a voice, create a voice profile, or generate voice style text. Outputs exactly 300 characters describing voice characteristics.
---

# ElevenLabs Voice Style Creator

Generate 300-character voice style descriptions for ElevenLabs voice cloning and design.

## Output Format

- Exactly 300 characters (including spaces)
- One paragraph, English only
- No line breaks

## What to Include

Describe these voice characteristics:

1. **Tone**: warm, cold, authoritative, friendly, mysterious, energetic
2. **Pitch**: deep, high, mid-range, bass, tenor, soprano
3. **Pace**: slow, fast, measured, dynamic, deliberate
4. **Texture**: smooth, gravelly, breathy, crisp, raspy, silky
5. **Emotion**: calm, excited, serious, playful, intense, soothing
6. **Accent/Style**: neutral American, British RP, conversational, formal, casual
7. **Special qualities**: resonant, nasal, airy, rich, thin, full-bodied

## Examples

**Narrator (audiobook):**
```
Deep, resonant male voice with a warm, rich timbre. Measured pace perfect for storytelling. Slight bass undertones with crystal-clear articulation. Calm and authoritative yet inviting. Neutral American accent with subtle gravitas. Smooth delivery that draws listeners in without overwhelming. Ideal for fiction narration.
```

**Podcast Host:**
```
Bright, energetic female voice with a conversational mid-range tone. Natural pace with dynamic inflections that keep listeners engaged. Warm and approachable with a hint of playfulness. Clear articulation without being overly formal. Light, airy texture with genuine enthusiasm. Perfect for casual discussions and interviews.
```

**Corporate Narrator:**
```
Professional male voice with confident, measured delivery. Mid-range pitch with smooth, polished texture. Authoritative yet approachable tone suitable for business content. Neutral accent with precise articulation. Calm and reassuring without being monotonous. Subtle warmth that builds trust. Ideal for training videos and presentations.
```

**Character Voice (villain):**
```
Low, menacing male voice with a cold, calculated delivery. Slow, deliberate pace that creates tension. Slight rasp adding an edge of danger. Dark undertones with precise, clipped articulation. Controlled intensity that suggests hidden power. British accent with aristocratic quality. Perfect for antagonist roles and dark narratives.
```

**ASMR/Meditation:**
```
Soft, gentle female voice with a breathy, intimate quality. Very slow, soothing pace designed for relaxation. Whisper-like texture with warm undertones. Calming and nurturing without being sleepy. Minimal dynamic range for consistent tranquility. Neutral accent with careful, unhurried articulation. Ideal for guided meditation and sleep content.
```

## Workflow

1. Ask user about the intended use (narration, character, podcast, etc.)
2. Ask about preferred gender, age range, and mood
3. Draft the description
4. Count characters precisely — must be exactly 300
5. Adjust by adding/removing adjectives to hit 300 characters
6. Present the final description
