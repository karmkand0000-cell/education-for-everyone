# Detailed chapter files

Each chapter's full study material lives in its own file:

    content/<subject id>/<level>/<chapter id>.json      e.g. content/maths/6/ch1.json

The site loads the file only when a student opens that chapter, so the main
page stays fast however much material is added. If a file is missing, the
chapter page shows its short key points as before.

Every piece of text is bilingual: `{"en": "...", "hi": "..."}`. Lists are
`{"en": [...], "hi": [...]}` with the same number of items in both languages.
Text is plain (no HTML, no Markdown). A newline (`\n`) starts a new line.

```json
{
  "v": 1,
  "sub": "maths", "lv": "6", "id": "ch1",
  "intro": {"en": "...", "hi": "..."},
  "learn": {"en": ["what you will learn", "..."], "hi": ["...", "..."]},
  "sections": [
    {
      "h": {"en": "1.1 What is a pattern?", "hi": "1.1 पैटर्न क्या है?"},
      "blocks": [
        {"p": {"en": "paragraph", "hi": "अनुच्छेद"}},
        {"def": {"term": {"en": "", "hi": ""}, "text": {"en": "", "hi": ""}}},
        {"list": {"en": ["", ""], "hi": ["", ""]}},
        {"formula": {"en": "1 + 3 + 5 + ... + (2n - 1) = n × n", "hi": "..."}},
        {"note": {"en": "remember / tip", "hi": ""}},
        {"table": {"head": {"en": ["", ""], "hi": ["", ""]}, "rows": {"en": [["", ""]], "hi": [["", ""]]}}},
        {"ex": {"q": {"en": "", "hi": ""}, "a": {"en": "step 1\nstep 2", "hi": ""}}}
      ]
    }
  ],
  "mistakes": {"en": ["common mistake and the fix"], "hi": [""]},
  "terms": [{"t": {"en": "", "hi": ""}, "d": {"en": "", "hi": ""}}],
  "exercises": [{"lvl": "easy|medium|hard", "q": {"en": "", "hi": ""}, "a": {"en": "", "hi": ""}}],
  "summary": {"en": [""], "hi": [""]}
}
```

`python3 content/validate.py` checks every file against this shape.
