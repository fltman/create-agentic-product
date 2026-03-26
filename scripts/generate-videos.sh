#!/bin/bash
# Cargo Survey — Generera alla videor med Sora
# Kör detta lokalt på din dator
# Förutsätter att .env finns med OPENAI_API_KEY

set -e
cd "$(dirname "$0")/.."

# Ladda miljövariabler
export $(grep -v '^#' .env | xargs)

SCRIPT=".claude/skills/sora-video/scripts/generate_video.py"
OUTDIR="assets/videos"

echo "=== Cargo Survey — Videogenerering ==="
echo ""

echo "[1/4] Scen 1: Hamnen vid gryning..."
python "$SCRIPT" \
  --prompt "Cinematic slow drone shot of an industrial harbor at dawn. A large oil tanker ship 'Oceanic Endeavor' is docked at the pier. Oil pipelines and pumping equipment stretch across the dock. Warm golden sunrise light reflects off the calm water and metal pipes. Workers in orange high-vis jackets walk along the pier. Industrial, professional, beautiful atmosphere." \
  --output "$OUTDIR/scene1-harbor-dawn.mp4" \
  --seconds 8

echo ""
echo "[2/4] Scen 2: Inspektören arbetar..."
python "$SCRIPT" \
  --prompt "Close-up cinematic shot of a safety inspector in orange high-visibility workwear and white hard hat carefully inspecting oil pipeline connections at a harbor pump station. His hands check pipe fittings with precision. Oil pumps running in background. Golden hour lighting, industrial setting. Professional and meticulous work." \
  --output "$OUTDIR/scene2-inspector-work.mp4" \
  --seconds 8

echo ""
echo "[3/4] Scen 3: Teamet..."
python "$SCRIPT" \
  --prompt "Cinematic tracking shot of three safety inspectors walking together along a harbor pier next to a large oil tanker. They wear orange high-visibility workwear and white hard hats. Professional and focused but with friendly expressions. One holds a clipboard. Industrial harbor with pipelines and cranes in background. Golden hour warm lighting." \
  --output "$OUTDIR/scene3-team-walking.mp4" \
  --seconds 8

echo ""
echo "[4/4] Scen 4: Slutkort..."
python "$SCRIPT" \
  --prompt "Cinematic wide shot slowly pulling back from an industrial harbor at sunset. Oil tanker and pipelines silhouetted against orange sky. The scene gradually darkens as text 'CARGO SURVEY' appears in large industrial metallic font. Professional recruitment advertisement feel." \
  --output "$OUTDIR/scene4-logo-cta.mp4" \
  --seconds 4

echo ""
echo "=== Klart! Alla videor sparade i $OUTDIR ==="
echo ""
echo "Nästa steg: Klipp ihop videorna med musik och voiceover"
