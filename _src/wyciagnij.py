# Wyciąga tekst Tomu I z PDF-a do _src/tom1.json (akapity po wcięciu pierwszej linii)
import json, re, sys
from pathlib import Path
import pypdf

PDF = Path(r"C:\Users\kluch\Downloads\Stare Male Dziecko Tom_I.pdf")
r = pypdf.PdfReader(str(PDF))
lines = []  # (x, text) w kolejności czytania
for i, page in enumerate(r.pages):
    frags = []
    def v(text, cm, tm, fd, fs):
        if text.strip():
            frags.append((tm[5], tm[4], text))
    page.extract_text(visitor_text=v)
    rows = {}
    for y, x, t in frags:
        if y > 540 or y < 50:  # nagłówek strony i numer strony
            continue
        key = round(y)
        rows.setdefault(key, []).append((x, t))
    for y in sorted(rows, reverse=True):
        parts = sorted(rows[y])
        txt = " ".join(t.strip() for _, t in parts)
        lines.append((parts[0][0], re.sub(r"\s+", " ", txt).strip(), i))

# dzielimy na sekcje po nagłówkach
secs = []
cur = None
i = 0
while i < len(lines):
    x, t, pg = lines[i]
    if t in ("P R O L O G", "E P I L O G") or t.startswith("R O Z D Z I A Ł"):
        label = t.replace(" ", "").replace("ROZDZIAŁ", "Rozdział ").title() if not t.startswith("R O Z") else "Rozdział " + t.split("Ł", 1)[1].replace(" ", "")
        if t == "P R O L O G": label = "Prolog"
        if t == "E P I L O G": label = "Epilog"
        title = lines[i + 1][1]
        cur = {"label": label, "title": title, "paras": []}
        secs.append(cur)
        i += 2
        if i < len(lines) and "⁂" in lines[i][1]:
            i += 1
        continue
    if t.startswith("C Z Ę Ś Ć") or t in ("CISZA", "TRZY GŁOSY", "NIEBO"):
        i += 1; continue
    if cur is None or t.startswith("Stare małe Dziecko") and cur["label"] == "Epilog" and "Tom I" in t:
        if cur and cur["label"] == "Epilog": break
        i += 1; continue
    if t.startswith("(Ostatnia strona"):
        break
    new_par = x > 55 or t.startswith("—") or not cur["paras"]
    if new_par:
        cur["paras"].append(t)
    else:
        prev = cur["paras"][-1]
        if prev.endswith("-") and not prev.endswith(" -"):
            cur["paras"][-1] = prev + t
        else:
            cur["paras"][-1] = prev + " " + t
    i += 1

for s in secs:
    s["paras"] = [re.sub(r"\s+([,.;:!?])", r"\1", p) for p in s["paras"]]
secs[-1]["paras"] = [p for p in secs[-1]["paras"] if not p.startswith(("Stare małe Dziecko", "Tom I ·"))]
Path(__file__).with_name("tom1.json").write_text(json.dumps(secs, ensure_ascii=False, indent=1), encoding="utf-8")
for s in secs:
    print(s["label"], "|", s["title"], "|", len(s["paras"]), "akapitów")
