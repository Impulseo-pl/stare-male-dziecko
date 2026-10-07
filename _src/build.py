"""python _src/build.py -> generuje index.html i podstrony z _src/tom1.json"""
import json, random, re, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
URL = "https://impulseo-pl.github.io/stare-male-dziecko/"
FB = "https://www.facebook.com/profile.php?id=61593939705947"
TOM = json.loads((ROOT / "_src" / "tom1.json").read_text(encoding="utf-8"))
FREE = 3  # Prolog, Rozdział I, Rozdział II
PARTS = [("Część pierwsza", "Cisza", TOM[1:5]), ("Część druga", "Trzy głosy", TOM[5:9]), ("Część trzecia", "Niebo", TOM[9:13])]
ROMAN = {s["label"]: s["label"].replace("Rozdział ", "") for s in TOM}


# ---------- rysunki ----------
def bench(x, y, w, fill="#070b17", hi="#f0b34e", hio=.55):
    p = [f'<rect x="{x+8}" y="{y-38}" width="5" height="40" fill="{fill}"/>',
         f'<rect x="{x+w-13}" y="{y-38}" width="5" height="40" fill="{fill}"/>',
         f'<rect x="{x}" y="{y-36}" width="{w}" height="8" rx="1.5" fill="{fill}"/>',
         f'<rect x="{x}" y="{y-24}" width="{w}" height="8" rx="1.5" fill="{fill}"/>',
         f'<rect x="{x-5}" y="{y}" width="{w+10}" height="8" rx="1.5" fill="{fill}"/>',
         f'<rect x="{x+6}" y="{y+8}" width="6" height="30" fill="{fill}"/>',
         f'<rect x="{x+w-12}" y="{y+8}" width="6" height="30" fill="{fill}"/>',
         f'<rect x="{x}" y="{y-36}" width="{w}" height="1.6" fill="{hi}" opacity="{hio}"/>',
         f'<rect x="{x}" y="{y-24}" width="{w}" height="1.6" fill="{hi}" opacity="{hio*.8}"/>',
         f'<rect x="{x-5}" y="{y}" width="{w+10}" height="1.8" fill="{hi}" opacity="{hio}"/>']
    return "".join(p)


def sparrow(x, y, fill="#070b17"):
    return (f'<g fill="{fill}"><ellipse cx="{x}" cy="{y}" rx="9" ry="6"/><circle cx="{x+8}" cy="{y-5}" r="4.4"/>'
            f'<path d="M{x+12} {y-5} l5 1.5 -5 1z"/><path d="M{x-8} {y-2} l-9 -5 2 7z"/></g>')


def lamp(x, top, bottom, glow_id):
    return (f'<rect x="{x-3}" y="{top+16}" width="6" height="{bottom-top-16}" fill="#070b17"/>'
            f'<rect x="{x-7}" y="{bottom-10}" width="14" height="10" fill="#070b17"/>'
            f'<path d="M{x-13} {top+16} h26 l-5 -18 h-16z" fill="#070b17"/>'
            f'<rect x="{x-9}" y="{top+2}" width="18" height="13" fill="#ffe2a3"/>'
            f'<path d="M{x-10} {top-2} h20 l-10 -7z" fill="#070b17"/>')


def cover(pid="c", cls="cover", label=True):
    rnd = random.Random(3)
    stars = "".join(f'<circle cx="{rnd.randint(24,376)}" cy="{rnd.randint(24,330)}" r="{rnd.choice([.7,.9,1.1,1.4])}" fill="#f4ecdc" opacity="{rnd.choice([.35,.55,.8])}"/>' for _ in range(34))
    t = (f'<svg class="{cls}" viewBox="0 0 400 600" role="img" aria-label="Okładka: Stare małe Dziecko, Tom I, Pusta ławka i Niebo, Philippe Usyk">'
         f'<defs><linearGradient id="{pid}s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#121a33"/><stop offset=".75" stop-color="#25315a"/><stop offset="1" stop-color="#2d3966"/></linearGradient>'
         f'<radialGradient id="{pid}g" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ffd98f" stop-opacity=".55"/><stop offset="1" stop-color="#ffd98f" stop-opacity="0"/></radialGradient></defs>'
         f'<rect width="400" height="600" fill="url(#{pid}s)"/>{stars}'
         f'<rect x="16" y="16" width="368" height="568" fill="none" stroke="#f0b34e" stroke-opacity=".35"/>'
         f'<text x="200" y="74" text-anchor="middle" font-family="Source Sans 3, sans-serif" font-size="15" letter-spacing="4.5" fill="#cfd3e2">PHILIPPE USYK</text>'
         f'<text x="200" y="158" text-anchor="middle" font-family="Literata, Georgia, serif" font-size="50" font-weight="500" fill="#fff">Stare małe</text>'
         f'<text x="200" y="214" text-anchor="middle" font-family="Literata, Georgia, serif" font-size="50" font-weight="500" fill="#fff">Dziecko</text>'
         f'<text x="200" y="252" text-anchor="middle" font-family="Literata, Georgia, serif" font-size="18" fill="#f0b34e">⁂</text>'
         f'<text x="200" y="290" text-anchor="middle" font-family="Source Sans 3, sans-serif" font-size="15" letter-spacing="3" fill="#f7cf86">TOM I</text>'
         f'<text x="200" y="322" text-anchor="middle" font-family="Literata, Georgia, serif" font-style="italic" font-size="24" fill="#f4ecdc">Pusta ławka i Niebo</text>'
         f'<circle cx="268" cy="430" r="150" fill="url(#{pid}g)"/>'
         f'<rect x="16" y="528" width="368" height="56" fill="#0b1020"/>'
         f'<ellipse cx="230" cy="530" rx="120" ry="9" fill="#ffd98f" opacity=".16"/>'
         + lamp(268, 418, 530, pid) + bench(120, 494, 116) + sparrow(136, 486) +
         f'<text x="200" y="566" text-anchor="middle" font-family="Source Sans 3, sans-serif" font-size="13" letter-spacing="3" fill="#9aa1b8">WYDAWNICTWO CISZA</text></svg>')
    return t


