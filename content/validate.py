#!/usr/bin/env python3
"""Check every detailed chapter file in content/ against SCHEMA.md.

Usage: python3 content/validate.py [file ...]
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
BLOCKS = {"p", "def", "list", "formula", "note", "table", "ex"}


def bi(x, where, errs, empty_ok=False):
    if not isinstance(x, dict) or set(x) != {"en", "hi"}:
        errs.append(f"{where}: needs exactly en and hi")
        return
    for k in ("en", "hi"):
        if not isinstance(x[k], str):
            errs.append(f"{where}.{k}: must be text")
        elif not empty_ok and not x[k].strip():
            errs.append(f"{where}.{k}: empty")


def bilist(x, where, errs):
    if not isinstance(x, dict) or set(x) != {"en", "hi"}:
        errs.append(f"{where}: needs exactly en and hi lists")
        return
    if not all(isinstance(x[k], list) for k in ("en", "hi")):
        errs.append(f"{where}: en and hi must be lists")
        return
    if len(x["en"]) != len(x["hi"]):
        errs.append(f"{where}: en has {len(x['en'])} items, hi has {len(x['hi'])}")
    for k in ("en", "hi"):
        for i, item in enumerate(x[k]):
            if not isinstance(item, str) or not item.strip():
                errs.append(f"{where}.{k}[{i}]: empty or not text")


def check(path):
    errs = []
    try:
        d = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        return [f"not valid JSON: {e}"], 0
    rel = path.relative_to(ROOT).parts
    if d.get("v") != 1:
        errs.append("v must be 1")
    if (d.get("sub"), d.get("lv"), d.get("id") + ".json" if d.get("id") else None) != rel:
        errs.append(f"sub/lv/id {d.get('sub')}/{d.get('lv')}/{d.get('id')} do not match path {'/'.join(rel)}")
    bi(d.get("intro"), "intro", errs)
    bilist(d.get("learn"), "learn", errs)
    secs = d.get("sections")
    if not isinstance(secs, list) or not secs:
        errs.append("sections: must be a non-empty list")
        secs = []
    for si, s in enumerate(secs):
        w = f"sections[{si}]"
        bi(s.get("h"), w + ".h", errs)
        blocks = s.get("blocks")
        if not isinstance(blocks, list) or not blocks:
            errs.append(w + ".blocks: must be a non-empty list")
            continue
        for bi_, b in enumerate(blocks):
            bw = f"{w}.blocks[{bi_}]"
            if not isinstance(b, dict) or len(b) != 1 or next(iter(b)) not in BLOCKS:
                errs.append(f"{bw}: must be one of {sorted(BLOCKS)}")
                continue
            kind, val = next(iter(b.items()))
            if kind in ("p", "formula", "note"):
                bi(val, f"{bw}.{kind}", errs)
            elif kind == "list":
                bilist(val, bw + ".list", errs)
            elif kind == "def":
                bi(val.get("term"), bw + ".def.term", errs)
                bi(val.get("text"), bw + ".def.text", errs)
            elif kind == "ex":
                bi(val.get("q"), bw + ".ex.q", errs)
                bi(val.get("a"), bw + ".ex.a", errs)
            elif kind == "table":
                bilist(val.get("head"), bw + ".table.head", errs)
                rows = val.get("rows")
                if not isinstance(rows, dict) or set(rows) != {"en", "hi"}:
                    errs.append(bw + ".table.rows: needs en and hi")
                else:
                    if len(rows["en"]) != len(rows["hi"]):
                        errs.append(bw + ".table.rows: en and hi row counts differ")
                    n = len(val.get("head", {}).get("en", []))
                    for k in ("en", "hi"):
                        for ri, r in enumerate(rows[k]):
                            if not isinstance(r, list) or len(r) != n:
                                errs.append(f"{bw}.table.rows.{k}[{ri}]: needs {n} cells")
    bilist(d.get("mistakes"), "mistakes", errs)
    bilist(d.get("summary"), "summary", errs)
    for ti, t in enumerate(d.get("terms") or []):
        bi(t.get("t"), f"terms[{ti}].t", errs)
        bi(t.get("d"), f"terms[{ti}].d", errs)
    exs = d.get("exercises")
    if not isinstance(exs, list) or not exs:
        errs.append("exercises: must be a non-empty list")
        exs = []
    for ei, e in enumerate(exs):
        if e.get("lvl") not in ("easy", "medium", "hard"):
            errs.append(f"exercises[{ei}].lvl: must be easy, medium or hard")
        bi(e.get("q"), f"exercises[{ei}].q", errs)
        bi(e.get("a"), f"exercises[{ei}].a", errs)
    words = len(json.dumps([d.get("intro"), secs], ensure_ascii=False).split())
    return errs, words


def main():
    files = [pathlib.Path(f).resolve() for f in sys.argv[1:]] or sorted(ROOT.glob("*/*/*.json"))
    bad = 0
    for f in files:
        errs, words = check(f)
        print(f"{'OK  ' if not errs else 'FAIL'} {f.relative_to(ROOT)}  (~{words} words)")
        for e in errs[:30]:
            print("     -", e)
        bad += bool(errs)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
