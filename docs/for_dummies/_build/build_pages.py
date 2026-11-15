#!/usr/bin/env python3
"""Builds the openMemristorPDK beginner guide (docs/for_dummies/*.html).

Each section's steps live in _src/<slug>.html; this script wraps them in
the shared page frame (top bar, hero, "on this page", pager, footer,
step player) and writes index.html with the introduction and the
section index. To add a section: write _src/<slug>.html and add one
entry to SECTIONS (status "soon" lists it on the index without a page;
"draft" builds the page with a draft banner; a draft that already has
screenshot steps also gets the step player, and "draftnote" overrides
the banner text).

    python3 docs/for_dummies/_build/build_pages.py
"""

from __future__ import annotations

import html
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent  # docs/for_dummies

GUIDE_TITLE = "openMemristorPDK Guide"

SECTIONS = [
    {
        "slug": "install",
        "title": "Install from scratch",
        "short": "Install",
        "status": "ready",
        "time": "30–60 min, mostly waiting · once per computer",
        "desc": "Get a new Linux computer ready: two programs, openPDKcreator, the memristor PDK "
                "and the container with all the chip-design tools.",
        "lede": "Everything you need, downloaded and set up on a new Linux computer: two programs, "
                "openPDKcreator, the memristor PDK, and the container with all the chip-design tools. "
                "You only do this once per computer.",
        "prereq": "",
    },
    {
        "slug": "first-simulation",
        "title": "Your first simulation",
        "short": "First simulation",
        "status": "ready",
        "time": "about 10 min · 24 steps",
        "desc": "Start the tools, read the memristor's model, simulate its pinched hysteresis loop "
                "in xschem and ngspice, then look at its chip layout in KLayout.",
        "lede": "From a closed laptop to a real simulated memristor curve on your screen, and a look "
                "at the chip itself, in 24 steps.",
        "prereq": 'First time on this computer? Do <a href="install.html">Install from scratch</a> first.',
    },
    {
        "slug": "add-model",
        "title": "Add a model",
        "short": "Add a model",
        "status": "ready",
        "time": "about 15 min · 24 steps",
        "desc": "Write a new Verilog-A memristor model, let openPDKcreator compile it, "
                "and try it in the testbench in place of the old one.",
        "lede": "Give the PDK a brand-new memristor model, the HP memristor with a Joglekar window, "
                "then swap it into the testbench and compare its loop with the first one.",
        "prereq": 'Start with openPDKcreator open, as after steps 1–4 of '
                  '<a href="first-simulation.html">Your first simulation</a>. You\'ll also use the laptop\'s terminal once.',
    },
    {
        "slug": "add-device",
        "title": "Add a new device",
        "short": "Add a device",
        "status": "ready",
        "time": "about 15 min · 33 steps",
        "lede": "Delete the Au/HfO₂/Al memristor completely, then rebuild every piece of it: its model, "
                "its symbol, its layout and a testbench, and watch it switch on and off.",
        "prereq": 'Do <a href="add-model.html">Add a model</a> first: this section uses the same moves '
                  '(New Cell, a terminal command, View and Close). Start with openPDKcreator open in the Library Manager.',
        "desc": "Delete the Au/HfO₂/Al memristor and rebuild it from nothing: layers, layout, "
                "symbol, model and testbench.",
    },
    {
        "slug": "corners-montecarlo",
        "title": "Corners and Monte Carlo",
        "short": "Monte Carlo",
        "status": "ready",
        "time": "about 15 min · 41 steps",
        "desc": "Simulate the TT/FF/SS process corners, then a Monte Carlo run where Ron, Roff and "
                "the oxide thickness vary from device to device.",
        "lede": "No two devices from a factory are exactly alike. Read the PDK's process corners, simulate "
                "the typical and the slow memristor, then build 20 random memristors in one Monte Carlo run "
                "and find out which manufacturing spread matters most.",
        "prereq": 'Do <a href="first-simulation.html">Your first simulation</a> first: this section uses the '
                  'same moves (Netlist, Simulate, Quit, quit). Start with openPDKcreator open.',
    },
    {
        "slug": "digital",
        "title": "The digital side",
        "short": "Digital",
        "status": "draft",
        "time": "about 30 min · 56 steps · draft",
        "desc": "Store a bit in a memristor, see a write that is too weak fail, write a pattern into a "
                "2 × 2 crossbar and simulate a digital twin in Verilog.",
        "lede": "A memristor can store a bit with no power at all. Write a 1 into the Au/HfO₂/Al memristor, "
                "read it back, erase it, find out why a write that is too weak does nothing, "
                "then store four bits in a crossbar without disturbing the neighbours, and simulate "
                "the same memory the way digital designers do, in Verilog.",
        "prereq": 'Easier after <a href="add-device.html">Add a new device</a>: it uses the Au/HfO₂/Al memristor. '
                  'Start with openPDKcreator open (steps 1–3 of <a href="first-simulation.html">Your first simulation</a>).',
        "draftnote": 'Parts 1–5 are finished, with a real screenshot for every click. Parts 6 and 7 are still a '
                     'first draft we are working on together: ideas, a plan and open questions.',
    },
]

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:'
    'ital,wght@0,400;0,700;1,400&family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&'
    'family=JetBrains+Mono:wght@400;600&display=swap">'
)

