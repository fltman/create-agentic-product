# Creative Product Team

[![Support me on Patreon](https://img.shields.io/badge/Patreon-Support%20my%20work-FF424D?style=flat&logo=patreon&logoColor=white)](https://www.patreon.com/AndersBjarby)

Ett ramverk för Claude Code som snabbt sätter upp ett AI-drivet kreativt team. Teamet hjälper dig ta en produktidé från koncept till lansering med hjälp av specialiserade agenter som samarbetar i faser — research, koncept och design, byggande, samt lansering och tillväxt.

## Vad det innehåller

- **Faståbaserat arbetsflöde** — `CLAUDE.md` beskriver hur Claude Code förstår behovet, sätter ihop rätt team och kör faserna i ordning.
- **Agenter** (`.claude/agents/`) — t.ex. `image-creator`, `elevenlabs-voice` och `suno-songwriter`, plus exempelroller (project-lead, market-researcher, brand-strategist, copywriter m.fl.) som skräddarsys per projekt.
- **Skills** (`.claude/skills/`) för att generera kreativt material:
  - `agent-builder` — skapa nya agenter
  - `gemini-imagegen` — bildgenerering via Google Gemini (text-to-image, image-to-image)
  - `sora-video` — videogenerering via OpenAI Sora (image-to-video)
  - `suno-music-skill` — musikskapande för Suno AI
  - `elevenlabs-skill` — röstdesign för ElevenLabs

## Använda

Öppna projektet i Claude Code. Claude följer `CLAUDE.md`: den ställer frågor om produkt, målgrupp, marknader, ambition, budget och tidplan, föreslår ett team och kör sedan faserna. Allt genererat material sparas i `assets/` (bilder, video, ljud) och all strategi i `docs/`.

Skills som bild-, video- och musikgenerering kräver API-nycklar (OpenRouter, OpenAI, ElevenLabs). Lägg dem i en `.env` i projektroten — den är gitignored och skapas aldrig utan ditt godkännande.

## Teknik

Claude Code-agenter och skills (Markdown + Python-script). Inga fasta teknikval för produkterna som byggs — de väljs per projekt.
