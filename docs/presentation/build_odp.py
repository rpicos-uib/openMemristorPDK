#!/usr/bin/env python3
"""Builds a real .odp presentation -- 'openMemristorPDK: layout,
extraction, LVS, DRC and simulation, step by step' -- directly from
the real, already-verified content and real, already-captured
screenshots in docs/presentation/digital_aspects.tex (the real
memristor_tio2_au build walkthrough), not fabricated or re-guessed."""

from odf.opendocument import OpenDocumentPresentation
from odf.style import (
    Style, MasterPage, PageLayout, PageLayoutProperties,
    TextProperties, GraphicProperties, ParagraphProperties, DrawingPageProperties,
)
from odf.draw import Page, Frame, TextBox, Image
from odf.text import P, List, ListItem

import os

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, "figures")
OUT = os.path.join(HERE, "memristor_walkthrough.odp")

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
def pstyle(name, size, bold=False, color="#1a1a1a", align=None):
    s = Style(name=name, family="paragraph")
    tp_kwargs = dict(fontsize=size, fontweight="bold" if bold else "normal", color=color)
    s.addElement(TextProperties(**tp_kwargs))
    pp_kwargs = {}
    if align:
        pp_kwargs["textalign"] = align
    if pp_kwargs:
        s.addElement(ParagraphProperties(**pp_kwargs))
    doc.automaticstyles.addElement(s)
    return s

st_title = pstyle("STTitle", "32pt", bold=True, color="#1b3a6b")
st_subtitle = pstyle("STSubtitle", "18pt", bold=False, color="#444444")
st_heading = pstyle("STHeading", "24pt", bold=True, color="#1b3a6b")
st_body = pstyle("STBody", "15pt", bold=False, color="#222222")
st_caption = pstyle("STCaption", "12pt", bold=False, color="#555555")
st_footer = pstyle("STFooter", "10pt", bold=False, color="#888888")

def frame_style(name, **graphic_kwargs):
    s = Style(name=name, family="graphic")
    s.addElement(GraphicProperties(**graphic_kwargs))
    doc.automaticstyles.addElement(s)
    return s

fs_plain = frame_style("FSPlain", stroke="none", fill="none")

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


def add_bullets(page, bullets, x=1.0, y=3.2, w=PAGE_W - 2, h=10.0, style=st_body):
    f = Frame(stylename=fs_plain, width=f"{w}cm", height=f"{h}cm", x=f"{x}cm", y=f"{y}cm")
    page.addElement(f)
    tb = TextBox()
    f.addElement(tb)
    for b in bullets:
        tb.addElement(P(stylename=style, text=("•  " + b)))
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
    tb.addElement(P(stylename=st_title, text="openMemristorPDK"))
    tb.addElement(P(stylename=st_heading, text="Layout, Extraction, LVS, DRC and Simulation"))
    tb.addElement(P(stylename=st_subtitle, text="A real, step-by-step walkthrough -- memristor_tio2_au, built and verified end to end with OpenPDKCreator"))
    tb.addElement(P(stylename=st_subtitle, text=""))
    tb.addElement(P(stylename=st_subtitle, text="R. Picos · rpicos.uib@gmail.com / rodrigo.picos@uib.es"))
    tb.addElement(P(stylename=st_subtitle, text="Project PID2025-170062NB (MemFRAME) funded by MICIU/AEI/10.13039/501100011033"))
    add_image(page, os.path.join(HERE, "figures", "miciu_aei.png"), 2, 12.2, 11, 2.7)
    return page


def step_slide(heading, bullets, images, caption=None):
    """images: list of (path, ) placed side by side, equally sized."""
    page = new_page(heading)
    n = len(images)
    if bullets:
        add_bullets(page, bullets, y=3.0, h=3.0 if images else 10.5)
        img_y = 6.3
        img_h = PAGE_H - img_y - 1.3
    else:
        img_y = 3.2
        img_h = PAGE_H - img_y - 1.3
    if n:
        gap = 0.4
        total_w = PAGE_W - 2 - gap * (n - 1)
        w_each = total_w / n
        for i, path in enumerate(images):
            x = 1 + i * (w_each + gap)
            add_image(page, path, x, img_y, w_each, img_h)
    if caption:
        f = Frame(stylename=fs_plain, width=f"{PAGE_W-2}cm", height="0.8cm",
                  x="1cm", y=f"{PAGE_H-1.1}cm")
        page.addElement(f)
        tb = TextBox()
        f.addElement(tb)
        tb.addElement(P(stylename=st_caption, text=caption))
    return page


# =====================================================================
# 1. Title
title_slide()

