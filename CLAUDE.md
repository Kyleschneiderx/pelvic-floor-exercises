# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture

This is a **static HTML site** with no build tools, no frameworks, and no package.json. Every page is a standalone `index.html` file in its own directory for clean URLs (e.g., `/wellness-bundle/index.html` serves at `/wellness-bundle/`).

- **26 HTML pages** — each self-contained with inline CSS and JS
- **No build step** — edit HTML files directly
- **Deployment** — push to `main` on GitHub triggers Vercel auto-deploy (zero config)
- **Repository** — `github.com/Kyleschneiderx/pelvic-floor-exercises`

## Site Structure

- `index.html` — Homepage content hub linking to all video pages
- `starter-course/` — Sales page for the $39 starter course
- `wellness-bundle/` — Sales page for the Pelvic Wellness + Sexual Health bundle
- `video-funnel/`, `youtube-funnel/` — Email funnel landing pages
- **21 video page directories** (e.g., `pelvic-floor-exercises-for-women/`, `pelvic-floor-exercises-pregnancy/`) — SEO-optimized pages each embedding a YouTube video with tracking
- `scripts/create-nurture-flow.py` — Python script that creates a 21-email Klaviyo nurture campaign via API

## Design System ("Refined Aqua")

All pages share the same CSS custom properties defined inline in each file:

```css
--aqua: #5AADB5;        /* Primary */
--aqua-dark: #3D8E96;   /* Hover state */
--periwinkle: #7BA4D4;  /* Accent */
--sage: #8A9E83;        /* Secondary */
--cream: #F6F9FA;       /* Light background */
--charcoal: #1E2D33;    /* Dark sections / text */
--slate: #4A5C65;       /* Body text */
--blush: #E4C8D0;       /* Feminine accent */
--rose: #C4899A;        /* Warm accent */
--gold: #C9A96E;        /* Highlight */
--gradient: linear-gradient(135deg, #5AADB5 0%, #7BA4D4 100%);
```

**Fonts:** Cormorant Garamond (headings) + Karla (body) via Google Fonts.

**Dark sections** use `--charcoal` (#1E2D33) background. Video pages use dark theme: background `#1A2830`, cards `#243640`, borders `#3A4F5A`.

## Page Template Pattern

Every page follows this structure:
1. SEO meta tags (title, description, canonical, Open Graph, Twitter Card)
2. JSON-LD structured data (VideoObject, Article, FAQPage, or Product schema)
3. Google Fonts preconnect + stylesheet link
4. Klaviyo snippet (`company_id=VfvegM`)
5. GTM script (`GTM-MFF4BKKX`)
6. Inline `<style>` block with full CSS (including responsive breakpoints at 1024px, 768px, 380px)
7. Body sections with `.reveal` class for scroll animations
8. GTM noscript iframe
9. Inline `<script>` with IntersectionObserver for scroll reveal + Klaviyo/GTM event tracking

## Third-Party Integrations

| Service | Purpose | Identifier |
|---------|---------|------------|
| **Vercel** | Static hosting | Project in `.vercel/project.json` |
| **Klaviyo** | Email marketing & tracking | `company_id=VfvegM` |
| **GTM** | Analytics | `GTM-MFF4BKKX` |
| **Thinkific** | Course checkout | Enrollment links (`sheree-s-site-bb02.thinkific.com`) |
| **YouTube** | Video hosting | IFrame API embeds |

## Key Conventions

- **No external CSS/JS files** — everything is inline per page for zero-dependency loading
- **All CTAs** use `data-cta-location` attributes for click tracking via GTM and Klaviyo
- **Klaviyo email identification** uses `?email=` URL parameter parsed by JS on each page
- **Images** reference `../ShereeProfilePic.jpg` from subdirectories or YouTube thumbnail URLs
- **Responsive design** uses CSS Grid (3-col → 2-col → 1-col) and Flexbox with mobile breakpoints
- **Scroll reveal** uses IntersectionObserver with `.reveal` / `.visible` classes and cubic-bezier transitions

## Deployment

```bash
git add <files> && git commit -m "message" && git push
```

Vercel automatically deploys on push to `main`. No build command needed.

---

## Workflow Orchestration

### 1. Plan Node Default
- Enter plan mode for ANY non-trivial task (3+ steps or architectural decisions)
- If something goes sideways, STOP and re-plan immediately – don't keep pushing
- Use plan mode for verification steps, not just building
- Write detailed specs upfront to reduce ambiguity

### 2. Subagent Strategy
- Use subagents liberally to keep main context window clean
- Offload research, exploration, and parallel analysis to subagents
- For complex problems, throw more compute at it via subagents
- One task per subagent for focused execution

### 3. Self-Improvement Loop
- After ANY correction from the user: update `tasks/lessons.md` with the pattern
- Write rules for yourself that prevent the same mistake
- Ruthlessly iterate on these lessons until mistake rate drops
- Review lessons at session start for relevant project

### 4. Verification Before Done
- Never mark a task complete without proving it works
- Diff behavior between main and your changes when relevant
- Ask yourself: "Would a staff engineer approve this?"
- Run tests, check logs, demonstrate correctness

### 5. Demand Elegance (Balanced)
- For non-trivial changes: pause and ask "is there a more elegant way?"
- If a fix feels hacky: "Knowing everything I know now, implement the elegant solution"
- Skip this for simple, obvious fixes – don't over-engineer
- Challenge your own work before presenting it

### 6. Autonomous Bug Fixing
- When given a bug report: just fix it. Don't ask for hand-holding
- Point at logs, errors, failing tests – then resolve them
- Zero context switching required from the user
- Go fix failing CI tests without being told how

---

## Task Management

1. **Plan First**: Write plan to `tasks/todo.md` with checkable items
2. **Verify Plan**: Check in before starting implementation
3. **Track Progress**: Mark items complete as you go
4. **Explain Changes**: High-level summary at each step
5. **Document Results**: Add review section to `tasks/todo.md`
6. **Capture Lessons**: Update `tasks/lessons.md` after corrections

---

## Core Principles

- **Simplicity First**: Make every change as simple as possible. Impact minimal code.
- **No Laziness**: Find root causes. No temporary fixes. Senior developer standards.
- **Minimal Impact**: Changes should only touch what's necessary. Avoid introducing bugs.