LEGEND = '''  <div class="hero-row">
    <button class="btn" type="button" id="play-all">▶ Play as video</button>
    <span class="legend">
      <span><i class="swatch-box"></i> click here</span>
      <span>Click any screenshot to see it full size</span>
      <span>Keys in the player: <kbd>←</kbd> <kbd>→</kbd> <kbd>Space</kbd> <kbd>Esc</kbd></span>
    </span>
  </div>'''

PLAYER = '''<div class="overlay" id="player" hidden role="dialog" aria-modal="true" aria-label="Step player">
  <div class="bar">
    <div class="title"><span class="n" id="p-n"></span><span id="p-title"></span></div>
    <button type="button" id="p-close">Close ✕</button>
  </div>
  <div class="stage" id="p-stage"></div>
  <div style="display:grid;gap:10px">
    <p class="do-line" id="p-do"></p>
    <div class="progress" aria-hidden="true"><i id="p-bar"></i></div>
    <div class="ctrls">
      <button type="button" id="p-prev">← Back</button>
      <button type="button" class="primary" id="p-play">⏸ Pause</button>
      <button type="button" id="p-next">Next →</button>
    </div>
  </div>
</div>'''

FUNDING = ('<div class="funding"><img src="img/miciu_aei.png" alt="Ministerio de Ciencia, Innovación y Universidades and Agencia Estatal de Investigación" width="1600" height="393">'
           '<p>Project PID2025-170062NB (MemFRAME) funded by <span class="nw">MICIU/AEI/'
           '<a href="https://doi.org/10.13039/501100011033">10.13039/501100011033</a></span></p></div>')

FOOTER = '''<footer>
  <p>Every screenshot was taken from the real programs with real mouse clicks: openPDKcreator, xschem, ngspice with OpenVAF-compiled models and KLayout, inside the IIC-OSIC-TOOLS container. The capture scripts are in <code>docs/for_dummies/_capture/</code>.</p>
  <p>Created by R. Picos (<a href="mailto:rpicos.uib@gmail.com">rpicos.uib@gmail.com</a> / <a href="mailto:rodrigo.picos@uib.es">rodrigo.picos@uib.es</a>), as part of the research project <b>MemFRAME</b>.</p>
  ''' + FUNDING + '''
  <p><a href="https://github.com/rpicos-uib/openMemristorPDK">openMemristorPDK</a> · <a href="https://github.com/rpicos-uib/openpdkcreator-toolkit">openPDKcreator</a> · Apache License 2.0</p>
</footer>'''


DRAFT_NOTE = (
    '  <p class="draftnote"><strong>Draft</strong> This section is a first draft we are still '
    'working on together: the ideas and the plan, real simulation results, but no click-by-click '
    'screenshots yet. Read it, comment on it, and expect it to change.</p>'
)


def ready() -> list[dict]:
    return [s for s in SECTIONS if s["status"] in ("ready", "draft")]


