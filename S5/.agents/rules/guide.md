---
trigger: always_on
---

# Course Notes Manager

## When the user shares course content:
1. Find/create `Notes/<Course>/index.html`. Use the template below for new files.
2. **Read the existing file first.** Append new `.topic-card` sections after existing ones in `#main-content`. Add matching `<li>` to `#nav-list`. Increment IDs (`topic-1`, `topic-2`…). Never delete existing content.
3. If a book/reference is provided, cite it at the top of generated sections.

## Design Philosophy
- **Sleek Dark Zinc** palette — neutral deep darks with vibrant semantic accents.
- **Color has meaning**:
  - `--ac` (terracotta `#d97757`): Primary brand accent for headings, links, summary boxes.
  - `--exp-bd`, `--exp-bg` (vivid blue): Explanations / concepts (`.example`).
  - `--def-bd`, `--def-bg` (vivid emerald): Definitions (`.definition`).
  - `--qst-bd`, `--qst-bg` (vivid violet): Questions / think-about-it (`details`).
  - `--wrn-bd`, `--wrn-bg` (amber): Warnings / important (`.note-box`).
  - `--crit-bd`, `--crit-bg` (red-orange): Critical warnings (`.warning-box`).
- **Full-width screen coverage**: Text and topic cards span the full available width of the screen (`width: 100%`). Do not constrain `.module-container` or `.topic-card` with artificial `max-width: 860px`.
- **Generous whitespace**: 36px/40px card padding, 18px callout margins, 1.75 line-height on body text. Content should breathe, never feel cramped.
- **Subtle interactivity**: cards glow brand color on hover, details toggle brand on hover, back-to-top fades in. Transitions stay ≤0.3s — smooth but snappy.
- **Typography hierarchy**: Poppins at 600/700 for headings, 400 for body, 300 for muted text. This creates a clear visual flow so students can scan quickly.
- **Multi-page architecture**: Topics are loaded dynamically as single views rather than all scrolling at once, with next/previous buttons for pagination.

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

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1.0" />
    <title>[Course] — Notes</title>
    <link
      href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap"
      rel="stylesheet"
    />
    <!-- Adjust path to notes.css depending on folder depth -->
    <link rel="stylesheet" href="../notes.css" />
  </head>
  <body>
    <button
      id="menu-toggle"
      onclick="document.getElementById('sidebar').classList.toggle('open')"
    >
      ☰
    </button>
    <div id="sidebar">
      <div class="sidebar-header">
        <div class="sidebar-course-label">Course Notes</div>
        <div class="sidebar-title">[Course]</div>
      </div>
      <div class="sidebar-search-wrap">
        <input
          type="text"
          id="search-input"
          placeholder="Search topics…"
          onkeyup="filterContent()"
        />
      </div>
      <ul class="nav-list" id="nav-list">
        <li class="nav-section">
          <div class="nav-section-title" onclick="toggleSection(this)">
            <span>New Module</span>
            <span class="chevron">▼</span>
          </div>
          <ul class="nav-sublist">
            <li>
              <a href="javascript:void(0)" onclick="showTopic('topic-1')">
                <span class="nav-num">01</span>Topic Title
              </a>
            </li>
          </ul>
        </li>
      </ul>
    </div>
    <div id="main-content">
      <div class="module-container" id="module-new">
        <div class="module-header">
          <div class="module-eyebrow">[Course]</div>
          <h1 class="module-title">New Module</h1>
        </div>
        <!-- Each topic card: -->
        <div class="topic-card" id="topic-1">
          <h2><span class="topic-num">1</span>Topic Title</h2>
          <p class="topic-subtitle">One-line descriptor</p>
          <p>Topic introduction paragraph...</p>
          <div class="definition">
            <div class="callout-label">Definition</div>
            <strong>Term:</strong> Formal definition...
          </div>
          <div class="note-box">
            <div class="callout-label">Pro Tip</div>
            ...
          </div>
          <div class="warning-box">
            <div class="callout-label">Common Mistake</div>
            ...
          </div>
          <div class="example">
            <div class="callout-label">Example</div>
            <h4>Title</h4>
            ...
          </div>
          <div class="summary-box">
            <h4>Key Takeaways</h4>
            <ul>
              <li>...</li>
            </ul>
          </div>
          <details>
            <summary>Practice Q: ...</summary>
            <p><strong>Answer:</strong> ...</p>
          </details>
        </div>
      </div>
      <div class="bottom-nav">
        <button id="prev-btn" onclick="goPrev()">
          <div>
            <span class="btn-label">← Previous</span>
            <span class="btn-title" id="prev-title">Topic</span>
          </div>
        </button>
        <button id="next-btn" onclick="goNext()">
          <div>
            <span class="btn-label">Next →</span>
            <span class="btn-title" id="next-title">Topic</span>
          </div>
        </button>
      </div>
    </div>
    <button
      id="back-to-top"
      onclick="
        document
          .getElementById('main-content')
          .scrollTo({ top: 0, behavior: 'smooth' })
      "
    >
      ↑
    </button>
    <script>
      const topics = ["topic-1"]; // e.g. ["topic-1","topic-2"]
      let currentTopicIndex = 0;
      function showTopic(id) {
        document
          .querySelectorAll(".topic-card")
          .forEach((c) => (c.style.display = "none"));
        const t = document.getElementById(id);
        if (t) t.style.display = "block";
        currentTopicIndex = topics.indexOf(id);
        document
          .querySelectorAll(".nav-sublist a")
          .forEach((a) => a.classList.remove("active"));
        const lk = document.querySelector(
          `.nav-sublist a[onclick="showTopic('${id}')"]`,
        );
        if (lk) lk.classList.add("active");
        const pb = document.getElementById("prev-btn"),
          nb = document.getElementById("next-btn"),
          pt = document.getElementById("prev-title"),
          nt = document.getElementById("next-title");
        if (currentTopicIndex > 0) {
          pb.style.display = "flex";
          const pl = document.querySelector(
            `.nav-sublist a[onclick="showTopic('${topics[currentTopicIndex - 1]}')"]`,
          );
          if (pt && pl)
            pt.textContent = pl.querySelector(".nav-num")
              ? pl.textContent
                  .replace(pl.querySelector(".nav-num").textContent, "")
                  .trim()
              : pl.innerText.trim();
        } else {
          pb.style.display = "none";
        }
        if (currentTopicIndex < topics.length - 1) {
          nb.style.display = "flex";
          const nl = document.querySelector(
            `.nav-sublist a[onclick="showTopic('${topics[currentTopicIndex + 1]}')"]`,
          );
          if (nt && nl)
            nt.textContent = nl.querySelector(".nav-num")
              ? nl.textContent
                  .replace(nl.querySelector(".nav-num").textContent, "")
                  .trim()
              : nl.innerText.trim();
        } else {
          nb.style.display = "none";
        }
        document
          .getElementById("main-content")
          .scrollTo({ top: 0, behavior: "smooth" });
      }
      function goPrev() {
        if (currentTopicIndex > 0) showTopic(topics[currentTopicIndex - 1]);
      }
      function goNext() {
        if (currentTopicIndex < topics.length - 1)
          showTopic(topics[currentTopicIndex + 1]);
      }
      function toggleSection(el) {
        const s = el.nextElementSibling,
          c = el.querySelector(".chevron");
        if (s.style.display === "none") {
          s.style.display = "block";
          c.style.transform = "rotate(0deg)";
        } else {
          s.style.display = "none";
          c.style.transform = "rotate(-90deg)";
        }
      }
      function filterContent() {
        const q = document.getElementById("search-input").value.toLowerCase();
        document
          .querySelectorAll(".nav-sublist li")
          .forEach(
            (i) =>
              (i.style.display = i.textContent.toLowerCase().includes(q)
                ? ""
                : "none"),
          );
      }
      if (topics.length > 0) showTopic(topics[0]);
      const mc = document.getElementById("main-content"),
        bb = document.getElementById("back-to-top");
      mc.addEventListener(
        "scroll",
        () => (bb.style.display = mc.scrollTop > 300 ? "flex" : "none"),
      );
    </script>
  </body>
</html>
```
```