def hero_scene():
    rnd = random.Random(11)
    stars = "".join(f'<circle cx="{rnd.randint(0,1440)}" cy="{rnd.randint(10,520)}" r="{rnd.choice([.7,.9,1.1,1.5])}" fill="#f4ecdc" opacity="{rnd.choice([.25,.4,.6,.85])}"/>' for _ in range(110))
    wins = []
    rw = random.Random(5)
    for r in range(7):
        for c in range(7):
            on = rw.random() < .5
            wins.append(f'<rect class="win{" on" if on else ""}" x="{352+c*30}" y="{560+r*20}" width="15" height="11"/>')
    wins2 = "".join(f'<rect class="win{" on" if rw.random()<.4 else ""}" x="{596+c*26}" y="{622+r*20}" width="12" height="10"/>' for r in range(4) for c in range(3))
    canopy = [(170, 520, 92), (110, 560, 70), (240, 560, 74), (160, 600, 80), (220, 470, 60), (95, 500, 54), (275, 505, 52), (60, 600, 46)]
    can = "".join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in canopy)
    rc = random.Random(9)
    candles = "".join(f'<path d="M{x} {y} l-4 12 h8z" fill="#efe6cf" opacity=".75"/>' for x, y in
                      [(rc.randint(70, 290), rc.randint(450, 610)) for _ in range(18)])
    far = "".join(f'<circle cx="{x}" cy="{712}" r="{r}"/>' for x, r in [(1060, 34), (1110, 46), (1170, 38), (1230, 52), (1300, 40), (1360, 56), (1420, 44)])
    return ('<svg class="hero-scene" viewBox="0 0 1440 800" preserveAspectRatio="xMidYMax slice" aria-hidden="true">'
            '<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#10162b"/><stop offset=".62" stop-color="#1a2342"/><stop offset=".9" stop-color="#2b3765"/></linearGradient>'
            '<radialGradient id="glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ffd98f" stop-opacity=".42"/><stop offset=".45" stop-color="#ffd98f" stop-opacity=".12"/><stop offset="1" stop-color="#ffd98f" stop-opacity="0"/></radialGradient>'
            '<mask id="moon"><rect width="1440" height="800" fill="#fff"/><circle cx="1302" cy="100" r="25" fill="#000"/></mask></defs>'
            '<rect width="1440" height="800" fill="url(#sky)"/>' + stars +
            '<circle cx="1290" cy="110" r="27" fill="#f4ecdc" mask="url(#moon)"/>'
            '<g fill="#0e1428">' + far + '</g>'
            '<rect x="336" y="544" width="228" height="170" fill="#161e38"/><rect x="330" y="538" width="240" height="8" fill="#121a31"/>'
            '<rect x="584" y="606" width="96" height="108" fill="#121a31"/>'
            '<g class="wins">' + "".join(wins) + wins2 + '</g>'
            '<circle cx="820" cy="500" r="250" fill="url(#glow)"/>'
            '<path d="M0 712 Q 360 702 720 710 T 1440 704 V800 H0Z" fill="#0a0f1f"/>'
            '<ellipse cx="760" cy="716" rx="260" ry="20" fill="#ffd98f" opacity=".14"/>'
            '<g fill="#090e1d"><path d="M150 712 C152 660 156 640 160 600 L172 600 C176 640 180 660 184 712Z"/><path d="M164 640 L120 590 L126 586 L170 628Z"/><path d="M170 630 L222 580 L228 586 L176 640Z"/>' + can + '</g>'
            + lamp(820, 488, 712, "h") + bench(640, 676, 150) + sparrow(660, 668) +
            '</svg>')


BRAND = ('<svg viewBox="0 0 42 42" aria-hidden="true"><rect width="42" height="42" rx="6" fill="#1d2744"/>'
         '<circle cx="34" cy="13" r="7" fill="#f7cf86" opacity=".18"/><rect x="33" y="14" width="2" height="21" fill="#f0b34e"/><rect x="30.5" y="9.5" width="7" height="5" rx="1" fill="#f7cf86"/>'
         '<g fill="#f0b34e"><rect x="6" y="18" width="20" height="3" rx="1"/><rect x="8" y="18" width="2.4" height="9"/><rect x="21.6" y="18" width="2.4" height="9"/>'
         '<rect x="4" y="25" width="24" height="3" rx="1"/><rect x="6.5" y="28" width="2.4" height="7"/><rect x="23.1" y="28" width="2.4" height="7"/></g></svg>')
CART_ICO = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M5 7h14l-1.2 12.2a1 1 0 0 1-1 .8H7.2a1 1 0 0 1-1-.8z"/><path d="M9 9V6a3 3 0 0 1 6 0v3"/></svg>'
ICO_STAR = '<svg viewBox="0 0 64 64" fill="none" stroke="#fff" stroke-width="2" aria-hidden="true"><circle cx="40" cy="20" r="3"/><path d="M40 9v5M40 26v5M29 20h5M46 20h5"/><path d="M10 54l20-22M24 39l6 6"/><rect x="22" y="30" width="16" height="7" rx="2" transform="rotate(-42 30 33)"/><circle cx="16" cy="12" r="1.2" fill="#fff"/><circle cx="54" cy="44" r="1.2" fill="#fff"/></svg>'
ICO_BRUSH = '<svg viewBox="0 0 64 64" fill="none" stroke="#fff" stroke-width="2" aria-hidden="true"><path d="M12 52V14h40v38z"/><path d="M12 42l12-10 9 8 7-6 12 10"/><circle cx="40" cy="23" r="4"/><path d="M50 6l-14 22"/><path d="M36 28l-3 5 5-2"/></svg>'
ICO_BIRD = '<svg viewBox="0 0 64 64" fill="none" stroke="#fff" stroke-width="2" aria-hidden="true"><path d="M14 40c4-10 14-15 24-13l8-7 4 3-4 6c2 8-4 17-16 18-6 .5-12-2-16-7z"/><path d="M46 22l6 1"/><circle cx="45" cy="24" r=".8" fill="#fff"/><path d="M28 47l-2 7M34 47l1 7"/><path d="M8 58h48"/><circle cx="20" cy="56" r="1" fill="#fff"/><circle cx="27" cy="57" r="1" fill="#fff"/></svg>'


def nbsp(s):
    out = []
    for part in re.split(r"(<script.*?</script>|<style.*?</style>|<[^>]+>)", s, flags=re.S):
        if part.startswith("<"):
            out.append(part)
        else:
            out.append(re.sub(r"(?<=[\s(„])([aiouwzAIOUWZ]|na|do|od|po|we|ze|że|to|nie|się|Tom) (?=\S)", r"\1&nbsp;", part))
    return "".join(out)


NAV = [("tom-1/", "Tom I"), ("czytaj/", "Czytaj za darmo"), ("o-serii/", "O serii"), ("dla-parafii-i-szkol/", "Dla parafii i szkół")]


