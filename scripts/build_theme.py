#!/usr/bin/env python3
"""Build themes/vercel-italics.json from upstream Vercel + Night Owl sources."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "themes" / "vercel-italics.json"

# Optional local paths to upstream repos (sibling forks in this workspace).
VERCEL = ROOT.parent / "zed-vercel-theme" / "themes" / "vercel-theme.json"
NIGHT_OWL = ROOT.parent / "night-owlz" / "themes" / "NightOwl.json"

TOKEN_COLOR_PARENT = {
    "constant.builtin": "constant",
    "diff.minus": "editor.foreground",
    "diff.plus": "editor.foreground",
    "embedded": "editor.foreground",
    "enum": "type",
    "function.method": "function",
    "hint": "comment",
    "keyword.control": "keyword",
    "keyword.declaration": "keyword",
    "namespace": "editor.foreground",
    "predictive": "comment",
    "preproc": "keyword",
    "primary": "editor.foreground",
    "selector": "tag",
    "selector.pseudo": "attribute",
    "type.builtin": "type",
    "variant": "type",
}

# Defining punctuation.* overrides Zed fallback and changes Vercel colors for
# operators, brackets, and delimiters. Leave them undefined.
SKIP_TOKENS = {
    "punctuation",
    "punctuation.bracket",
    "punctuation.delimiter",
    "punctuation.list_marker",
    "punctuation.markup",
    "punctuation.special",
}


def resolve_color(style: dict, syntax: dict, parent_key: str) -> str:
    if parent_key == "editor.foreground":
        return style["editor.foreground"]
    entry = syntax.get(parent_key)
    if entry and entry.get("color"):
        return entry["color"]
    return style["editor.foreground"]


def build(vercel_path: Path, night_owl_path: Path) -> dict:
    vercel = json.loads(vercel_path.read_text())
    night_owl = json.loads(night_owl_path.read_text())
    night_owl_by_name = {theme["name"]: theme for theme in night_owl["themes"]}

    merged = deepcopy(vercel)
    merged["name"] = "Vercel Italics"
    merged["author"] = "Cibi Aananth"

    for theme in merged["themes"]:
        appearance = theme["appearance"]
        theme["name"] = f"Vercel Italics {'Dark' if appearance == 'dark' else 'Light'}"

        no_variant = "Night Owl Dark" if appearance == "dark" else "Night Owl Light"
        no_syntax = night_owl_by_name[no_variant]["style"]["syntax"]
        style = theme["style"]
        vercel_syntax = style["syntax"]

        for token in vercel_syntax:
            if token in no_syntax and no_syntax[token].get("font_style") == "italic":
                vercel_syntax[token]["font_style"] = "italic"

        for token, no_style in no_syntax.items():
            if token in vercel_syntax or token in SKIP_TOKENS:
                continue
            parent = TOKEN_COLOR_PARENT.get(token, "editor.foreground")
            vercel_syntax[token] = {
                "color": resolve_color(style, vercel_syntax, parent),
                "background_color": None,
                "font_style": no_style.get("font_style"),
                "font_weight": no_style.get("font_weight"),
            }

    return merged


def main() -> None:
    if not VERCEL.exists() or not NIGHT_OWL.exists():
        raise SystemExit(
            "Upstream theme sources not found. Expected:\n"
            f"  {VERCEL}\n"
            f"  {NIGHT_OWL}\n"
            "Rebuild from the committed themes/vercel-italics.json instead."
        )

    OUT.write_text(json.dumps(build(VERCEL, NIGHT_OWL), indent=2) + "\n")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
