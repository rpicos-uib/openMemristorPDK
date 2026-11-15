#!/usr/bin/env python3
"""Builds a real .odp presentation -- 'Building openMemristorPDK' --
directly from the real, already-written content and real,
already-captured screenshots in docs/presentation/walkthrough.tex (a
from-scratch PDK built end to end with openPDKcreator's own Wizard,
Layers, Magic Tech, DRC Rules, Library Manager, Verilog-A and a real
ngspice simulation), not fabricated or re-guessed."""

from odf.opendocument import OpenDocumentPresentation
from odf.style import (
    Style, MasterPage, PageLayout, PageLayoutProperties,
    TextProperties, GraphicProperties, ParagraphProperties, DrawingPageProperties,
)
from odf.draw import Page, Frame, TextBox, Image
from odf.text import P

import os

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, "figures")
OUT = os.path.join(HERE, "walkthrough.odp")

PAGE_W = 28.0   # cm, 16:9
PAGE_H = 15.75  # cm

doc = OpenDocumentPresentation()

# --- page layout / master page -------------------------------------------
pagelayout = PageLayout(name="PDKLayout")
pagelayout.addElement(PageLayoutProperties(
    margin="0cm", pagewidth=f"{PAGE_W}cm", pageheight=f"{PAGE_H}cm",
    printorientation="landscape"))
doc.automaticstyles.addElement(pagelayout)

dpstyle = Style(name="PDKDrawingPage", family="drawing-page")
dpstyle.addElement(DrawingPageProperties(backgroundsize="border"))
doc.automaticstyles.addElement(dpstyle)

masterpage = MasterPage(name="PDKMaster", pagelayoutname=pagelayout, stylename=dpstyle)
doc.masterstyles.addElement(masterpage)

# --- paragraph/text styles -------------------------------------------------
def pstyle(name, size, bold=False, color="#1a1a1a", mono=False):
    s = Style(name=name, family="paragraph")
    kwargs = dict(fontsize=size, fontweight="bold" if bold else "normal", color=color)
    if mono:
        kwargs["fontfamily"] = "Courier New"
    s.addElement(TextProperties(**kwargs))
    doc.automaticstyles.addElement(s)
    return s

st_title = pstyle("STTitle2", "32pt", bold=True, color="#1b3a6b")
st_subtitle = pstyle("STSubtitle2", "18pt", bold=False, color="#444444")
st_heading = pstyle("STHeading2", "24pt", bold=True, color="#1b3a6b")
st_body = pstyle("STBody2", "15pt", bold=False, color="#222222")
st_code = pstyle("STCode2", "13pt", bold=False, color="#1a1a1a", mono=True)
st_caption = pstyle("STCaption2", "12pt", bold=False, color="#555555")

def frame_style(name, **graphic_kwargs):
    s = Style(name=name, family="graphic")
    s.addElement(GraphicProperties(**graphic_kwargs))
    doc.automaticstyles.addElement(s)
    return s

fs_plain = frame_style("FSPlain2", stroke="none", fill="none")

# --- slide builders ---------------------------------------------------------

def new_page(title_text=None, subtitle_text=None):
    page = Page(masterpagename="PDKMaster")
    doc.presentation.addElement(page)
    if title_text is not None:
        f = Frame(stylename=fs_plain, width=f"{PAGE_W-2}cm", height="2.2cm", x="1cm", y="0.6cm")
        page.addElement(f)
        tb = TextBox()
        f.addElement(tb)
        tb.addElement(P(stylename=st_title, text=title_text))
        if subtitle_text:
            tb.addElement(P(stylename=st_subtitle, text=subtitle_text))
    return page


def add_lines(page, lines, x=1.0, y=3.2, w=PAGE_W - 2, h=10.0, style=st_body, code_style=None):
    """lines: list of (text, is_code) tuples, or plain strings (bulleted)."""
    f = Frame(stylename=fs_plain, width=f"{w}cm", height=f"{h}cm", x=f"{x}cm", y=f"{y}cm")
    page.addElement(f)
    tb = TextBox()
    f.addElement(tb)
    for item in lines:
        if isinstance(item, tuple):
            text, is_code = item
        else:
            text, is_code = item, False
        if is_code:
            tb.addElement(P(stylename=code_style or st_code, text=text))
        else:
            tb.addElement(P(stylename=style, text=("•  " + text)))
    return f