def page(path, title, desc, body, schema=None, extra_head=""):
    depth = path.count("/")
    base = "../" * depth
    nav = "".join(f'<a href="{base}{h}"{" aria-current=page" if h == path else ""}>{t}</a>' for h, t in NAV)
    menu = f'<a href="{base or "./"}">Strona główna</a>' + "".join(f'<a href="{base}{h}">{t}</a>' for h, t in NAV) + f'<a href="{base}koszyk/">Koszyk</a>'
    ld = f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>' if schema else ""
    doc = f'''<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{URL}{path}">
<meta property="og:type" content="website"><meta property="og:locale" content="pl_PL"><meta property="og:site_name" content="Wydawnictwo CISZA">
<meta property="og:title" content="{title}"><meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{URL}{path}"><meta property="og:image" content="{URL}img/og.png">
<meta name="theme-color" content="#141b31">
<link rel="icon" href="{base}favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,500;0,7..72,600;1,7..72,400;1,7..72,500&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}assets/styles.css">{extra_head}
{ld}
</head>
<body data-base="{base}">
<a class="skip" href="#tresc">Przejdź do treści</a>
<header class="top"><div class="wrap top-in">
  <a class="brand" href="{base or './'}" aria-label="Wydawnictwo CISZA – strona główna">{BRAND}<span><b>Wydawnictwo CISZA</b><span>Stare małe Dziecko · seria</span></span></a>
  <nav class="nav" aria-label="Menu główne">{nav}</nav>
  <a class="cart-btn" href="{base}koszyk/">{CART_ICO}<span class="cart-l">Koszyk</span><span data-cart-count>0</span></a>
  <button class="burger" aria-label="Menu" aria-expanded="false" aria-controls="menu"><i></i><i></i><i></i></button>
</div>
<nav class="menu" id="menu" aria-label="Menu">{menu}</nav>
</header>
<main id="tresc">
{body}
</main>
<footer class="foot"><div class="wrap">
  <div class="foot-in">
    <div><b>Wydawnictwo CISZA</b><p>Seria „Stare małe Dziecko” Philippe’a Usyka: powieści o dialogu nauki, kultury i wiary. E-booki wysyłamy od razu po zaksięgowaniu płatności.</p><p><a href="{FB}" rel="noopener">Profil na Facebooku: Cicha Mądrość</a></p></div>
    <div><b>Sklep</b><ul><li><a href="{base}tom-1/">Tom I · Pusta ławka i Niebo</a></li><li><a href="{base}czytaj/">Darmowy fragment</a></li><li><a href="{base}tom-1/?opcja=prezent">E-book na prezent</a></li><li><a href="{base}koszyk/">Koszyk</a></li></ul></div>
    <div><b>Seria</b><ul><li><a href="{base}o-serii/">Kim jest Stare Małe Dziecko</a></li><li><a href="{base}o-serii/#autor">O autorze</a></li><li><a href="{base}dla-parafii-i-szkol/">Dla parafii, szkół i bibliotek</a></li></ul></div>
  </div>
  <p class="demo">Projekt demonstracyjny sklepu przygotowany przez Impulseo. Ceny są przykładowe, okładka robocza. Płatności w demo nie są pobierane.</p>
</div></footer>
<script src="{base}assets/app.js" defer></script>
<script src="{base}assets/licznik.js" defer></script>
</body>
</html>
'''
    out = ROOT / path / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(nbsp(doc), encoding="utf-8")


def toc_html(base, link_free=True):
    h = '<div class="toc">'
    for small, name, chs in PARTS:
        h += f'<div class="toc-part"><h3><small>{small}</small>{name}</h3><ol>'
        for s in chs:
            idx = TOM.index(s)
            free = idx < FREE
            t = f'<a href="{base}czytaj/#{slug(s)}">{s["title"]}</a>' if free and link_free else s["title"]
            h += f'<li><span class="n">{ROMAN[s["label"]]}.</span><span class="t">{t}</span>{"<span class=free>za darmo</span>" if free else ""}</li>'
        h += '</ol></div>'
    return h + '</div>'


def slug(s):
    return {"Prolog": "prolog", "Epilog": "epilog"}.get(s["label"], "rozdzial-" + ROMAN[s["label"]].lower())


FAQ = [
    ("Jak dostanę e-booka po zakupie?", "Po zaksięgowaniu płatności przychodzi e-mail z linkami do pobrania trzech plików: EPUB, MOBI i PDF. Linki działają wielokrotnie, więc książkę wgrasz na czytnik, telefon i komputer."),
    ("Na czym przeczytam tę książkę?", "Na każdym czytniku (Kindle, PocketBook, Kobo, inkBOOK), na telefonie, tablecie i komputerze. Pliki nie mają blokad DRM."),
    ("Czy mogę kupić książkę komuś w prezencie?", "Tak. Przy zakupie wybierz „Na prezent”, wpisz e-mail obdarowanej osoby, dzień wysyłki i dedykację. Książka przyjdzie do niej w wybranym dniu, a potwierdzenie do Ciebie."),
    ("Czy dostanę fakturę?", "Tak, zaznacz w koszyku „Potrzebuję faktury” i wpisz NIP. Faktura przyjdzie e-mailem razem z e-bookiem."),
    ("Czy książka jest tylko dla osób wierzących?", "Nie. To opowieść dla każdego, kto zadaje pytania o samotność, miłość i sens. Rozmawiają w niej uczony, artystka i ksiądz, a żaden nie musi przegrać, żeby inny miał rację."),
    ("Kiedy ukaże się Tom II?", "Zapisz się na powiadomienie pod półką z tomami. Napiszemy w dniu premiery, bez innych wiadomości."),
]


def faq_html():
    return '<div class="faq">' + "".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ) + '</div>'


def shelf(base):
    return f'''<div class="shelf" aria-label="Tomy serii">
  <a class="spine s1" href="{base}tom-1/"><span><b>Tom I</b> · Pusta ławka i Niebo</span></a>
  <div class="spine s2"><span>Tom II · w przygotowaniu</span></div>
  <div class="spine s3 later"><span>Tom III</span></div><div class="spine s4 later"><span>Tom IV</span></div>
  <div class="spine s5 later"><span>Tom V</span></div><div class="spine s6 later"><span>Tom VI</span></div>
  <div class="spine s7 later"></div><div class="spine s8 later"></div>
</div>'''


NOTIFY = '''<form class="notify" data-ok="ok-{id}"><label class="sr" for="n-{id}">Twój e-mail</label><input id="n-{id}" type="email" placeholder="Twój e-mail" autocomplete="email" required><button class="btn btn-ink" type="submit">Powiadom mnie o Tomie II</button></form>
<p class="ok" id="ok-{id}">Dziękujemy. Napiszemy w dniu premiery Tomu II.</p>'''


