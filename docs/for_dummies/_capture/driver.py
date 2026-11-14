"""Screenshot driver for the "for dummies" guide.

Runs the real openPDKcreator GUI (same App main.py gui builds) inside
the IIC-OSIC-TOOLS container on display :1, and executes small Python
command files dropped into /tmp/drv/cmd.py. Clicks/keys go through
the X server via XTest -- real input, not widget.invoke() -- so every
screenshot shows the real application reacting to a real click.

    podman exec -d -e DISPLAY=:1 -w /foss/designs/openMemristorPDK <ctr> \
        bash -lc 'exec python3 docs/for_dummies/_capture/driver.py'
"""

from __future__ import annotations

import ctypes
import io
import json
import os
import sys
import time
import traceback
from contextlib import redirect_stdout
from pathlib import Path

PROJECT = Path("/foss/designs/openMemristorPDK")
OUT = PROJECT / "docs" / "for_dummies" / "img"
DRV = Path("/tmp/drv")
os.chdir(PROJECT)
sys.path.insert(0, str(PROJECT))

import tkinter as tk  # noqa: E402
from tkinter import ttk  # noqa: E402

from PIL import Image, ImageDraw, ImageFont, ImageGrab  # noqa: E402

# ---------------------------------------------------------------- XTest
_x11 = ctypes.cdll.LoadLibrary("libX11.so.6")
_xtst = ctypes.cdll.LoadLibrary("libXtst.so.6")
_x11.XOpenDisplay.restype = ctypes.c_void_p
_x11.XStringToKeysym.restype = ctypes.c_ulong
_x11.XKeysymToKeycode.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
for fn in ("XTestFakeMotionEvent", "XTestFakeButtonEvent", "XTestFakeKeyEvent"):
    getattr(_xtst, fn).argtypes = None
_dpy = _x11.XOpenDisplay(os.environ.get("DISPLAY", ":1").encode())
_x11.XFlush.argtypes = [ctypes.c_void_p]


def _flush():
    _x11.XFlush(ctypes.c_void_p(_dpy))


def move(x, y):
    _xtst.XTestFakeMotionEvent(ctypes.c_void_p(_dpy), -1, int(x), int(y), 0)
    _flush()


def click(x, y, button=1, double=False):
    move(x, y)
    time.sleep(0.08)
    for _ in range(2 if double else 1):
        _xtst.XTestFakeButtonEvent(ctypes.c_void_p(_dpy), button, True, 0)
        _xtst.XTestFakeButtonEvent(ctypes.c_void_p(_dpy), button, False, 0)
        _flush()
        time.sleep(0.06)


def _keycode(name):
    return _x11.XKeysymToKeycode(ctypes.c_void_p(_dpy), _x11.XStringToKeysym(name.encode()))


def key(name, shift=False):
    sh = _keycode("Shift_L")
    if shift:
        _xtst.XTestFakeKeyEvent(ctypes.c_void_p(_dpy), sh, True, 0)
    kc = _keycode(name)
    _xtst.XTestFakeKeyEvent(ctypes.c_void_p(_dpy), kc, True, 0)
    _xtst.XTestFakeKeyEvent(ctypes.c_void_p(_dpy), kc, False, 0)
    if shift:
        _xtst.XTestFakeKeyEvent(ctypes.c_void_p(_dpy), sh, False, 0)
    _flush()
    time.sleep(0.02)


# ------------------------------------------------------------ widgets
def walk(w=None):
    w = w or root
    yield w
    for c in w.winfo_children():
        yield from walk(c)


def find(text, cls=None, visible=True):
    """First widget whose 'text' option equals *text*."""
    for w in walk():
        try:
            if w.cget("text") != text:
                continue
        except tk.TclError:
            continue
        if cls and w.winfo_class() != cls:
            continue
        if visible and not w.winfo_ismapped():
            continue
        return w
    raise LookupError(text)


def center(w):
    w.update_idletasks()
    return w.winfo_rootx() + w.winfo_width() // 2, w.winfo_rooty() + w.winfo_height() // 2


def box(w, pad=4):
    w.update_idletasks()
    x, y = w.winfo_rootx(), w.winfo_rooty()
    return (x - pad, y - pad, x + w.winfo_width() + pad, y + w.winfo_height() + pad)


def tab_box(nb, label):
    """Screen box of a ttk.Notebook tab, found by scanning the tab strip."""
    nb.update_idletasks()
    labels = [nb.tab(t, "text") for t in nb.tabs()]
    want = labels.index(label)
    xs = []
    for y in range(2, 40, 3):
        for x in range(0, nb.winfo_width(), 2):
            if nb.tk.call(nb._w, "identify", "tab", x, y) == want:
                xs.append((x, y))
    if not xs:
        raise LookupError(label)
    x0 = min(p[0] for p in xs); x1 = max(p[0] for p in xs)
    y0 = min(p[1] for p in xs); y1 = max(p[1] for p in xs)
    rx, ry = nb.winfo_rootx(), nb.winfo_rooty()
    return (rx + x0 - 2, ry + y0 - 2, rx + x1 + 2, ry + y1 + 2)