def add_image(page, path, x, y, max_w, max_h):
    from PIL import Image as PILImage
    im = PILImage.open(path)
    pw, ph = im.size
    ar = pw / ph
    w, h = max_w, max_w / ar
    if h > max_h:
        h = max_h
        w = max_h * ar
    cx = x + (max_w - w) / 2
    cy = y + (max_h - h) / 2
    f = Frame(stylename=fs_plain, width=f"{w:.2f}cm", height=f"{h:.2f}cm",
              x=f"{cx:.2f}cm", y=f"{cy:.2f}cm")
    page.addElement(f)
    href = doc.addPicture(path)
    f.addElement(Image(href=href))
    return f


def title_slide():
    page = new_page()
    f = Frame(stylename=fs_plain, width=f"{PAGE_W-4}cm", height="8cm", x="2cm", y="3.5cm")
    page.addElement(f)
    tb = TextBox()
    f.addElement(tb)
    tb.addElement(P(stylename=st_title, text="Building openMemristorPDK"))
    tb.addElement(P(stylename=st_heading, text="A minimum memristor PDK, built end-to-end with openPDKcreator"))
    tb.addElement(P(stylename=st_subtitle, text="Wizard → Layers → Magic Tech/DRC → Library Manager → Verilog-A → real ngspice simulation"))
    tb.addElement(P(stylename=st_subtitle, text=""))
    tb.addElement(P(stylename=st_subtitle, text="R. Picos · rpicos.uib@gmail.com / rodrigo.picos@uib.es"))
    tb.addElement(P(stylename=st_subtitle, text="Project PID2025-170062NB (MemFRAME) funded by MICIU/AEI/10.13039/501100011033"))
    add_image(page, os.path.join(HERE, "figures", "miciu_aei.png"), 2, 12.2, 11, 2.7)
    return page


def text_slide(heading, lines):
    page = new_page(heading)
    add_lines(page, lines, y=3.0, h=11.0)
    return page


def image_slide(heading, lines, image_path, caption=None):
    page = new_page(heading)
    if lines:
        add_lines(page, lines, y=3.0, h=2.6)
        img_y = 6.0
    else:
        img_y = 3.2
    img_h = PAGE_H - img_y - 1.3
    add_image(page, image_path, 1.0, img_y, PAGE_W - 2, img_h)
    if caption:
        f = Frame(stylename=fs_plain, width=f"{PAGE_W-2}cm", height="0.8cm", x="1cm", y=f"{PAGE_H-1.1}cm")
        page.addElement(f)
        tb = TextBox()
        f.addElement(tb)
        tb.addElement(P(stylename=st_caption, text=caption))
    return page


# =====================================================================
# 1. Title
title_slide()

# 2. Goal
text_slide(
    "Goal",
    [
        "Note: this short deck is the first pass of the project (a 4-layer, 1-plane stack). The current PDK -- 7 layers, 3 planes, 3 device variants -- is in walkthrough_full.tex.",
        "Build a genuinely minimum PDK for a two-terminal memristor device, using openPDKcreator's own GUI/CLI.",
        "Separate from the IHP-based project: its own directory, its own git history, its own empty starting point -- only the openPDKcreator tool itself is shared.",
        "Every step documented here is a real GUI action, nothing staged.",
        "Capstone: a real openvaf/ngspice transient simulation of the memristor's own compact model, showing the classic pinched I-V hysteresis loop.",
    ],
)

