"""Cut placeholder photography out of the client's mood board and export
responsive WebP sizes. Replace with real photography before launch: drop
new source JPEGs into tools/src/photos/<name>.jpg and rerun; files there
take priority over the mood-board crops.

Usage: python3 tools/make_images.py
"""
from pathlib import Path
from PIL import Image, ImageFilter, ImageEnhance

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "site" / "assets" / "img"
BOARD = ROOT / "src" / "moodboard.png"
PHOTOS = ROOT / "src" / "photos"

# Real photos in tools/src/photos/<name>.jpg are used as-is (already cropped);
# originals are kept in tools/src/originals/ with their licence noted in CREDITS.md.
# name: (left, top, right, bottom) on the 1536x1024 mood board
CROPS = {
    "living":    (4, 442, 575, 745),
    "bedroom":   (588, 442, 987, 745),
    "kitchen":   (998, 442, 1532, 745),
    "dining":    (998, 560, 1350, 745),
    "bathroom":  (777, 756, 1165, 1020),
    "terrace":   (316, 230, 760, 430),
}

WIDTHS = [480, 800, 1200, 1600, 2000, 2400]


def load(name):
    p = PHOTOS / f"{name}.jpg"
    if p.exists():
        return Image.open(p).convert("RGB")
    if name not in CROPS:
        raise SystemExit(f"No source for {name}")
    return Image.open(BOARD).convert("RGB").crop(CROPS[name])


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    names = list(CROPS) + [p.stem for p in sorted(PHOTOS.glob("*.jpg")) if p.stem not in CROPS]
    for name in names:
        im = load(name)
        made = []
        real = (PHOTOS / f"{name}.jpg").exists()
        widths = [w for w in WIDTHS if w <= im.width] if real else WIDTHS
        if real and im.width - widths[-1] > 150:
            widths.append(im.width)  # serve the full resolution to high-density screens
        for w in widths:
            # mood-board crops are small; allow up to ~2.2x upscale, then stop
            if not real and (w > im.width * 2.2 and made or w > 1600):
                break
            h = round(im.height * w / im.width)
            r = im.resize((w, h), Image.LANCZOS)
            if w > im.width:
                r = r.filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))
            r.save(OUT / f"{name}-{w}.webp", "WEBP", quality=82 if real else 80, method=6)
            made.append(w)
        # small blurred LQIP colour for backgrounds
        print(name, im.size, "->", made)


if __name__ == "__main__":
    main()