# ---------- strona główna ----------
def home():
    base = ""
    prolog = TOM[0]
    paras = "".join(f'<p{" class=first" if i == 0 else ""}>{p}</p>' for i, p in enumerate(prolog["paras"][:4]))
    body = f'''<section class="hero">{hero_scene()}<div class="wrap hero-in">
  <div>
    <h1>Stare małe Dziecko</h1>
    <p class="vol">Tom I · Pusta ławka i Niebo</p>
    <p class="lead">Powieść o człowieku, który przez wiele lat nauczył się żyć bez przytulenia, ale nie pozwolił, żeby jego serce zrobiło się zimne. I o Ciszy, która okazuje się przyjaciółką.</p>
    <p class="promise">Nie musisz być doskonały, żeby rozpocząć drogę.</p>
    <div class="actions"><a class="btn btn-lamp" href="tom-1/">Kup e-book · 29,90 zł</a><a class="btn btn-line" href="czytaj/">Przeczytaj początek za darmo</a></div>
    <p class="fine">EPUB, MOBI i PDF · plik przychodzi na e-mail zaraz po płatności</p>
  </div>
  <div class="cover-wrap">{cover("hc")}<p class="cover-note">Okładka robocza</p></div>
</div></section>

<section class="sec"><div class="wrap two">
  <div class="sec-head prose" style="margin:0">
    <h2>Opowieść, która nie udaje, że samotność nie boli</h2>
    <p>Na pustej ławce w parku Stare Małe Dziecko spotyka Ciszę. Najpierw wydaje się pustką, potem staje się wierną przyjaciółką, która uczy patrzeć wyżej: w prawdziwe Niebo, gdzie nie ginie ani jedno dobre słowo, ani jedna łza, ani jedno niespełnione pragnienie.</p>
    <p>Między astronomem, malarką i starym księdzem rodzi się rozmowa nauki, kultury i wiary. Trzy języki jednej tęsknoty za Światłem.</p>
    <p><a class="link" href="tom-1/">Zobacz spis treści i szczegóły Tomu I</a></p>
  </div>
  <div>
    <h3>Dla kogo jest ta książka</h3>
    <ul class="who">
      <li><b>Dla młodzieży</b><span>dla tych, którzy podejmują pierwsze trudne decyzje i chcą szybko dorosnąć</span></li>
      <li><b>Dla rodziców i dziadków</b><span>historia, od której może zacząć się prawdziwa rozmowa z dzieckiem lub wnukiem</span></li>
      <li><b>Dla dorosłych</b><span>dla tych, którzy mimo doświadczenia wciąż pytają o sens i mierzą się z własnymi słabościami</span></li>
      <li><b>Dla seniorów</b><span>okazja do spojrzenia na przeżyte życie, przebaczenie i to, co zostawiamy innym</span></li>
      <li><b>Dla wierzących i poszukujących</b><span>wiara jest tu rozmową, a nie wykładem</span></li>
    </ul>
  </div>
</div></section>

<section class="sec sec-soft" id="fragment"><div class="wrap">
  <div class="sec-head" style="margin-left:auto;margin-right:auto;text-align:center"><h2>Zacznij czytać</h2><p>Prolog i dwa pierwsze rozdziały są za darmo, bez zakładania konta.</p></div>
  <div class="book-page">
    <div class="run">Stare małe Dziecko · Tom I</div>
    <h3>Prolog</h3><p class="sub">{prolog["title"]}</p><div class="orn">⁂</div>
    {paras}
    <div class="fade"></div>
  </div>
  <div class="book-cta"><a class="btn btn-ink" href="czytaj/">Czytaj dalej za darmo</a><p>Otworzy się czytnik w przeglądarce: tło jasne, sepia lub nocne, regulowana wielkość liter.</p></div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><h2>Spis treści Tomu I</h2><p>Dwanaście rozdziałów w trzech częściach, od wiosny na pustej ławce do zimy, w której Cisza wskazuje drogę.</p></div>
  {toc_html(base)}
</div></section>

<section class="sec voices"><div class="wrap">
  <div class="sec-head"><h2>Trzy głosy na jednej ławce</h2><p>Nauka, kultura i wiara zbyt często muszą się kłócić. W tej książce siadają obok siebie i uczą się rozmawiać.</p></div>
  <div class="voice-row">
    <div class="voice">{ICO_STAR}<h3>Profesor Antoni</h3><p class="role">astronom, przychodzi latem z teczką pełną liczb</p><blockquote>„Im więcej wiem, tym bardziej się dziwię. A zdziwienie to początek modlitwy.”</blockquote><p class="ch">Rozdział V · Astronom</p></div>
    <div class="voice">{ICO_BRUSH}<h3>Helena</h3><p class="role">malarka, jesienią rozstawia sztalugę naprzeciw ławki</p><blockquote>„Cisza nie jest pusta. Cisza jest pełna. Tylko trzeba mieć odwagę, żeby zatrzymać się przy niej dostatecznie długo.”</blockquote><p class="ch">Rozdział VI · Malarka</p></div>
    <div class="voice">{ICO_BIRD}<h3>Ksiądz Tomasz</h3><p class="role">stary proboszcz, zimą karmi gołębie okruchami z kieszeni</p><blockquote>„Nauka mówi ci, jak. Wiara mówi ci, po co.”</blockquote><p class="ch">Rozdział VII · Stary ksiądz</p></div>
  </div>
  <p class="bench-line">„Całe życie myślałem, że jestem po przeciwnej stronie niż ksiądz. A okazuje się, że patrzymy na tę samą gwiazdę. Tylko ja mierzę odległość, a ksiądz pyta, kto ją zapalił.”<br><span style="font:400 .95rem var(--sans);color:#bcd3c6">Profesor Antoni, rozdział VIII · Trzy języki jednej tęsknoty</span></p>
</div></section>

<section class="sec" id="kup"><div class="wrap">
  <div class="sec-head"><h2>Wybierz, jak chcesz czytać</h2><p>Każda opcja to ten sam e-book w trzech formatach. Różni się tylko tym, kto go dostaje i co dzieje się z kolejnymi tomami.</p></div>
  <div class="offers">
    <div class="offer"><h3>Dla siebie</h3><p class="what">Tom I na Twój e-mail, zaraz po płatności.</p><p class="price">29,90 <small>zł</small></p><ul><li>EPUB, MOBI i PDF</li><li>bez blokad DRM</li><li>faktura na życzenie</li></ul><a class="btn btn-out" href="tom-1/" data-add="tom1">Do koszyka</a></div>
    <div class="offer main"><p class="tag">Dla tych, którzy chcą iść dalej</p><h3>Klub Czytelnika</h3><p class="what">Tom I teraz, a każdy kolejny tom przyjdzie sam w dniu premiery.</p><p class="price">24,90 <small>zł za tom</small></p><ul><li>niższa cena każdego tomu</li><li>nowy tom w dniu premiery</li><li>rezygnujesz jednym kliknięciem</li></ul><a class="btn btn-lamp" href="tom-1/?opcja=klub" data-add="klub">Dołączam</a></div>
    <div class="offer"><h3>Na prezent</h3><p class="what">Dla dziecka, wnuka, przyjaciela. Z Twoją dedykacją.</p><p class="price">29,90 <small>zł</small></p><ul><li>wysyłka w wybranym dniu</li><li>dedykacja w wiadomości</li><li>potwierdzenie dla Ciebie</li></ul><a class="btn btn-out" href="tom-1/?opcja=prezent">Wybierz dzień i dedykację</a></div>
  </div>
  <p class="price-note">Ceny brutto, z 5% VAT. Ceny w demo są przykładowe, ustalimy je z autorem.</p>
</div></section>

<section class="sec sec-soft"><div class="wrap shelf-box">
  {shelf(base)}
  <div>
    <h2>Ta opowieść nie kończy się na jednym tomie</h2>
    <p>„Stare małe Dziecko” to seria wielotomowa. W kolejnych tomach bohater spotyka mistrzów dawnych rzemiosł: kowala, który uczy cierpliwości, zegarmistrza, który uczy szacunku do czasu, i rzemieślnika, przy którym widać, że niedokładność ma konsekwencje.</p>
    {NOTIFY.replace("{id}", "home")}
  </div>
</div></section>

<section class="band"><div class="wrap band-in">
  <div><h2>Dla parafii, szkół i bibliotek</h2><p>Katecheci, nauczyciele, duszpasterze i grupy formacyjne mogą zamówić książkę dla całej grupy, razem z pytaniami do rozmowy po każdym rozdziale.</p></div>
  <a class="btn btn-ink" href="dla-parafii-i-szkol/">Zobacz ofertę dla grup</a>
</div></section>

<section class="sec" id="autor"><div class="wrap author">
  <div class="author-mark"><svg viewBox="0 0 84 60" aria-hidden="true">{bench(14, 36, 56, "#141b31", "#141b31", 0)}</svg></div>
  <div>
    <h2>Od autora</h2>
    <blockquote>„Tę książkę napisano dla każdego, kto nosi w sobie stare małe dziecko, pragnące miłości, bliskości i zrozumienia. Najlepszym Autorem jest sam Pan Bóg, a najlepszym Nauczycielem Pan Jezus, od którego wszyscy się uczymy. Ja tylko spisałem to, co usłyszałem w ciszy.”</blockquote>
    <p><b>Philippe Usyk</b>, autor serii. <a class="link" href="o-serii/#autor">Więcej o autorze i serii</a></p>
  </div>
</div></section>

<section class="sec sec-soft"><div class="wrap"><div class="sec-head"><h2>Pytania przed zakupem</h2></div>{faq_html()}</div></section>
'''
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "name": "Wydawnictwo CISZA", "url": URL, "inLanguage": "pl"},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}]}
    page("", "Stare małe Dziecko – e-book, Tom I: Pusta ławka i Niebo | Wydawnictwo CISZA",
         "Powieść o samotności, ciszy i Bogu, który nie gubi ani jednej łzy. E-book EPUB, MOBI i PDF. Przeczytaj prolog i dwa rozdziały za darmo.", body, schema)


