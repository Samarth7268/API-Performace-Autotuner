import re

def extract_hotspots(svg_path, top_k=10):
    hotspots = {}

    with open(svg_path, "r", encoding="utf-8") as f:
        content = f.read()

    functions = re.findall(r'function="([^"]+)"', content)

    for fn in functions:
        hotspots[fn] = hotspots.get(fn, 0) + 1

    sorted_hotspots = dict(
        sorted(hotspots.items(), key=lambda x: x[1], reverse=True)
    )

    return dict(list(sorted_hotspots.items())[:top_k])
