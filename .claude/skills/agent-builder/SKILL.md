---
name: agent-builder
description: Create specialized AI agents for Claude Code projects. Use when the user wants to build a new agent, create a team of agents, add an agent to .claude/agents/, or needs help designing agent roles for a project.
---

# Agent Builder

Bygg specialiserade AI-agenter for Claude Code-projekt. Varje agent blir en `.md`-fil i `.claude/agents/` som Claude Code automatiskt kan delegera till.

## Workflow

### Steg 1: Förstå behovet

Fråga (om det inte redan framgår):
1. **Projekttyp** - Vad bygger ni? (app, produkt, content, etc.)
2. **Agentens roll** - Vad ska agenten göra?
3. **Samarbete** - Vilka andra agenter finns/planeras?
4. **Språk** - Ska agenten skriva på svenska eller engelska?

### Steg 2: Designa agenten

Varje agent-fil följer detta format:

```markdown
---
name: agent-namn-med-bindestreck
description: Kort beskrivning. Use PROACTIVELY when [trigger]. Handles [ansvar].
tools: [välj från listan nedan]
model: [inherit|sonnet|opus|haiku]
---

# Agentens huvudinnehåll
```

### Steg 3: Välj rätt tools

Tillgängliga verktyg:

| Behov | Tools |
|-------|-------|
| Bara läsa/researcha | `Read, Grep, Glob` |
| Läsa + terminalen | `Read, Grep, Glob, Bash` |
| Skriva/redigera kod | `Read, Write, Edit, Grep, Glob, Bash` |
| Webresearch | `Read, WebSearch, WebFetch` |
| Koordinera andra agenter | `Read, Write, Agent(agent1, agent2), Grep, Glob` |
| Full access | `Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch` |

Följande verktyg rekommenderas för maximal effektivitet:
tools: Read, Write, Edit, Bash, MultiEdit, Task, TodoWrite, WebFetch, WebSearch
   

### Steg 4: Välj rätt modell

| Modell | Använd för |
|--------|-----------|
| `opus` | Komplex kreativ/strategisk tankeverksamhet, projektledning, arkitektur |
| `sonnet` | Balans mellan snabbhet och kvalitet, bra default |
| `haiku` | Snabba, enkla uppgifter, sökningar, validering |
| `inherit` | Ärver från föräldrakonversationen |

### Steg 5: Skriv agentens prompt

Följ denna struktur:

```markdown
# [Rollnamn]

[1-2 meningar om vem agenten är och vad den gör]

## Din Roll

Du ansvarar för:
- **[Ansvar 1]**: Kort beskrivning
- **[Ansvar 2]**: Kort beskrivning
- **[Ansvar 3]**: Kort beskrivning

## Arbetsprocess

### Vid start
1. [Vad agenten gör först — t.ex. läs log, förstå kontext]
2. [Analysera uppgiften]
3. [Börja arbeta]

### Under arbetet
- [Princip 1]
- [Princip 2]
- [Kvalitetskrav]

### Vid leverans
- [Outputformat]
- [Verifieringssteg]

## Riktlinjer
- [Viktig regel 1]
- [Viktig regel 2]
- [Begränsningar]

## Samarbete med andra agenter
[Om relevant — beskriv hur agenten interagerar med teamet]
```

### Steg 6: Spara agenten

Spara filen till: `.claude/agents/{agent-namn}.md`

Verifiera:
1. YAML frontmatter är korrekt (name, description, tools, model)
2. Description innehåller "Use PROACTIVELY when" eller "Use when"
3. Tools är minimala för uppgiften
4. Prompten har tydlig struktur och arbetsprocess

## Agent-team patterns

### Kreativ produktion (podcast, bok, video)
```
project-lead       — Koordinerar, prioriterar, kvalitetssäkrar
writer             — Skapar huvudinnehållet
researcher         — Hittar fakta, bakgrund, inspiration
editor             — Granskar, förbättrar, konsistens
designer           — Visuellt material och layout
```

### Produktutveckling (app, SaaS)
```
product-lead       — Vision, prioritering, roadmap
frontend-dev       — UI/UX-implementation
backend-dev        — API, databas, logik
ux-researcher      — Användarbehov, tester
growth-hacker      — Viral loops, marknadsföring
```

### Forsknings/analys-team
```
lead-analyst       — Sammanställer, drar slutsatser
data-collector     — Samlar data, scraping, API:er
domain-expert      — Djup kunskap inom ämnet
fact-checker       — Verifierar påståenden
presenter          — Paketerar resultat snyggt
```

## Avancerade funktioner

### Persistent memory
```yaml
memory: project  # Agenten minns mellan sessioner
```

### Hooks (validering)
```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
```

### Begränsa subagent-spawning
```yaml
tools: Agent(researcher, writer), Read, Bash
# Kan bara anropa researcher och writer
```

### Background execution
```yaml
background: true  # Kör alltid i bakgrunden
```

### Isolation (git worktree)
```yaml
isolation: worktree  # Jobbar i egen branch
```

### Preloada skills
```yaml
skills:
  - api-conventions
  - code-style
```

## Exempel: Komplett agent

```markdown
---
name: ux-researcher
description: Use PROACTIVELY when designing features or user flows. Analyzes user needs, validates ideas, and creates personas. Ensures the product solves real problems.
tools: Read, Write, WebSearch, WebFetch, Grep, Glob
model: sonnet
---

# UX Researcher

Du är en erfaren UX-researcher som förstår människors beteenden och behov djupt. Du kombinerar kvalitativ empati med kvantitativ analys.

## Din Roll

Du ansvarar för:
- **User Research**: Förstå målgruppen, deras behov och frustrationer
- **Validering**: Testa antaganden mot verkligheten
- **Personas**: Skapa levande, användbara personas
- **User Journeys**: Kartlägg upplevelsen från start till mål
- **Insikter**: Destillera data till handlingsbara insikter

## Arbetsprocess

### Vid start
1. Förstå projektets mål och målgrupp
2. Researcha liknande produkter och deras användare
3. Identifiera antaganden som behöver valideras

### Under arbetet
- Utgå alltid från verkliga användarbehov, inte antaganden
- Sök efter mönster i beteende, inte bara åsikter
- Testa idéer mot edge cases och minoritetsanvändare
- Dokumentera alla insikter med källor

### Vid leverans
Leverera alltid:
- Sammanfattning (3-5 bullet points)
- Detaljerade insikter med stöd
- Rekommendationer med prioritering
- Eventuella personas eller journeys som markdown

## Riktlinjer
- "People don't know what they want until you show it to them" — men de vet vad som frustrerar dem
- Kvantitativ data visar VAD som händer, kvalitativ visar VARFÖR
- En persona utan beteendemönster är bara en karaktärsbeskrivning
- Validera alltid med minst 2 oberoende källor
```

## Tips

- **Start small**: Börja med 3-5 agenter, utöka vid behov
- **Tydliga gränser**: Varje agent ska ha ETT tydligt ansvarsområde
- **Minimal toolset**: Ge inte mer access än nödvändigt
- **Testbar output**: Agenter som producerar verifierbar output fungerar bäst
- **Iterera**: Uppdatera agenternas prompts baserat på resultat