def notebooks():
    return [w for w in walk() if isinstance(w, ttk.Notebook) and w.winfo_ismapped()]


def nb_with(label):
    for nb in notebooks():
        if label in [nb.tab(t, "text") for t in nb.tabs()]:
            return nb
    raise LookupError(label)


def click_tab(label):
    b = tab_box(nb_with(label), label)
    click((b[0] + b[2]) // 2, (b[1] + b[3]) // 2)
    return b


def click_widget(w, double=False):
    x, y = center(w)
    click(x, y, double=double)
    return box(w)


def tree_row_box(tree, iid):
    tree.see(iid)
    tree.update_idletasks()
    bb = tree.bbox(iid)
    if not bb:
        raise LookupError(iid)
    x, y, w, h = bb
    rx, ry = tree.winfo_rootx(), tree.winfo_rooty()
    return (rx + x, ry + y, rx + x + w, ry + y + h)


# --------------------------------------------------------- screenshots
try:
    FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
except OSError:
    FONT = ImageFont.load_default()

SHOTS = OUT / "shots.json"


def shot(name, marks=(), crop=None, note=""):
    """Grab display :1, draw numbered red circles around *marks* (screen
    boxes), crop to *crop* (a screen box, default: the app window),
    save OUT/<name>.png, and record it in shots.json."""
    OUT.mkdir(parents=True, exist_ok=True)
    root.update()
    time.sleep(0.3)
    img = ImageGrab.grab(xdisplay=os.environ.get("DISPLAY", ":1")).convert("RGB")
    draw = ImageDraw.Draw(img)
    for i, m in enumerate(marks, 1):
        x0, y0, x1, y1 = m
        pad = 6
        for k in range(4):
            draw.rounded_rectangle((x0 - pad - k, y0 - pad - k, x1 + pad + k, y1 + pad + k), radius=10, outline=(230, 30, 30))
        if len(marks) > 1:
            cx, cy = x0 - pad - 4, y0 - pad - 4
            draw.ellipse((cx - 16, cy - 16, cx + 16, cy + 16), fill=(230, 30, 30))
            draw.text((cx, cy), str(i), fill="white", font=FONT, anchor="mm")
    if crop is None:
        crop = (root.winfo_rootx() - 2, root.winfo_rooty() - 2,
                root.winfo_rootx() + root.winfo_width() + 2, root.winfo_rooty() + root.winfo_height() + 2)
    if crop != "full":
        img = img.crop(tuple(max(0, int(v)) for v in crop))
    img.save(OUT / f"{name}.png", optimize=True)
    data = json.loads(SHOTS.read_text()) if SHOTS.exists() else {}
    data[name] = {"note": note, "size": img.size}
    SHOTS.write_text(json.dumps(data, indent=1))
    return img.size


def windows():
    """Top-level X windows (name, x, y, w, h) via xwininfo."""
    import re
    import subprocess
    out = subprocess.run(["xwininfo", "-root", "-tree"], capture_output=True, text=True).stdout
    res = []
    for line in out.splitlines():
        m = re.search(r'0x[0-9a-f]+ "([^"]*)".*?(\d+)x(\d+)\+-?\d+\+-?\d+\s+\+(-?\d+)\+(-?\d+)', line)
        if m and int(m.group(2)) > 50:
            res.append((m.group(1), int(m.group(4)), int(m.group(5)), int(m.group(2)), int(m.group(3))))
    return res


# ---------------------------------------------------------- the app
from openpdkcreator.gui.app import App  # noqa: E402

root = tk.Tk()
app = App(root, Path("data/openmemristorpdk"))
root.geometry("1400x860+40+30")

DRV.mkdir(exist_ok=True)
ENV = {k: v for k, v in globals().items()}


def poll():
    # Reschedule first: a command may click something that opens a
    # modal dialog (wait_window runs a nested event loop and never
    # returns until the dialog closes), and the next command -- the
    # one that closes it -- must still be picked up from inside there.
    root.after(150, poll)
    cmd = DRV / "cmd.py"
    if cmd.exists():
        src = cmd.read_text()
        cmd.unlink()
        buf = io.StringIO()
        try:
            with redirect_stdout(buf):
                exec(src, ENV)
        except Exception:
            buf.write(traceback.format_exc())
        (DRV / "out.txt").write_text(buf.getvalue() + "\n<<done>>\n")


root.after(500, poll)
root.mainloop()