# 3. A separate project, one shared tool
text_slide(
    "A separate project, one shared tool",
    [
        "openPDKcreator tracks two different roots, each its own flag: --pdk-root (the PDK data directory) and --project-root (saves/, user_models/, libraries/, library_index.yaml, export/ -- defaults to the openPDKcreator checkout itself).",
        "So a new project is just a new directory -- no copy of the tool:",
        ("cd openPDKcreator", True),
        ("mkdir -p openMemristorPDK/data/openmemristorpdk", True),
        ("cd openMemristorPDK && git init", True),
        "openMemristorPDK/ is gitignored by openPDKcreator and reachable inside the already-running container at /foss/designs/openMemristorPDK/ -- no new container/mount needed.",
    ],
)

# 4. Launching against the new, empty project
text_slide(
    "Launching against the new, empty project",
    [
        ("cd /foss/designs     # the openPDKcreator checkout", True),
        ("python3 main.py --project-root openMemristorPDK --pdk-root openMemristorPDK/data/openmemristorpdk inventory", True),
        ("> Nothing found -- has ihp/fetch.py been run yet?", True),
        ("python3 main.py --project-root openMemristorPDK --pdk-root openMemristorPDK/data/openmemristorpdk gui", True),
        "From the host, ./start_eda_container.sh --gui-memristor runs that same gui command inside the container.",
        "Honest, real output for a genuinely empty deck -- confirming openPDKcreator really does support building up from nothing, not just editing an existing real PDK.",
    ],
)

# 5. PDK Wizard
image_slide(
    "The PDK Wizard's own Analog/Memristor path",
    [],
    f"{FIG}/pdk_wizard.jpg",
    caption="Green = real data present. The wizard forks Digital vs. Analog/Memristor -- this walk follows "
            "Layers -> Magic Tech/DRC -> LEF -> User Models (Verilog-A) -> xschem Symbol/Schematic.",
)

# 6. Layers
text_slide(
    "Layers: a 4-layer memristor stack",
    [
        "Technology -> Layers -> New .lyp File..., then New Layer x4:",
        "BE -- GDS 30/0, drawing -- Bottom electrode metal",
        "MEM -- GDS 31/0, drawing -- Memristive switching oxide",
        "TE -- GDS 32/0, drawing -- Top electrode metal",
        "PRBOUNDARY -- GDS 235/4, marker -- Cell outline, no real geometry",
        "Fictional, illustrative GDS numbers -- a demo stack, not a qualified process. Exported via File -> Export Edited Layers to a real, valid, open_pdks-format KLayout layer file.",
    ],
)

# 7. Magic Tech + DRC Rules
text_slide(
    "Magic Tech + DRC Rules",
    [
        "Magic Tech (Technology -> Magic Tech): New .tech File..., 1 real plane (metal), 3 real types (be, mem, te).",
        "DRC Rules (Technology -> DRC Rules): New DRC Deck..., New Rule -- MEM.W.1: minimum width, 0.1 micron.",
        "Both exported via File -> Save Edits / Export Edited Magic Types / Export Edited DRC Rules.",
    ],
)

# 8. Library Manager: the real payoff
image_slide("Library Manager: the real payoff", [], f"{FIG}/library_manager.jpg")

# 9. Library Manager: what actually happened
text_slide(
    "Library Manager: what actually happened",
    [
        "The real LEF macro is auto-discovered: library openmemristorpdk_pr, cell memristor, 1 view.",
        "Create -> Symbol: a real, valid xschem .sym skeleton at libraries/openmemristorpdk_pr/memristor.sym.",
        "Create -> Verilog-A: \"Created Verilog-A at .../user_models/veriloga/memristor.va with 2 real pin(s) from an existing view.\"",
        "The real pins (BE, TE, both INOUT from the LEF) were pulled straight into the generated module memristor(BE, TE); -- infer_ports_for_cell's LEF -> xschem -> existing-Verilog priority, validated end to end on a brand-new project it had never seen before.",
    ],
)

# 10. The generated Verilog-A model
image_slide("The generated Verilog-A model", [], f"{FIG}/veriloga_model.jpg")

