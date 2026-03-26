#!/bin/bash
# Cargo Survey — Generera voiceover med ElevenLabs
# Kör detta lokalt på din dator
# Förutsätter att .env finns med ELEVENLABS_API_KEY
#
# Behöver: pip install elevenlabs pydub
# Samt ffmpeg installerat (apt install ffmpeg / brew install ffmpeg)

set -e
cd "$(dirname "$0")/.."

# Ladda miljövariabler
export $(grep -v '^#' .env | xargs)

SCRIPT=".claude/skills/elevenlabs-skill/scripts/generate_dialogue.py"
OUTDIR="assets/audio"

echo "=== Cargo Survey — Voiceover-generering ==="
echo ""
echo "Röst: Josh (djup bas, action-trailer stil)"
echo "Text: Svenskt voiceover-manus"
echo ""

# Kontrollera att ELEVENLABS_API_KEY finns
if [ -z "$ELEVENLABS_API_KEY" ]; then
    echo "FEL: ELEVENLABS_API_KEY saknas i .env"
    echo ""
    echo "Lägg till den i .env-filen:"
    echo "  ELEVENLABS_API_KEY=din-nyckel-här"
    echo ""
    echo "Skaffa nyckel på: https://elevenlabs.io/api"
    exit 1
fi

echo "Genererar voiceover..."
python "$SCRIPT" \
  --input "$OUTDIR/cargo-survey-dialogue.json" \
  --output "$OUTDIR/cargo-survey-voiceover.mp3"

echo ""
echo "=== Klart! ==="
echo "Voiceover sparad: $OUTDIR/cargo-survey-voiceover.mp3"
echo ""
echo "Nästa steg: Klipp ihop video + musik + voiceover i valfritt videoredigeringsprogram"
echo ""
echo "Tidslinje för klippning:"
echo "  0-5s   : scene1-harbor-dawn.mp4    + Voiceover: 'Varje dag. Varje last. Varje kontroll.'"
echo "  5-15s  : scene2-inspector-work.mp4  + Voiceover: 'Vi är Cargo Survey. Vi ser till att allt fungerar...'"
echo "  15-22s : scene3-team-walking.mp4    + Voiceover: 'Nu söker vi fler till vårt team. Omedelbar tillträde.'"
echo "  22-28s : scene4-logo-cta.mp4        + Voiceover: 'Cargo Survey. Ansök idag.'"
echo ""
echo "Musik: Lägg Suno-låten som bakgrundsmusik genom hela filmen"
echo "       Sänk musikvolymen under voiceover-partierna"
