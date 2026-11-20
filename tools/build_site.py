#!/usr/bin/env python3
"""Собирает site/index.html из site/src/majorka-opt.html: подставляет фото товаров (вырезки из posts/*/photos) как data: URI."""
import base64, io, re, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "site/src/majorka-opt.html"
OUT = ROOT / "site/index.html"

def find_photo(name):
    hits = sorted(ROOT.glob(f"posts/*/photos/{name}.png"))
    if not hits:
        sys.exit(f"нет фото: {name}")
    return hits[-1]

def data_uri(path):
    im = Image.open(path).convert("RGBA")
    im = im.crop(im.getbbox())
    im.thumbnail((260, 260))
    buf = io.BytesIO()
    im.save(buf, "WEBP", quality=82)
    return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()

html = SRC.read_text(encoding="utf-8")
html = re.sub(r"\{\{IMG:([\w-]+)\}\}", lambda m: data_uri(find_photo(m.group(1))), html)
OUT.write_text(html, encoding="utf-8")
print(f"{OUT.relative_to(ROOT)}: {len(html)//1024} КБ")
