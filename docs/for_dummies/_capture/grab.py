import sys, json, re, subprocess
from PIL import Image, ImageDraw, ImageGrab
name = sys.argv[1]; marks = json.loads(sys.argv[2]) if len(sys.argv) > 2 else []
img = ImageGrab.grab(xdisplay=":1").convert("RGB")
d = ImageDraw.Draw(img)
for (x0, y0, x1, y1) in marks:
    for k in range(4):
        d.rounded_rectangle((x0-6-k, y0-6-k, x1+6+k, y1+6+k), radius=10, outline=(230, 30, 30))
img.crop((0, 0, 1853, 930)).save(f"/foss/designs/openMemristorPDK/docs/for_dummies/img/{name}.png", optimize=True)
out = subprocess.run(["xwininfo", "-root", "-tree"], capture_output=True, text=True).stdout
for line in out.splitlines():
    if "openPDKcreator" in line: print(line.strip())