def topbar(current: str | None) -> str:
    links = []
    for s in ready():
        cur = ' aria-current="page"' if s["slug"] == current else ""
        links.append(f'<a href="{s["slug"]}.html"{cur}>{s["short"]}</a>')
    home_cur = ' aria-current="page"' if current is None else ""
    return (
        '<header class="topbar"><div class="inner">\n'
        f'  <a class="brand" href="index.html"><span class="mark" aria-hidden="true"></span>{GUIDE_TITLE}</a>\n'
        f'  <nav class="topnav" aria-label="Guide sections"><a href="index.html"{home_cur}>Overview</a>'
        + "".join(links) + "</nav>\n"
        "</div></header>"
    )


def page(title: str, description: str, current: str | None, body: str, player: bool) -> str:
    return (
        "<!doctype html>\n<html lang=\"en\">\n<head>\n"
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<meta name="claude:viewport-fit-sides" content="cover">\n'
        f"<title>{html.escape(title)}</title>\n"
        f'<meta name="description" content="{html.escape(description)}">\n'
        f"{FONTS}\n"
        '<link rel="stylesheet" href="guide.css">\n'
        "</head>\n<body>\n"
        f"{topbar(current)}\n"
        f'<div class="wrap">\n{body}\n{FOOTER}\n</div>\n'
        + (f"\n{PLAYER}\n" if player else "")
        + '<script src="guide.js"></script>\n</body>\n</html>\n'
    )


def add_step_ids(src: str) -> str:
    """id="step-<n>" on every step card, so other pages can link to a step."""

    return re.sub(
        r'<article class="step"(?![^>]*\bid=)([^>]*>\s*<div class="step-head"><span class="num">([^<]+)</span>)',
        lambda m: f'<article class="step" id="step-{m.group(2).lower()}"{m.group(1)}',
        src,
    )


def on_this_page(src: str) -> str:
    parts = re.findall(r'<section class="chapter" id="([^"]+)">.*?<h2>(.*?)</h2>', src, re.S)
    if len(parts) < 2:
        return ""
    chips = "".join(f'<a href="#{pid}">{title}</a>' for pid, title in parts)
    return f'  <nav class="onpage" aria-label="On this page"><span>On this page:</span>{chips}</nav>'


def section_page(i: int, s: dict) -> str:
    src = add_step_ids((HERE.parent / "_src" / f'{s["slug"]}.html').read_text(encoding="utf-8"))
    n = SECTIONS.index(s) + 1
    prereq = f'  <p class="prereq">{s["prereq"]}</p>\n' if s.get("prereq") else ""
    # A draft can already contain real screenshot steps: then it gets the
    # red-box hint and the step player too, plus its draft note.
    draft = s["status"] == "draft"
    has_steps = not draft or 'data-img="' in src
    note = ""
    if draft:
        note = (f'  <p class="draftnote"><strong>Draft</strong> {s["draftnote"]}</p>'
                if s.get("draftnote") else DRAFT_NOTE) + "\n"
    hero = (
        '<header class="hero">\n'
        f'  <div class="crumbs"><a href="index.html">Guide</a> · Section {n} · {s["time"]}</div>\n'
        f'  <h1>{s["title"]}</h1>\n'
        f'  <p class="lede">{s["lede"]}'
        + (' You only ever need to click whatever is inside the '
           '<b class="ui">red box</b>, or type exactly what is in a black box.' if has_steps else '')
        + '</p>\n'
        f"{prereq}{note}{LEGEND + chr(10) if has_steps else ''}{on_this_page(src)}\n"
        "</header>"
    )
    rs = ready()
    prev_s = rs[i - 1] if i > 0 else None
    next_s = rs[i + 1] if i + 1 < len(rs) else None
    pager = '<nav class="pager" aria-label="Previous and next section">'
    pager += (f'<a class="prev" href="{prev_s["slug"]}.html"><span class="dir">← Previous</span>'
              f'<span class="t">{prev_s["title"]}</span></a>') if prev_s else \
             '<a class="prev" href="index.html"><span class="dir">← Back to</span><span class="t">Guide overview</span></a>'
    pager += (f'<a class="next" href="{next_s["slug"]}.html"><span class="dir">Next →</span>'
              f'<span class="t">{next_s["title"]}</span></a>') if next_s else \
             '<a class="next" href="index.html"><span class="dir">Back to →</span><span class="t">Guide overview</span></a>'
    pager += "</nav>"
    return page(f'{s["title"]} · {GUIDE_TITLE}', s["desc"], s["slug"], f"{hero}\n\n{src}\n{pager}", player=True)