# 2. Overview
step_slide(
    "What this walkthrough builds",
    [
        "A memristor is a real, two-terminal, purely resistive element -- no clock, no digital logic of its own.",
        "This guide builds every real view OpenPDKCreator can hold for one cell, memristor_tio2_au: Verilog, CDL, SPICE, Liberty, a real Magic layout, an extracted netlist, LVS, DRC, and a real ngspice simulation.",
        "Every screenshot in this deck is a real, live capture of OpenPDKCreator and the real EDA tools it drives (Magic, Netgen, KLayout, ngspice/OpenVAF) -- nothing staged or mocked up.",
    ],
    [],
)

# 3. Step 1 -- select the cell
step_slide(
    "Step 1 -- Select the real cell",
    [
        "Library Manager -> library openmemristorpdk_pr -> cell memristor_tio2_au.",
        "It already carries real LEF, Verilog-A and xschem symbol/schematic views from an earlier pass -- every view added below is added to this same real cell.",
    ],
    [f"{FIG}/memristor_step1_cell_selected.png"],
    caption="Real, live Library Manager: Schematic/Symbol already real, everything else still (absent) with Create/Add... buttons.",
)

# 4. Step 2 -- Verilog view
step_slide(
    "Step 2 -- Create the Verilog view",
    [
        "Library Manager, memristor_tio2_au row: Create next to Verilog.",
        "Writes user_models/verilog/memristor_tio2_au.v -- a real module memristor_tio2_au(BE, TE); with both ports inout.",
        "The real port list comes straight from the LEF macro's own BE/TE pins, the same inference path every other view uses.",
    ],
    [f"{FIG}/memristor_step2_create_verilog.png"],
    caption="Real, live Library Manager right after Create -- the row now shows (real) with the real path and inferred pin count.",
)

# 5. Steps 3-4 -- CDL and SPICE views (text only, no screenshot in the source deck)
step_slide(
    "Steps 3-4 -- Create the CDL and SPICE views",
    [
        "Create next to CDL writes a real, valid, empty subcircuit: .SUBCKT memristor_tio2_au BE TE ... .ENDS.",
        "Create next to SPICE writes the same shape in real SPICE subckt syntax.",
        "Both exist so a real external LVS/netlisting flow has something to bind the cell name to -- the device's actual electrical behavior stays in the Verilog-A model and LEF macro, the project's single source of truth for it.",
    ],
    [],
)

# 6. Step 5 -- Liberty view
step_slide(
    "Step 5 -- Create the Liberty view",
    [
        "Create next to Liberty writes a real .lib skeleton: library/cell memristor_tio2_au, pins BE and TE, both direction inout.",
    ],
    [f"{FIG}/memristor_step5_create_liberty.png"],
    caption="Real, live Library Manager after Create next to Liberty -- Verilog/Verilog-A/CDL/SPICE/Liberty all real now.",
)

# 7. Step 6 -- Magic Tech planes/types
step_slide(
    "Step 6 -- Set up Magic Tech: planes and types",
    [
        "Technology -> Magic Tech -> Planes/Types sub-tabs.",
        "3 real planes (botmetal/oxide/topmetal); each of 6 device types reassigned to its own real plane -- the real prerequisite for drawing a true, physically-stacked device. (A seventh type, via1 on botmetal, was added later with the via fix.)",
    ],
    [f"{FIG}/memristor_step6_planes.png", f"{FIG}/memristor_step6_types.png"],
    caption="Left: Planes sub-tab (planes:3 types:6). Right: Types sub-tab, each type on its own real plane.",
)

# 8. Step 7 -- draw the real layout
step_slide(
    "Step 7 -- Draw the real, physically-stacked layout",
    [
        "Open in Magic, launched already pointed at this cell's real .mag file with an explicit tech load.",
        "Three overlapping boxes, one real type per plane, at the true 0.5 lambda (= 1 micron) footprint: be_au, then mem_tio2, then te_au, each labeled and ported.",
        "A real Magic quirk: label without an explicit layer infers one from whatever is topmost -- with three overlapping types, the explicit layer argument is what puts each label on the intended one.",
    ],
    [f"{FIG}/memristor_step7_magic_layout.png"],
    caption="Real, live Magic: real layer swatches, a real green DRC-clean indicator, editing the real, physically-stacked cell.",
)

