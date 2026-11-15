#!/usr/bin/env python3
"""Builds the openMemristorPDK beginner guide (docs/for_dummies/*.html).

Each section's steps live in _src/<slug>.html; this script wraps them in
the shared page frame (top bar, hero, "on this page", pager, footer,
step player) and writes index.html with the introduction and the
section index. To add a section: write _src/<slug>.html and add one
entry to SECTIONS (status "soon" lists it on the index without a page;
"draft" builds the page with a draft banner; a draft that already has
screenshot steps also gets the step player, and "draftnote" overrides
the banner text). A section with "children" is a hub: _src/<slug>.html
holds its own text, with <!--PARTS--> where the part cards go, and each
child is a part page of its own (_src/<child-slug>.html).

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
        "slug": "foss",
        "group": "intro",
        "title": "Introduction to FOSS",
        "short": "FOSS",
        "status": "ready",
        "time": "5 parts · about 20 min",
        "desc": "What free and open-source software is, what each program in this guide does and how to install it, "
                "and openPDKcreator's Tools tab, which checks them all.",
        "lede": "Every program in this guide is free and open-source software. Meet them one by one: what each does, "
                "who makes it, how to install it. Then let openPDKcreator's Tools tab check them for you.",
        "prereq": "",
        "children": [
            {
                "slug": "foss-laptop",
                "title": "On your laptop",
                "status": "ready",
                "time": "about 3 min to read",
                "desc": "Git, Podman and IIC-OSIC-TOOLS: the two programs on the laptop and the container they start.",
                "lede": "Two programs live on the laptop itself, Git and Podman. Together they bring the container that "
                        "holds everything else.",
                "prereq": "",
            },
            {
                "slug": "foss-analog",
                "title": "Drawing and simulating",
                "status": "ready",
                "time": "about 4 min to read",
                "desc": "openPDKcreator, xschem, ngspice and OpenVAF: the programs the Analog sections use.",
                "lede": "The PDK window, the schematic editor, the circuit simulator and the compiler that turns a "
                        "memristor model into something the simulator can run.",
                "prereq": "",
            },
            {
                "slug": "foss-layout",
                "title": "Layouts and checks",
                "status": "ready",
                "time": "about 3 min to read",
                "desc": "KLayout, Magic and Netgen: look at a chip layout and check it (DRC and LVS).",
                "lede": "The drawing the factory builds from, and the two checks every layout must pass before it "
                        "goes to the factory.",
                "prereq": "",
            },
            {
                "slug": "foss-digital",
                "title": "Digital tools",
                "status": "ready",
                "time": "about 4 min to read",
                "desc": "Icarus Verilog, GTKWave, Yosys, OpenROAD and LibreLane: from Verilog to a chip layout.",
                "lede": "Simulate bits, look at them as waveforms, turn Verilog into logic gates, and turn the gates "
                        "into a chip layout.",
                "prereq": "",
            },
            {
                "slug": "foss-tools-tab",
                "title": "openPDKcreator's Tools tab",
                "status": "ready",
                "time": "about 5 min",
                "desc": "Let openPDKcreator check every program: found or missing, version, how to install it, "
                        "and a button to start it.",
                "lede": "One tab in openPDKcreator checks every program on the other pages: is it there, which version, "
                        "how to install it. It can also start them.",
                "prereq": 'Do <a href="install.html">Install from scratch</a> first, and start with openPDKcreator open '
                          '(steps 1–5 of <a href="first-simulation.html">Your first simulation</a>).',
            },
        ],
    },
    {
        "slug": "install",
        "group": "install",
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
        "slug": "ihp",
        "group": "install",
        "title": "Add IHP's PDK",
        "short": "IHP PDK",
        "status": "ready",
        "time": "about 7 min · 9 steps",
        "desc": "Use IHP's open SG13G2 PDK, with real transistors and logic gates, next to the memristor PDK. "
                "Needed for the last digital parts.",
        "lede": "openMemristorPDK has no transistors, on purpose. Borrow them from IHP's open SG13G2 PDK: "
                "check it is in the container, give openPDKcreator its own copy, and open it next to ours.",
        "prereq": 'Do <a href="install.html">Install from scratch</a> first, and start with openPDKcreator open '
                  '(steps 1–3 of <a href="first-simulation.html">Your first simulation</a>).',
    },
    {
        "slug": "first-simulation",
        "group": "analog",
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
        "group": "analog",
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
        "group": "analog",
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
        "group": "analog",
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
        "group": "digital",
        "title": "The digital side",
        "short": "Digital",
        "status": "ready",
        "time": "6 parts · about 1 hour",
        "desc": "Use memristors as bits: store one, fill a 2 × 2 crossbar, describe it in Verilog, turn its "
                "controller into IHP logic gates and a chip layout, and build a real 1T1R bit-cell.",
        "lede": "A memristor can store a bit with no power at all. These parts go from one memristor in a "
                "simulator to a small memory whose controller becomes real logic gates and a real chip layout.",
        "prereq": "",
        "children": [
            {
                "slug": "digital-bit",
                "title": "Store a bit",
                "status": "ready",
                "time": "about 10 min",
                "desc": "Write a 1 into one memristor, read it back, erase it, and see a write that is too weak fail.",
                "lede": "Write a 1 into the Au/HfO₂/Al memristor, read it back and erase it, then find out why a "
                        "write that is too weak does nothing.",
                "prereq": 'Easier after <a href="add-device.html">Add a new device</a>: it uses the Au/HfO₂/Al memristor. '
                          'Start with openPDKcreator open (steps 1–3 of <a href="first-simulation.html">Your first simulation</a>).',
            },
            {
                "slug": "digital-crossbar",
                "title": "Write a pattern into a crossbar",
                "status": "ready",
                "time": "about 10 min",
                "desc": "Four memristors in a 2 × 2 grid: write 1 0 0 1 without disturbing the neighbours, "
                        "then see a careless write overwrite them.",
                "lede": "Store four bits in a 2 × 2 crossbar without disturbing the neighbours, then see what a "
                        "careless write does to them.",
                "prereq": 'Do <a href="digital-bit.html">Store a bit</a> first: same moves (Netlist, Simulate, Edit Properties).',
            },
            {
                "slug": "digital-twin",
                "title": "A digital twin in Verilog",
                "status": "ready",
                "time": "about 10 min",
                "desc": "Describe the memristor bit the way digital designers do, simulate it with Icarus Verilog "
                        "and look at the waveforms in GTKWave.",
                "lede": "Simulate the same bit the way digital designers do: a short Verilog description, Icarus "
                        "Verilog, and waveforms in GTKWave.",
                "prereq": 'Do <a href="digital-bit.html">Store a bit</a> first: this part gives the same answers without volts.',
            },
            {
                "slug": "digital-gates",
                "title": "A controller made of real logic gates",
                "status": "ready",
                "time": "about 10 min",
                "desc": "Write a small memory controller in Verilog and let Yosys turn it into 65 logic gates "
                        "from IHP's library.",
                "lede": "Build a 4-bit memory with a controller, then let Yosys turn the controller into real logic "
                        "gates from IHP's SG13G2 library.",
                "prereq": 'Do <a href="digital-twin.html">A digital twin in Verilog</a> first: it uses the same terminal.',
            },
            {
                "slug": "digital-layout",
                "title": "From gates to a chip layout",
                "status": "ready",
                "time": "about 10 min",
                "desc": "Place and wire the controller's gates with LibreLane and IHP's standard cells, and look at "
                        "the result in KLayout.",
                "lede": "Turn the controller's gates into a real chip layout with LibreLane: placed, wired, checked "
                        "and ready to build, in about two minutes.",
                "prereq": 'Do <a href="digital-gates.html">A controller made of real logic gates</a> first.',
            },
            {
                "slug": "digital-1t1r",
                "title": "A real bit-cell: 1T1R",
                "status": "ready",
                "time": "about 10 min",
                "desc": "Put IHP's transistor in series with the memristor: a door that blocks writes to the cells "
                        "you don't want to change.",
                "lede": "Add IHP's transistor to the memristor to make the bit-cell real memory chips use.",
                "prereq": 'Do <a href="ihp.html">Add IHP\'s PDK</a> first, and <a href="digital-bit.html">Store a bit</a>.',
            },
        ],
    },
]

GROUPS = [
    {"id": "intro", "title": "Introduction",
     "intro": "The free programs this guide is built on: what they are and how they fit together."},
    {"id": "install", "title": "Installing",
     "intro": "Get the tools and the PDKs onto your computer. You do this once per computer."},
    {"id": "analog", "title": "Analog",
     "intro": "Memristors as analog devices: simulate their currents and voltages, write new models, build a new "
              "device and see how a factory's spread changes them."},
    {"id": "digital", "title": "Digital",
     "intro": "Memristors as bits: store them, fill a small memory, describe it in Verilog, and turn its controller "
              "into real logic gates and a chip layout."},
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


def ready_children(s: dict) -> list[dict]:
    return [c for c in s.get("children", []) if c["status"] in ("ready", "draft")]


def reading_order() -> list[dict]:
    """Every page in reading order: each section, then its ready parts."""
    order = []
    for s in ready():
        order.append(s)
        order.extend(ready_children(s))
    return order


def parent_of(slug: str) -> dict | None:
    for s in SECTIONS:
        if any(c["slug"] == slug for c in s.get("children", [])):
            return s
    return None


def steps_label(slug: str) -> str:
    """" · N steps", or nothing for a reading-only page."""
    n = count_steps(slug)
    return f" · {n} steps" if n else ""


def count_steps(slug: str) -> int:
    src = (HERE.parent / "_src" / f"{slug}.html").read_text(encoding="utf-8")
    return len(re.findall(r'<span class="num">\d+</span>', src))


def topbar(current: str | None) -> str:
    links = []
    par = parent_of(current) if current else None
    for s in ready():
        cur = ' aria-current="page"' if s["slug"] == current or (par and par["slug"] == s["slug"]) else ""
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


def pager(s: dict) -> str:
    order = reading_order()
    i = order.index(s)
    prev_s = order[i - 1] if i > 0 else None
    next_s = order[i + 1] if i + 1 < len(order) else None
    out = '<nav class="pager" aria-label="Previous and next section">'
    out += (f'<a class="prev" href="{prev_s["slug"]}.html"><span class="dir">← Previous</span>'
            f'<span class="t">{prev_s["title"]}</span></a>') if prev_s else \
           '<a class="prev" href="index.html"><span class="dir">← Back to</span><span class="t">Guide overview</span></a>'
    out += (f'<a class="next" href="{next_s["slug"]}.html"><span class="dir">Next →</span>'
            f'<span class="t">{next_s["title"]}</span></a>') if next_s else \
           '<a class="next" href="index.html"><span class="dir">Back to →</span><span class="t">Guide overview</span></a>'
    return out + "</nav>"


def crumbs(s: dict) -> str:
    par = parent_of(s["slug"])
    if par:
        n = SECTIONS.index(par) + 1
        k = par["children"].index(s) + 1
        return (f'<a href="index.html">Guide</a> · Section {n} · <a href="{par["slug"]}.html">{par["title"]}</a>'
                f' · Part {k} · {s["time"]}{steps_label(s["slug"])}')
    return f'<a href="index.html">Guide</a> · Section {SECTIONS.index(s) + 1} · {s["time"]}'


def section_page(i: int, s: dict) -> str:
    src = add_step_ids((HERE.parent / "_src" / f'{s["slug"]}.html').read_text(encoding="utf-8"))
    prereq = f'  <p class="prereq">{s["prereq"]}</p>\n' if s.get("prereq") else ""
    # A draft can already contain real screenshot steps: then it gets the
    # red-box hint and the step player too, plus its draft note.
    draft = s["status"] == "draft"
    has_steps = 'data-img="' in src  # reading-only pages get no player
    note = ""
    if draft:
        note = (f'  <p class="draftnote"><strong>Draft</strong> {s["draftnote"]}</p>'
                if s.get("draftnote") else DRAFT_NOTE) + "\n"
    hero = (
        '<header class="hero">\n'
        f'  <div class="crumbs">{crumbs(s)}</div>\n'
        f'  <h1>{s["title"]}</h1>\n'
        f'  <p class="lede">{s["lede"]}'
        + (' You only ever need to click whatever is inside the '
           '<b class="ui">red box</b>, or type exactly what is in a black box.' if has_steps else '')
        + '</p>\n'
        f"{prereq}{note}{LEGEND + chr(10) if has_steps else ''}{on_this_page(src)}\n"
        "</header>"
    )
    return page(f'{s["title"]} · {GUIDE_TITLE}', s["desc"], s["slug"], f"{hero}\n\n{src}\n{pager(s)}", player=has_steps)


def part_cards(s: dict) -> str:
    cards = []
    for k, c in enumerate(s["children"], 1):
        if c["status"] == "ready":
            cards.append(
                f'  <a class="card" href="{c["slug"]}.html">\n'
                f'    <span class="no">PART {k}</span><h3>{c["title"]}</h3><p>{c["desc"]}</p>\n'
                f'    <span class="meta"><span class="pill ready">Ready</span>{c["time"]}{steps_label(c["slug"])}</span>\n  </a>'
            )
        else:
            cards.append(
                f'  <div class="card soon">\n'
                f'    <span class="no">PART {k}</span><h3>{c["title"]}</h3><p>{c["desc"]}</p>\n'
                f'    <span class="meta"><span class="pill soon">In preparation</span></span>\n  </div>'
            )
    return (
        '<section class="chapter" id="parts">\n  <header>\n    <div class="eyebrow">Parts</div>\n'
        '    <h2>Pick a part</h2>\n    <p>Do them in order the first time: each one builds on the one before.</p>\n'
        '  </header>\n  <div class="cards">\n' + "\n".join(cards) + '\n  </div>\n</section>'
    )


def hub_page(s: dict) -> str:
    src = (HERE.parent / "_src" / f'{s["slug"]}.html').read_text(encoding="utf-8")
    src = add_step_ids(src.replace("<!--PARTS-->", part_cards(s)))
    first = ready_children(s)[0]
    hero = (
        '<header class="hero">\n'
        f'  <div class="crumbs">{crumbs(s)}</div>\n'
        f'  <h1>{s["title"]}</h1>\n'
        f'  <p class="lede">{s["lede"]}</p>\n'
        f'  <div class="hero-row"><a class="btn" href="{first["slug"]}.html">Start with part 1 →</a></div>\n'
        f'{on_this_page(src)}\n'
        "</header>"
    )
    return page(f'{s["title"]} · {GUIDE_TITLE}', s["desc"], s["slug"], f"{hero}\n\n{src}\n{pager(s)}", player=False)


def section_card(n: int, s: dict, label: str | None = None) -> str:
    label = label or f"SECTION {n}"
    if s["status"] in ("ready", "draft"):
        pill = '<span class="pill draft">Draft</span>' if s["status"] == "draft" else '<span class="pill ready">Ready</span>'
        return (f'  <a class="card" href="{s["slug"]}.html">\n'
                f'    <span class="no">{label}</span><h3>{s["title"]}</h3><p>{s["desc"]}</p>\n'
                f'    <span class="meta">{pill}{s["time"]}</span>\n  </a>')
    return (f'  <div class="card soon">\n'
            f'    <span class="no">{label}</span><h3>{s["title"]}</h3><p>{s["desc"]}</p>\n'
            f'    <span class="meta"><span class="pill soon">In preparation</span></span>\n  </div>')


def index_page() -> str:
    chapters = []
    for g in GROUPS:
        cards = []
        for s in SECTIONS:
            if s.get("group") != g["id"]:
                continue
            n = SECTIONS.index(s) + 1
            if s.get("children"):
                cards.append(section_card(n, dict(s, title=s["title"] + ": overview"), f"SECTION {n}"))
                for k, c in enumerate(s["children"], 1):
                    if c["status"] in ("ready", "draft"):
                        c = dict(c, time=f'{c["time"]}{steps_label(c["slug"])}')
                    cards.append(section_card(n, c, f"SECTION {n} · PART {k}"))
            else:
                cards.append(section_card(n, s))
        chapters.append(
            f'<section class="chapter" id="{g["id"]}">\n  <header>\n    <div class="eyebrow">Sections</div>\n'
            f'    <h2>{g["title"]}</h2>\n    <p>{g["intro"]}</p>\n  </header>\n'
            f'  <div class="cards">\n' + "\n".join(cards) + '\n  </div>\n</section>'
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
    <div><h3>What is a memristor?</h3><p>A resistor with a memory. Its resistance depends on how much current has flowed through it before, so it "remembers". Its fingerprint is the <b>pinched hysteresis loop</b> you will simulate in Your first simulation.</p></div>
    <div><h3>What is a PDK?</h3><p>A <em>Process Design Kit</em>: the instruction manual a chip factory gives designers. It says which materials and layers exist, how small things can be, and how each device behaves. openMemristorPDK describes a made-up factory that builds memristors.</p></div>
    <div><h3>How to read the steps</h3><ul><li>Click what is inside the <b class="ui">red box</b>.</li><li>Type exactly what is in a black box (or use its <b>Copy</b> button).</li><li><b>Play as video</b> walks through a section on its own.</li><li>Click a screenshot to see it full size.</li></ul></div>
    <div><h3>What you need</h3><ul><li>A Linux computer (Ubuntu or similar).</li><li>About 35 GB of free disk space and an internet connection, the first time.</li><li>No programming: every command is given.</li></ul></div>
  </div>
</section>

{chr(10).join(chapters)}'''
    return page(GUIDE_TITLE, "A step-by-step beginner's guide to openMemristorPDK: install the tools, "
                "simulate a memristor and look at its chip layout.", None, body, player=False)


def main() -> None:
    (ROOT / "index.html").write_text(index_page(), encoding="utf-8")
    for i, s in enumerate(reading_order()):
        out = hub_page(s) if s.get("children") else section_page(i, s)
        (ROOT / f'{s["slug"]}.html').write_text(out, encoding="utf-8")
    print("wrote index.html and", ", ".join(f'{s["slug"]}.html' for s in reading_order()))


if __name__ == "__main__":
    main()