# ---------- Tom I ----------
def tom1():
    base = "../"
    back = TOM[0]  # tylko do opisu
    body = f'''<div class="wrap"><p class="crumbs"><a href="../">Strona główna</a> / Tom I</p>
<div class="product">
  <div class="cover-wrap">{cover("pc")}<p class="cover-note" style="color:var(--muted)">Okładka robocza</p></div>
  <div>
    <h1>Stare małe Dziecko</h1>
    <p class="vol">Tom I · Pusta ławka i Niebo</p>
    <p class="by">Philippe Usyk · Wydawnictwo CISZA · wydanie pierwsze</p>
    <div class="prose"><p>Jest na świecie ktoś taki jak Stare Małe Dziecko: człowiek, który przez wiele lat nauczył się żyć bez przytulenia, lecz nie pozwolił, by jego serce zrobiło się zimne. Towarzyszy mu Cisza, najpierw jak pustka, potem jak wierna przyjaciółka.</p></div>
    <form class="buy" id="buy-form">
      <p class="price" id="buy-price">29,90 <small>zł brutto</small></p>
      <div class="choice">
        <label><input type="radio" name="opcja" value="tom1" checked><div><b>Dla siebie</b><span>e-book na Twój e-mail zaraz po płatności</span></div></label>
        <label><input type="radio" name="opcja" value="klub"><div><b>Klub Czytelnika · 24,90 zł</b><span>Tom I teraz i każdy kolejny tom w dniu premiery, rezygnacja w każdej chwili</span></div></label>
        <label><input type="radio" name="opcja" value="prezent"><div><b>Na prezent</b><span>wyślemy e-booka obdarowanej osobie w wybranym dniu</span></div></label>
      </div>
      <div class="gift" id="gift">
        <div class="field"><label for="g_email">E-mail osoby obdarowanej</label><input id="g_email" name="g_email" type="email" autocomplete="off"></div>
        <div class="field"><label for="g_data">Dzień wysyłki</label><input id="g_data" name="g_data" type="date"><small>Puste pole = wysyłka od razu</small></div>
        <div class="field"><label for="g_ded">Dedykacja</label><textarea id="g_ded" name="g_ded" placeholder="Np. Dla Zosi na bierzmowanie, od babci"></textarea></div>
        <p class="err" id="gift-err">Wpisz adres e-mail osoby, która ma dostać książkę.</p>
      </div>
      <div class="actions"><button class="btn btn-lamp" type="submit">Dodaj do koszyka</button><a class="btn btn-out" href="../czytaj/">Czytaj fragment</a></div>
    </form>
    <table class="spec"><tbody>
      <tr><th>Format</th><td>e-book: EPUB, MOBI, PDF (bez DRM)</td></tr>
      <tr><th>Objętość</th><td>Prolog, 12 rozdziałów w 3 częściach, epilog</td></tr>
      <tr><th>Seria</th><td>„Stare małe Dziecko”, tom I</td></tr>
      <tr><th>Wydawca</th><td>Wydawnictwo CISZA</td></tr>
      <tr><th>Darmowy fragment</th><td><a class="link" href="../czytaj/">Prolog i rozdziały I–II</a></td></tr>
    </tbody></table>
  </div>
</div></div>

<section class="sec sec-soft"><div class="wrap two">
  <div class="prose prose-serif">
    <h2>O książce</h2>
    <p>Na pustej ławce, między astronomem, malarką i starym księdzem, rodzi się rozmowa nauki, kultury i wiary: trzech języków jednej tęsknoty za Światłem.</p>
    <p>To nie jest bajka, choć ma w sobie łagodność bajki. To prawdziwa opowieść o tym, jak serce, które długo czekało na ciepło, samo staje się ciepłem.</p>
    <p>Tom I zaczyna się wiosną, kiedy w parku kwitną kasztanowce, a kończy zimą, w której Stare Małe Dziecko po raz pierwszy nie pyta „dlaczego”, tylko mówi „dziękuję”.</p>
  </div>
  <div>
    <h2>Z książki</h2>
    <ul class="who">
      <li><b>„Pustka to nie jest miejsce, w którym czegoś nie ma. Pustka to miejsce, w którym przestało się czegoś chcieć.”</b><span>Rozdział II · Imię Ciszy</span></li>
      <li><b>„Kroków Boga nie słychać w hałasie. Słychać je tylko w ciszy.”</b><span>Rozdział IV · Kiedy cisza krzyczy</span></li>
      <li><b>„Człowiek przeżywa dzięki tysiącom małych przytuleń, których nie zauważa.”</b><span>Rozdział IX · Tysiąc małych przytuleń</span></li>
      <li><b>„Serce, które długo czekało na ciepło, czasem samo staje się ciepłem.”</b><span>Rozdział X · Druga ławka</span></li>
    </ul>
  </div>
</div></section>

<section class="sec"><div class="wrap"><div class="sec-head"><h2>Spis treści</h2><p>Prolog „Za siedmioma cichymi wieczorami” i epilog „…a może dopiero początek” spinają trzy części opowieści.</p></div>{toc_html(base)}</div></section>
<section class="sec sec-soft"><div class="wrap"><div class="sec-head"><h2>Pytania przed zakupem</h2></div>{faq_html()}</div></section>
'''
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "Book", "@id": URL + "tom-1/#book", "name": "Stare małe Dziecko. Tom I: Pusta ławka i Niebo", "inLanguage": "pl",
         "author": {"@type": "Person", "name": "Philippe Usyk"}, "publisher": {"@type": "Organization", "name": "Wydawnictwo CISZA"},
         "bookFormat": "https://schema.org/EBook", "bookEdition": "Wydanie pierwsze", "genre": ["powieść", "literatura chrześcijańska"],
         "isPartOf": {"@type": "BookSeries", "name": "Stare małe Dziecko"}, "url": URL + "tom-1/",
         "offers": {"@type": "Offer", "price": "29.90", "priceCurrency": "PLN", "availability": "https://schema.org/InStock", "url": URL + "tom-1/"}},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Strona główna", "item": URL}, {"@type": "ListItem", "position": 2, "name": "Tom I", "item": URL + "tom-1/"}]}]}
    page("tom-1/", "Stare małe Dziecko, Tom I: Pusta ławka i Niebo – e-book | Philippe Usyk",
         "E-book Philippe’a Usyka: powieść o samotności, ciszy i wierze, w której astronom, malarka i ksiądz siadają na jednej ławce. EPUB, MOBI, PDF bez DRM.", body, schema)


