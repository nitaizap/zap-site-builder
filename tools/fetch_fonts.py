"""One-off: vendor Hebrew-capable Google Fonts (OFL) into the theme as woff2 + one CSS file per family.

Run again only to add a family:  py tools/fetch_fonts.py
"""
import re
import urllib.request
from pathlib import Path

DEST = Path(__file__).resolve().parent.parent / "wp" / "theme" / "zap-base" / "fonts"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36"

# family -> css2 axis spec. Variable where Google serves one file per subset.
FAMILIES = {
    "Heebo": "wght@300..800",
    "Assistant": "wght@300..800",
    "Rubik": "wght@300..800",
    "Noto Sans Hebrew": "wght@300..800",
    "IBM Plex Sans Hebrew": "wght@300;400;500;600;700",
    "Frank Ruhl Libre": "wght@300..900",
    "Noto Serif Hebrew": "wght@300..800",
    "Secular One": "",
    "Suez One": "",
    "Varela Round": "",
    "Fredoka": "wght@300..700",
}
KEEP = {"hebrew", "latin"}


def get(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    return data if binary else data.decode()


def main():
    for fam, axes in FAMILIES.items():
        slug = fam.lower().replace(" ", "-")
        q = fam.replace(" ", "+") + (":" + axes if axes else "")
        css = get(f"https://fonts.googleapis.com/css2?family={q}&display=swap")
        out, n = [], 0
        for subset, block in re.findall(r"/\*\s*([\w-]+)\s*\*/\s*(@font-face\s*{[^}]+})", css):
            if subset not in KEEP:
                continue
            url = re.search(r"url\((https://[^)]+\.woff2)\)", block).group(1)
            weight = re.search(r"font-weight:\s*([^;]+);", block).group(1).strip().replace(" ", "-")
            name = f"{slug}-{subset}-{weight}.woff2"
            (DEST / slug).mkdir(parents=True, exist_ok=True)
            p = DEST / slug / name
            if not p.exists():
                p.write_bytes(get(url, binary=True))
            out.append(block.replace(url, f"{slug}/{name}"))
            n += 1
        (DEST / f"{slug}.css").write_text("\n".join(out) + "\n", encoding="utf-8")
        print(f"{fam}: {n} faces")


if __name__ == "__main__":
    main()
