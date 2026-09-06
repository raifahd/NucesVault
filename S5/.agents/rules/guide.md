---
trigger: always_on
---

# Course Notes Manager

## Architecture: Modular One-HTML-File-Per-Module
To prevent massive files (thousands of LOC) and reduce syntax errors, **each lecture / module is stored in its own standalone HTML file**:
```text
Notes/<Course>/
├── 1- Introduction to DW.html        (~1,500 lines)
├── 2- Dimensional Modeling.html      (~1,500 lines)
└── 3- ETL Architecture.html          (~1,500 lines)
```

## When the user shares course content:
1. **Determine the target file**:
   - If content belongs to an existing lecture/module: open `Notes/<Course>/<N>- <Module Name>.html`, append new `.topic-card` sections after existing ones in `#main-content`, and add matching `<li>` to `#nav-list`.
   - If content is a new lecture/module: create a new file `Notes/<Course>/<N>- <Descriptive Lecture Name>.html` using the template below. **Never use `index.html` as the default file name.**
2. **Read the existing file first before making edits.** Never delete or overwrite existing content. Increment IDs (`topic-1`, `topic-2`…).
3. **Cross-Module Navigation in Sidebar**:
   - The current module's topics are listed under an open collapsible `.nav-section` with `.nav-sublist` calling `showTopic('topic-X')`.
   - Other modules in the course are listed as cross-file `.nav-module-link` anchors (e.g. `<a class="nav-module-link" href="./2- Dimensional Modeling.html"><span class="nav-num">02</span>Dimensional Modeling</a>`).
4. If a book/reference/syllabus is provided, cite it at the top of generated sections.
5. **Update Navigation Across All Files**: When adding a new module file, you MUST use a script to automatically parse and append the new module to the `#nav-list` of ALL sibling HTML files in the same course directory. Clean up any corrupted or duplicate navigation entries if found.

## Visuals and Diagrams
- When the user asks for visuals, **NEVER** use image generation tools.
- Instead, build **proper diagrams yourself natively** using HTML/CSS (e.g., flexbox grids, styled divs) or embed Mermaid.js graphs directly into the HTML file.

## Design Philosophy
- **Sleek Dark Zinc** palette — neutral deep darks with vibrant semantic accents.
- **Color has meaning**:
  - `--ac` (terracotta `#d97757`): Primary brand accent for headings, links, summary boxes.
  - `--exp-bd`, `--exp-bg` (vivid blue): Explanations / concepts (`.example`).
  - `--def-bd`, `--def-bg` (vivid emerald): Definitions (`.definition`).
  - `--qst-bd`, `--qst-bg` (vivid violet): Questions / think-about-it (`details`).
  - `--wrn-bd`, `--wrn-bg` (amber): Warnings / important (`.note-box`).
  - `--crit-bd`, `--crit-bg` (red-orange): Critical warnings (`.warning-box`).
- **Full-width screen coverage**: Text and topic cards span the full available width of the screen (`width: 100%`). Do not constrain `.module-container` or `.topic-card` with artificial `max-width`.
- **Generous whitespace**: 36px/40px card padding, 18px callout margins, 1.75 line-height on body text, 96px bottom padding to prevent fixed elements from overlapping content.
- **Subtle interactivity**: cards glow brand color on hover, active sidebar topics highlight in terracotta with indicator bar and solid badge, back-to-top fades in smoothly. Transitions stay ≤0.3s.
- **Typography hierarchy**: Poppins at 600/700 for headings, 400 for body, 300 for muted text.
- **Multi-page architecture**: Topics within a module are loaded dynamically as single views with Next/Previous pagination.

## Writing & Explanation Style
- Write as if you're an expert tutor — **clear, conversational, thorough**. Avoid dry textbook tone.
- Start each topic with a plain-language **"what and why"** overview before diving into formulas or formal definitions.
- Use **real-world analogies** to make abstract concepts click (e.g., "a stack is like a pile of plates").
- Build **progressive depth**: introduce the idea simply → define it formally → show an example → highlight edge cases.
- Bold key terms on first use and wrap them in `.definition` boxes.
- Use `.note-box` for "pro tips" and exam hints. Use `.warning-box` for common student mistakes, misconceptions, or tricky edge cases.

## Each topic section must include:
- `<h2>` topic heading, `<h3>`/`<h4>` subtopics with logical flow
- `.definition` boxes for every key term, formula, or theorem — include the formal statement AND an intuitive one-liner
- `.note-box` (tips, exam hints) and `.warning-box` (common mistakes, misconceptions)
- `.example` blocks with clearly numbered step-by-step solutions using `<pre>`/`<code>` for any code, math, or pseudocode
- `<table>` for comparisons, properties, or listing methods side-by-side
- ≥3 `<details><summary>` practice questions per topic — mix difficulty (easy/medium/hard), include full worked solutions in the hidden answer
- `.summary-box` with 3–5 bullet recap of the most important takeaways

## Template (new files only)

Instead of duplicating the HTML/JS here, use the master template file located at `../../_template.html` (or `Notes/S5/_template.html`). When creating a new module, read that file and use it as the base structure, replacing the placeholder `[Course]` and `[Module Name]` variables.