# ---------- czytnik ----------
def czytaj():
    free = TOM[:FREE]
    opts = "".join(f'<option value="{slug(s)}">{s["label"]}: {s["title"]}</option>' for s in free) + '<option value="dalej">Dalej w pełnej wersji</option>'
    secs = ""
    for s in free:
        ps = "".join(f'<p{" class=first" if i == 0 else ""}>{p}</p>' for i, p in enumerate(s["paras"]))
        secs += f'<section id="{slug(s)}"><p class="rmeta">{s["label"]}</p><h2>{s["title"]}</h2><div class="orn">⁂</div>{ps}</section>'
    rest = "".join(f'<li><span>{ROMAN[s["label"]]}.</span>{s["title"]}</li>' for s in TOM[FREE:])
    body = f'''<div class="reader-bar"><div class="reader-bar-in">
  <label class="sr" for="ch">Rozdział</label><select id="ch">{opts}</select>
  <div class="grp" role="group" aria-label="Wielkość liter"><button data-size="-0.08" aria-label="Mniejsze litery">A−</button><button data-size="0.08" aria-label="Większe litery">A+</button></div>
  <div class="grp" role="group" aria-label="Tło"><button data-theme-btn="jasny">Jasne</button><button data-theme-btn="sepia">Sepia</button><button data-theme-btn="noc">Noc</button></div>
  <a class="btn btn-lamp sp" style="min-height:40px;padding:0 16px" href="../tom-1/">Kup cały tom · 29,90 zł</a>
</div><div class="progress"></div></div>
<div class="reader" id="reader" data-theme="sepia"><article>
<p class="rmeta" style="margin-bottom:50px">Philippe Usyk · Stare małe Dziecko · Tom I: Pusta ławka i Niebo · darmowy fragment</p>
{secs}
<section class="locked" id="dalej"><h2>Tu kończy się darmowy fragment</h2>
<p>Stare Małe Dziecko zostało samo z Ciszą na ławce. Ale minęło wiele dni… W pełnej wersji czeka jeszcze dziesięć rozdziałów i epilog:</p>
<ol>{rest}</ol>
<a class="btn btn-lamp" href="../tom-1/">Kup e-book · 29,90 zł</a>
<p style="margin-top:16px;font-size:1rem !important;opacity:.75">Po zakupie czytasz dalej od rozdziału III, na czytniku, telefonie albo tutaj.</p>
</section>
</article></div>'''
    page("czytaj/", "Czytaj za darmo: Stare małe Dziecko, prolog i rozdziały I–II",
         "Przeczytaj w przeglądarce prolog i dwa pierwsze rozdziały powieści „Stare małe Dziecko. Pusta ławka i Niebo” Philippe’a Usyka. Bez rejestracji.", body)