def index_page() -> str:
    cards = []
    for n, s in enumerate(SECTIONS, 1):
        if s["status"] == "draft":
            cards.append(
                f'  <a class="card" href="{s["slug"]}.html">\n'
                f'    <span class="no">SECTION {n}</span><h3>{s["title"]}</h3><p>{s["desc"]}</p>\n'
                f'    <span class="meta"><span class="pill draft">Draft</span>{s["time"]}</span>\n  </a>'
            )
        elif s["status"] == "ready":
            cards.append(
                f'  <a class="card" href="{s["slug"]}.html">\n'
                f'    <span class="no">SECTION {n}</span><h3>{s["title"]}</h3><p>{s["desc"]}</p>\n'
                f'    <span class="meta"><span class="pill ready">Ready</span>{s["time"]}</span>\n  </a>'
            )
        else:
            cards.append(
                f'  <div class="card soon">\n'
                f'    <span class="no">SECTION {n}</span><h3>{s["title"]}</h3><p>{s["desc"]}</p>\n'
                f'    <span class="meta"><span class="pill soon">In preparation</span></span>\n  </div>'
            )
    first = ready()[0]
    body = f'''<header class="hero">
  {FUNDING}
  <div class="eyebrow">openMemristorPDK · beginner's guide</div>
  <h1>Design with memristors, step by step</h1>
  <p class="lede">A hands-on guide to openMemristorPDK, a small chip-design kit for memristors built with openPDKcreator. Every step shows a real screenshot of what to click, from installing the tools to simulating a memristor and looking at its layout. No chip-design experience needed.</p>
  <div class="hero-row"><a class="btn" href="{first["slug"]}.html">Start with section 1 →</a></div>
</header>

<section class="chapter" id="about">
  <header>
    <div class="eyebrow">Before you start</div>
    <h2>What this guide is about</h2>
  </header>
  <div class="intro-grid">
    <div><h3>What is a memristor?</h3><p>A resistor with a memory. Its resistance depends on how much current has flowed through it before, so it "remembers". Its fingerprint is the <b>pinched hysteresis loop</b> you will simulate in section 2.</p></div>
    <div><h3>What is a PDK?</h3><p>A <em>Process Design Kit</em>: the instruction manual a chip factory gives designers. It says which materials and layers exist, how small things can be, and how each device behaves. openMemristorPDK describes a made-up factory that builds memristors.</p></div>
    <div><h3>How to read the steps</h3><ul><li>Click what is inside the <b class="ui">red box</b>.</li><li>Type exactly what is in a black box (or use its <b>Copy</b> button).</li><li><b>Play as video</b> walks through a section on its own.</li><li>Click a screenshot to see it full size.</li></ul></div>
    <div><h3>What you need</h3><ul><li>A Linux computer (Ubuntu or similar).</li><li>About 35 GB of free disk space and an internet connection, the first time.</li><li>No programming: every command is given.</li></ul></div>
  </div>
</section>

<section class="chapter" id="sections">
  <header>
    <div class="eyebrow">Sections</div>
    <h2>Pick where to start</h2>
    <p>Do the sections in order the first time. Later ones build on the earlier ones.</p>
  </header>
  <div class="cards">
{chr(10).join(cards)}
  </div>
</section>'''
    return page(GUIDE_TITLE, "A step-by-step beginner's guide to openMemristorPDK: install the tools, "
                "simulate a memristor and look at its chip layout.", None, body, player=False)


def main() -> None:
    (ROOT / "index.html").write_text(index_page(), encoding="utf-8")
    for i, s in enumerate(ready()):
        (ROOT / f'{s["slug"]}.html').write_text(section_page(i, s), encoding="utf-8")
    print("wrote index.html and", ", ".join(f'{s["slug"]}.html' for s in ready()))


if __name__ == "__main__":
    main()
