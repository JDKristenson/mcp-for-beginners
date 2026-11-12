"""Render this map's axis-aligned rectangles/text; no app or network execution.

Only Python's standard library is used. Unsupported elements are rejected instead
of silently omitted. Excalidraw font family 2 is the Helvetica/Arial family.
"""
from html import escape
import json
from pathlib import Path


def render(document):
    assert document["type"] == "excalidraw" and document["version"] == 2
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1040 750" role="img" aria-labelledby="title desc">',
             '<title id="title">MCP curriculum reference map</title>',
             '<desc id="desc">Inherited curriculum, learning navigation, license credits and local evidence boundaries. Setup not run.</desc>',
             '<rect width="1040" height="750" fill="#ffffff"/>']
    ids = set()
    for element in document["elements"]:
        assert element["id"] not in ids
        ids.add(element["id"])
        assert not element["isDeleted"] and element["angle"] == 0
        x, y = element["x"], element["y"]
        color = escape(element["strokeColor"], quote=True)
        if element["type"] == "rectangle":
            fill = escape(element["backgroundColor"], quote=True)
            parts.append(f'<rect id="{element["id"]}" x="{x}" y="{y}" width="{element["width"]}" height="{element["height"]}" fill="{fill}" stroke="{color}"/>')
        elif element["type"] == "text":
            assert element["fontFamily"] == 2 and element["textAlign"] == "left"
            size = element["fontSize"]
            parts.append(f'<text id="{element["id"]}" x="{x}" y="{y}" fill="{color}" font-family="Helvetica, Arial, sans-serif" font-size="{size}">')
            for index, line in enumerate(element["text"].splitlines()):
                baseline = y + size + index * size * element["lineHeight"]
                parts.append(f'<tspan x="{x}" y="{baseline}">{escape(line)}</tspan>')
            parts.append('</text>')
        else:
            raise ValueError(f'Unsupported element type: {element["type"]}')
    parts.append('</svg>')
    return '\n'.join(parts) + '\n'


if __name__ == "__main__":
    directory = Path(__file__).resolve().parent
    source = json.loads((directory / "curriculum-map.excalidraw").read_text())
    (directory / "curriculum-map.svg").write_text(render(source))