# 11. The physics
text_slide(
    "The physics: HP linear ion-drift memristor",
    [
        "Strukov, Snider, Stewart & Williams, \"The missing memristor found,\" Nature 453, 80-83 (2008).",
        "A thin oxide film of thickness D between two electrodes (BE, TE); one region doped (low resistance Ron), the other undoped (Roff).",
        "State x = w/D in [0,1]: the doped/undoped boundary position.",
        ("dx/dt = (uv * Ron / D^2) * i(t)", True),
        ("Rmem(x) = Ron*x + Roff*(1-x)", True),
        ("v = Rmem(x) * i", True),
        "Textbook linear-drift form -- no window function. The state x is stored on a hidden node that starts at x0 and stops at 0 and 1.",
    ],
)

# 12. Compiling and instantiating it
text_slide(
    "Compiling and instantiating it -- real gotchas found",
    [
        ("openvaf memristor.va --output memristor.osdi   # compiles clean", True),
        "Name collision: ngspice ships its own built-in XSPICE memristor model. A same-named Verilog-A module silently binds to the wrong one and segfaults -- fixed by renaming the simulation-only copy to hp_memristor.",
        "Load order: osdi file.osdi inside a .control block runs after .model cards are parsed -- must be pre-loaded via a .spiceinit in the working directory (IHP's own real convention).",
        "Device letter: OSDI compact models instantiate with the N prefix (n1 te 0 modelname), not XSPICE's a -- confirmed by reverse-engineering a real IHP resistor subcircuit.",
        "Model parameters (ron, roff, ...) belong on the .model card, not the instance line.",
    ],
)

# 13. The real testbench
text_slide(
    "The real testbench",
    [
        (".model mm hp_memristor ron=100 roff=16k d=10n uv=1e-14 x0=0", True),
        ("n1 te 0 mm", True),
        ("vte te 0 dc 0 sin(0 1.0 0.6)", True),
        (".tran 300u 3.34", True),
        "A 1V, 0.6Hz sine drive across the device, 2 real periods, run via:",
        ("bash run_simulation.sh", True),
        ("  [1/3] openvaf hp_memristor.va --output hp_memristor.osdi", True),
        ("  [2/3] ngspice -b mem_tran.sp", True),
        ("  [3/3] python3 plot_memristor.py", True),
    ],
)

# 14. Result
image_slide(
    "Result: the real pinched hysteresis loop",
    [],
    f"{FIG}/memristor_transient.png",
    caption="Real, simulated data (11,145 points) -- the I-V loop pinches exactly at the origin every "
            "half-cycle: at V=0, I=0 always, regardless of history.",
)

# 15. What's real here
text_slide(
    "What's real here",
    [
        "Independent project, own git history",
        "4-layer stack, exported .lyp",
        "Magic tech planes/types",
        "1 DRC rule (unbound layer)",
        "LEF macro, 2 real pins",
        "xschem symbol",
        "Verilog-A model, real physics",
        "Real openvaf compile",
        "Real ngspice transient",
        "See walkthrough_full.tex for the current, complete state.",
    ],
)

# 16. Where everything lives
text_slide(
    "Where everything lives",
    [
        ("openMemristorPDK/", True),
        ("  data/openmemristorpdk/        # the live, editable PDK tree", True),
        ("  export/openmemristorpdk/      # real, open_pdks-format output", True),
        ("  libraries/openmemristorpdk_pr/memristor.sym", True),
        ("  user_models/veriloga/memristor.va   # real physics, real pins", True),
        ("  docs/simulation/", True),
        ("    hp_memristor.va             # renamed copy, for ngspice", True),
        ("    mem_tran.sp  run_simulation.sh  plot_memristor.py", True),
        ("    memristor_transient.png", True),
        ("  saves/openmemristorpdk.yaml   # Magic Types + DRC edits", True),
    ],
)

# 17. Thanks
page = new_page()
f = Frame(stylename=fs_plain, width=f"{PAGE_W-4}cm", height="4cm", x="2cm", y="6cm")
page.addElement(f)
tb = TextBox()
f.addElement(tb)
tb.addElement(P(stylename=st_title, text="Thanks!"))

doc.save(OUT)
print(f"Wrote {OUT}")