# ---------- o serii ----------
def o_serii():
    body = f'''<section class="page-head"><div class="wrap"><h1>Kim jest „Stare Małe Dziecko”?</h1><p>Czy można być jednocześnie starym i małym dzieckiem? Można. Bo ta opowieść nie mówi tylko o wieku.</p></div></section>
<section class="sec"><div class="wrap two">
  <div class="fb-text">
    <p>To opowieść o człowieku, który przez całe życie pozostaje uczniem. Kiedy jesteśmy młodzi, wydaje nam się czasem, że dorośli znają już wszystkie odpowiedzi. A później sami dorastamy. Mamy pracę, rodzinę, obowiązki. Podejmujemy ważne decyzje.</p>
    <p>I odkrywamy coś niezwykłego: nadal się uczymy. Cierpliwości. Kochania. Przebaczania. Przyznawania się do błędów. Odpowiedzialności za drugiego człowieka. Wiary i zaufania.</p>
    <p>„Stare Małe Dziecko” może mieć kilkanaście lat. Może mieć czterdzieści. Może mieć siedemdziesiąt. Dopóki człowiek potrafi powiedzieć:</p>
    <p class="say">„Nie wiem. Pomyliłem się. Naucz mnie. Spróbuję jeszcze raz.”</p>
    <p>dopóty pozostaje w nim coś z dziecka. A kiedy doświadczenie nauczy go patrzeć głębiej na siebie i drugiego człowieka, pojawia się mądrość.</p>
    <p>Być może najważniejsze pytanie nie brzmi: „Ile masz lat?”, tylko: „Czego życie próbuje Cię jeszcze nauczyć?”</p>
  </div>
  <div>
    <h2>Mistrzowie dawnych rzemiosł</h2>
    <p>Młody człowiek przychodzi do warsztatu, żeby nauczyć się zawodu. Z czasem okazuje się, że warsztat uczy go czegoś więcej.</p>
    <ul class="crafts">
      <li><b>Kowal</b><br>uczy cierpliwości</li>
      <li><b>Zegarmistrz</b><br>uczy szacunku do czasu</li>
      <li><b>Rzemieślnik</b><br>pokazuje, że niedokładność ma konsekwencje</li>
      <li><b>Mistrz</b><br>wie, że mądrość nie polega na tym, by nigdy się nie pomylić, bo sam kiedyś był uczniem</li>
    </ul>
  </div>
</div></section>

<section class="sec sec-soft"><div class="wrap">
  <div class="sec-head"><h2>Bohaterowie serii</h2><p>Stare Małe Dziecko to nie jeden bohater. To ktoś, kogo każdy z nas nosi w sobie.</p></div>
  <div class="people">
    <div><b>Stare Małe Dziecko</b><span>człowiek, który nie chce dorosnąć na tyle, by przestać się dziwić światu</span></div>
    <div><b>Cisza</b><span>bezcielesna i cierpliwa, nie mówi nic, a mówi wszystko</span></div>
    <div><b>Janek</b><span>stolarz z niewielkiego miasteczka, człowiek zwyczajnych dni i zwyczajnych upadków</span></div>
    <div><b>Hanna</b><span>uczy patrzeć oczami nauki, zanim serce zdąży się oszukać własnym uczuciem</span></div>
    <div><b>Profesor Antoni, Helena, ksiądz Tomasz</b><span>astronom, malarka i kapłan z Tomu I: trzy głosy na jednej ławce</span></div>
    <div><b>Rzemieślnicy i mieszkańcy wsi</b><span>kowale, tkacze, bartnicy, garncarze; ich jedno zdanie waży czasem więcej niż niejedno kazanie</span></div>
  </div>
</div></section>

<section class="sec"><div class="wrap shelf-box">
  {shelf("../")}
  <div><h2>Kolejne tomy</h2><p>Tom I jest już dostępny. Tom II jest w przygotowaniu, a autor pisze kolejne. Zostaw e-mail, a napiszemy w dniu premiery.</p><p>W przygotowaniu jest także seria „Stara Mała Dziewczynka”, dla osób szukających pogłębienia wiary i duchowej relacji z Bogiem.</p>{NOTIFY.replace("{id}", "seria")}</div>
</div></section>

<section class="sec sec-soft" id="autor"><div class="wrap author">
  <div class="author-mark"><svg viewBox="0 0 84 60" aria-hidden="true">{bench(14, 36, 56, "#141b31", "#141b31", 0)}</svg></div>
  <div class="prose">
    <h2>Philippe Usyk</h2>
    <p>Autor serii „Stare małe Dziecko” i założyciel Wydawnictwa CISZA. Pisze o tym, co dzieje się w człowieku, gdy zostaje sam ze swoimi pytaniami, i o tym, że nauka, kultura i wiara to trzy okna wychodzące na to samo Światło.</p>
    <p>„Stare małe dziecko to ja. I Ty.”</p>
    <p><a class="link" href="{FB}" rel="noopener">Cicha Mądrość na Facebooku</a></p>
  </div>
</div></section>'''
    page("o-serii/", "O serii „Stare małe Dziecko” – bohaterowie, autor, kolejne tomy | Wydawnictwo CISZA",
         "Kim jest Stare Małe Dziecko? Seria Philippe’a Usyka o człowieku, który przez całe życie pozostaje uczniem: bohaterowie, mistrzowie dawnych rzemiosł i zapowiedź kolejnych tomów.", body)


# ---------- dla parafii i szkół ----------
def instytucje():
    qs = [
        ("II", "Imię Ciszy", "Mylisz brak z pustką. To nie to samo.", "Czym różni się brak od pustki? Za czym tęsknisz i co ta tęsknota mówi o Twoim sercu?"),
        ("V", "Astronom", "Światło przeżywa swoje źródło.", "Czyje dobro wciąż do Ciebie dochodzi, choć tej osoby nie ma już obok? Komu Ty możesz dziś świecić?"),
        ("VII", "Stary ksiądz", "Nauka mówi ci, jak. Wiara mówi ci, po co.", "Czy spotkałeś się z tym, że trzeba wybierać między rozumem a wiarą? Co mówi o tym ksiądz Tomasz?"),
        ("X", "Druga ławka", "Serce, które długo czekało na ciepło, czasem samo staje się ciepłem.", "Kto w Twojej klasie, rodzinie albo parafii siedzi sam na ławce? Co znaczy „przesunąć się” dla drugiego człowieka?"),
    ]
    qh = "".join(f'<li><b><small>Rozdział {r}</small>{t}</b><div><blockquote>„{c}”</blockquote><p>{q}</p></div></li>' for r, t, c, q in qs)
    body = f'''<section class="page-head"><div class="wrap"><h1>Dla parafii, szkół i bibliotek</h1><p>Książka do wspólnego czytania i rozmowy o samotności, wierze, przebaczeniu i odpowiedzialności za drugiego człowieka.</p></div></section>
<section class="sec"><div class="wrap">
  <div class="sec-head"><h2>Dla kogo</h2></div>
  <div class="groups">
    <div><b>Katecheci i nauczyciele</b><span>lektura na lekcję religii, etyki lub godzinę wychowawczą</span></div>
    <div><b>Duszpasterze i parafie</b><span>materiał na spotkania grup młodzieżowych, rekolekcje, przygotowanie do bierzmowania</span></div>
    <div><b>Grupy formacyjne</b><span>rozdział tygodniowo i rozmowa w kręgu</span></div>
    <div><b>Biblioteki i szkoły</b><span>kolekcja e-booków serii do wypożyczania czytelnikom</span></div>
  </div>
</div></section>
<section class="sec sec-soft"><div class="wrap">
  <div class="sec-head"><h2>Przykład materiału do rozmowy</h2><p>Do każdego rozdziału jedno zdanie z książki i pytania, od których może zacząć się prawdziwa rozmowa.</p></div>
  <ol class="qs">{qh}</ol>
</div></section>
<section class="sec"><div class="wrap two">
  <div class="prose"><h2>Zamówienie dla grupy</h2><p>Napisz, ile osób będzie czytać i w jakiej formie. Przygotujemy wycenę licencji dla grupy lub biblioteki i odpiszemy e-mailem.</p><p>Dla parafii i szkół wystawiamy fakturę z odroczonym terminem płatności.</p></div>
  <form class="form-grid" data-ok="ok-inst" novalidate>
    <div class="field full"><label for="i1">Nazwa parafii, szkoły lub biblioteki</label><input id="i1" required></div>
    <div class="field"><label for="i2">Rodzaj</label><select id="i2"><option>Parafia</option><option>Szkoła</option><option>Biblioteka</option><option>Grupa formacyjna</option><option>Inne</option></select></div>
    <div class="field"><label for="i3">Liczba czytelników</label><input id="i3" inputmode="numeric"></div>
    <div class="field full"><label for="i4">E-mail</label><input id="i4" type="email" autocomplete="email" required></div>
    <div class="field full"><label for="i5">Wiadomość</label><textarea id="i5" placeholder="Np. grupa bierzmowanych, 24 osoby, czytamy od listopada"></textarea></div>
    <div class="full"><button class="btn btn-ink" type="submit">Wyślij zapytanie</button><p class="ok" id="ok-inst">Dziękujemy. Odpiszemy z wyceną na podany e-mail.</p></div>
  </form>
</div></section>'''
    page("dla-parafii-i-szkol/", "Książka dla parafii, szkół i bibliotek – Stare małe Dziecko | Wydawnictwo CISZA",
         "Powieść „Stare małe Dziecko” dla katechetów, nauczycieli, parafii i bibliotek: licencja dla grupy i pytania do rozmowy po każdym rozdziale.", body)


