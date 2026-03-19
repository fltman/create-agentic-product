---
name: suno-music
description: Create songs for Suno AI music generation. Use when the user wants to create a song, write lyrics, or make music. Outputs a 300-character style description and tagged lyrics formatted for Suno.
---

# Suno Music Creator

Generate Suno-ready song packages with style description and tagged lyrics.

## Output Format

Always provide exactly two sections:

### 1. Style Description
- Exactly 300 characters (including spaces)
- One paragraph, English only
- Include: genre, subgenre, mood, tempo (BPM or feel), instruments, vocal style
- No line breaks

**Example:**
```
Dreamy indie folk with fingerpicked acoustic guitar and soft piano. Female vocals, breathy and intimate. Slow tempo around 75 BPM. Melancholic yet hopeful atmosphere with subtle string swells. Lo-fi warmth with vinyl crackle undertones. Gentle percussion, brushed drums. Ethereal harmonies in chorus.
```

### 2. Tagged Lyrics

**Structure Tags:**
- `[Intro]` — Instrumental or vocal opening
- `[Verse]` — Story/narrative sections
- `[Pre-Chorus]` — Build-up to chorus
- `[Chorus]` — Main hook, repeat as needed
- `[Bridge]` — Contrast section
- `[Outro]` — Closing section
- `[Instrumental Break]` — No vocals
- `[Drop]` — For electronic/EDM

**Vocal Tags:**
- `[Male Vocal]`, `[Female Vocal]`
- `[Whispered]`, `[Spoken Word]`
- `[Harmony]`, `[Ad-lib]`

**Example:**
```
[Intro]
[Verse]
Walking through the morning light
Coffee steam and city sights
Every stranger has a story untold

[Pre-Chorus]
And I wonder where they go

[Chorus]
We're all just passing through
Chasing something true
In this beautiful mess we call life

[Verse]
Raindrops on the window pane
Washing yesterday's pain
Tomorrow's just a promise away

[Chorus]
We're all just passing through
Chasing something true
In this beautiful mess we call life

[Bridge]
[Female Vocal]
Maybe that's enough
Maybe that's enough

[Outro]
[Instrumental Break]
```

## Workflow

1. Ask user for song topic/mood if not provided
2. Write style description (count characters precisely — must be 300)
3. Write tagged lyrics matching the style
4. Present both sections clearly labeled