# 9. Step 8 -- Connect/Extract device recognition
step_slide(
    "Step 8 -- Connect/Extract: real device recognition",
    [
        "Technology -> Magic Tech -> Styles/Connect/Extract sub-tabs: 6 new styles, 4 connect rules (self-only), 3 plane orders, 4 resist entries.",
        "3 New Device rows (class subcircuit) turn a real BE/oxide/TE overlap into a recognized 2-terminal device during extraction -- one per real top-electrode metal (memristor_tio2_au_prim, _ti_prim, _hfo2_al_prim).",
        "No connect rule joins be_au to any te_* directly -- BE and TE stay two distinct extraction nodes, connected only through the real device.",
    ],
    [f"{FIG}/memristor_step8a_styles.png", f"{FIG}/memristor_step8b_connect.png", f"{FIG}/memristor_step8c_devices.png"],
    caption="Left to right: Styles, Connect, and Extract Devices -- each row a real, individually-added entry.",
)

# 10. Step 9 -- Extract to SPICE
step_slide(
    "Step 9 -- Extract to SPICE",
    [
        "Library Manager, Magic Layout row: Extract to SPICE -> Parasitic (for ngspice simulation).",
        "Runs a real, freshly-generated Magic batch script (extract all + ext2spice).",
        "Real result: .subckt memristor_tio2_au BE TE / X0 BE TE memristor_tio2_au_prim / .ends -- Step 8's device-recognition rule fired, a real recognized instance, not two disconnected ports.",
    ],
    [f"{FIG}/memristor_step9_extract_dialog.png"],
    caption="The real Extract to SPICE result dialog -- Magic's own stdout, shown verbatim.",
)

# 11. Step 10 -- Run LVS
step_slide(
    "Step 10 -- Run LVS",
    [
        "The CDL view from Step 3 is filled in with a matching real device call: X1 BE TE memristor_tio2_au_prim.",
        "Run LVS: a real, fast LVS-preset extraction followed by a real Netgen batch run.",
        "Real result: Number of devices: 1 | 1, Netlists match uniquely, Final result: Circuits match uniquely -- a genuine, device-level pass, not just a pin-list check.",
    ],
    [f"{FIG}/memristor_step10_lvs_dialog.png"],
    caption="The real Run LVS result dialog -- Netgen's own stdout, ending in Circuits match uniquely.",
)

# 12. Step 11 -- Run DRC
step_slide(
    "Step 11 -- Run DRC",
    [
        "Same row, Run DRC: a real Magic GDS export (BE_Au/TE_Au drawing layers), then a real, batch KLayout DRC run against the project's own custom_rules.drc deck.",
        "Real result: an empty <items> list -- 0 violations, a clean pass against all 4 real rules on the real, physically-stacked layout.",
    ],
    [f"{FIG}/memristor_step11_drc_dialog.png"],
    caption="The real Run DRC result dialog -- KLayout's own stdout plus the real, freshly-written report database.",
)

# 13. Step 12 -- simulate the extracted netlist
step_slide(
    "Step 12 -- Simulate the real extracted netlist",
    [
        "A real ngspice transient driven through the real extracted netlist itself, not a bare .model/instance line: X0 resolves to a real wrapper around the OpenVAF-compiled OSDI model.",
        "Real ngspice requirement: implicit .osdi auto-load only works with no .subckt anywhere in the deck -- fixed with an explicit pre_osdi <file>.osdi inside a leading .control block.",
        "Result: overlaid against the original, hand-written testbench's own real transient -- 0.0000% relative current difference, every sample.",
    ],
    [f"{FIG}/memristor_tio2_au_extracted_comparison.png"],
    caption="The real, Magic-extracted, device-recognized layout netlist reproduces the exact same real pinched hysteresis loop.",
)

# 14. Step 13 -- confirm all views
step_slide(
    "Step 13 -- Confirm all real views",
    [
        "Library Manager, memristor_tio2_au now lists 10 real views: LEF, Verilog-A, xschem symbol, xschem schematic, Verilog, CDL, SPICE, Liberty, Magic Layout, and the real GDS from Step 11.",
        "Every one auto-discoverable again from a fresh GUI relaunch, all agreeing on the same real BE/TE port list.",
    ],
    [f"{FIG}/memristor_step13_final_views.png"],
    caption="The real, live Library Manager after every step in this walkthrough.",
)

# 15. Closing
step_slide(
    "Where to find everything",
    [
        "Project: openMemristorPDK (github.com/rpicos-uib/openMemristorPDK).",
        "The real device: libraries/openmemristorpdk_pr/memristor_tio2_au.{mag,cdl,spice,lib} + user_models/verilog(-a)/memristor_tio2_au.*",
        "The real simulation: docs/simulation/memristor_tio2_au/ (mem_tran.sp, run_simulation.sh) and .../memristor_tio2_au_layout_extracted/ (the extracted-netlist comparison shown in Step 12).",
        "Full source deck for this walkthrough: docs/presentation/digital_aspects.tex.",
    ],
    [],
)

doc.save(OUT)
print(f"Wrote {OUT}")