# ---------- koszyk ----------
def koszyk():
    body = f'''<div class="wrap"><p class="crumbs"><a href="../">Strona główna</a> / Koszyk</p>
<template id="mini-cover">{cover("mc", "mini")}</template>
<div class="done" id="done" style="margin:40px 0 90px">
  <h1 style="font-size:2.2rem">Dziękujemy za zamówienie</h1>
  <p>To jest wersja demonstracyjna, więc płatność nie została pobrana. W gotowym sklepie stałoby się to tak:</p>
  <ol class="steps"><li>Otwiera się płatność <b id="done-pay">BLIK</b>.</li><li>Po zaksięgowaniu wysyłamy e-mail na <b id="done-mail"></b> z linkami do plików EPUB, MOBI i PDF.</li><li>Prezenty wychodzą do obdarowanych w wybranym dniu, a Ty dostajesz potwierdzenie.</li></ol>
  <p style="margin-top:22px"><a class="btn btn-ink" href="../czytaj/">Wróć do czytania</a></p>
</div>
<div id="cart-box"><h1 style="font-size:clamp(2rem,4vw,2.8rem);margin-top:18px">Koszyk</h1>
<div class="cart">
  <div>
    <div class="cart-lines" id="cart-lines"></div>
    <form id="checkout" novalidate style="margin-top:44px">
      <fieldset><legend>Dane do wysyłki e-booka</legend><div class="form-grid">
        <div class="field full"><label for="email">E-mail</label><input id="email" name="email" type="email" autocomplete="email" required><small>Na ten adres przyjdą pliki i potwierdzenie.</small></div>
        <div class="field full"><label for="imie">Imię i nazwisko</label><input id="imie" name="imie" autocomplete="name"></div>
        <label class="check full"><input type="checkbox" id="fv"> Potrzebuję faktury</label>
        <div class="form-grid full" id="fv-box" hidden><div class="field"><label for="nip">NIP</label><input id="nip" inputmode="numeric"></div><div class="field"><label for="firma">Nazwa firmy lub instytucji</label><input id="firma"></div></div>
      </div></fieldset>
      <fieldset><legend>Płatność</legend><div class="pay">
        <label><input type="radio" name="platnosc" value="BLIK" checked>BLIK</label>
        <label><input type="radio" name="platnosc" value="Przelewy24">Przelew online</label>
        <label><input type="radio" name="platnosc" value="karta">Karta</label>
      </div></fieldset>
      <fieldset><legend class="sr">Zgody</legend>
        <label class="check" style="margin-bottom:12px"><input type="checkbox" name="reg"> Akceptuję regulamin sklepu i politykę prywatności.</label>
        <label class="check"><input type="checkbox" name="cyfrowe"> Proszę o dostarczenie e-booka od razu i przyjmuję do wiadomości, że po pobraniu pliku tracę prawo do odstąpienia od umowy.</label>
      </fieldset>
      <p class="err" id="co-err">Wpisz poprawny e-mail i zaznacz obie zgody.</p>
      <button class="btn btn-lamp" type="submit" style="width:100%">Zamawiam i płacę <span data-sum style="margin-left:.3em"></span></button>
    </form>
  </div>
  <aside class="summary"><h2 style="font-size:1.5rem">Podsumowanie</h2>
    <div class="row"><span>Produkty</span><span data-sum>0,00 zł</span></div>
    <div class="row"><span>Dostawa e-mailem</span><span>0,00 zł</span></div>
    <div class="row" style="color:var(--muted);font-size:.95rem"><span>w tym VAT 5%</span><span data-vat>0,00 zł</span></div>
    <div class="row total"><span>Razem</span><span data-sum>0,00 zł</span></div>
    <p style="color:var(--muted);font-size:.95rem;margin:14px 0 0">Ceny w demo są przykładowe.</p>
  </aside>
</div></div></div>'''
    page("koszyk/", "Koszyk | Wydawnictwo CISZA", "Koszyk sklepu Wydawnictwa CISZA.", body, extra_head='\n<meta name="robots" content="noindex">')


def extras():
    (ROOT / "favicon.svg").write_text(BRAND.replace('aria-hidden="true"', 'xmlns="http://www.w3.org/2000/svg"'), encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {URL}sitemap.xml\n", encoding="utf-8")
    urls = ["", "tom-1/", "czytaj/", "o-serii/", "dla-parafii-i-szkol/"]
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
                                      "".join(f"  <url><loc>{URL}{u}</loc></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")
    (ROOT / "img").mkdir(exist_ok=True)
    (ROOT / "img" / "okladka.svg").write_text(cover("oc").replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1), encoding="utf-8")


home(); tom1(); czytaj(); o_serii(); instytucje(); koszyk(); extras()
print("ok")
