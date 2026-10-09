"""Resize and compress the supplied images to web-ready JPGs, and print their MD5s for upload."""
import hashlib
from pathlib import Path
from PIL import Image

SRC = Path(r"C:/Users/mrkau/Downloads")
OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

# source number -> (output name, max width, max height)
PLAN = {
    1: ("stellaspire-gcc-hiring-team.jpg", 1600, 1000),
    2: ("stellaspire-cfo-executive-search.jpg", 1000, 1250),
    3: ("stellaspire-finance-accounting-recruitment.jpg", 1600, 1000),
    4: ("stellaspire-analytics-data-team.jpg", 1600, 1000),
    5: ("stellaspire-diversity-hiring-team.jpg", 1600, 1000),
    6: ("stellaspire-women-returnship.jpg", 1000, 1250),
    7: ("blog-recruitment-agency-fees-india.jpg", 1600, 840),
    8: ("blog-gcc-hiring-guide-india.jpg", 1600, 840),
    9: ("blog-cfo-hiring-process.jpg", 1600, 840),
    10: ("blog-retained-vs-contingency-search.jpg", 1600, 840),
}

for n, (name, w, h) in PLAN.items():
    src = next(SRC.glob(f"ChatGPT Image Oct 7, 2026, 12_0*PM-{n}.png"))
    im = Image.open(src).convert("RGB")
    im.thumbnail((w, h), Image.LANCZOS)
    dest = OUT / name
    im.save(dest, "JPEG", quality=80, optimize=True, progressive=True)
    md5 = hashlib.md5(dest.read_bytes()).hexdigest()
    print(f"{n:>2} {name:48} {im.size[0]}x{im.size[1]} {dest.stat().st_size // 1024:>4} KB {md5}")
