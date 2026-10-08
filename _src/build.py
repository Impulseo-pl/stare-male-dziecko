"""python _src/build.py -> generuje index.html i podstrony z _src/tom1.json"""
import json, re, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
URL = "https://impulseo-pl.github.io/stare-male-dziecko/"
FB = "https://www.facebook.com/profile.php?id=61593939705947"
TOM = json.loads((ROOT / "_src" / "tom1.json").read_text(encoding="utf-8"))
FREE = 3  # Prolog, Rozdział I, Rozdział II
ROMAN = {s["label"]: s["label"].replace("Rozdział ", "") for s in TOM}
# numery stron ze spisu treści w PDF
STRONY = {"Prolog": 8, "Rozdział I": 11, "Rozdział II": 14, "Rozdział III": 17, "Rozdział IV": 20, "Rozdział V": 24, "Rozdział VI": 27,
          "Rozdział VII": 30, "Rozdział VIII": 33, "Rozdział IX": 37, "Rozdział X": 40, "Rozdział XI": 43, "Rozdział XII": 46, "Epilog": 49}
PARTS = [("Część pierwsza · Cisza", 10, TOM[1:5]), ("Część druga · Trzy głosy", 23, TOM[5:9]), ("Część trzecia · Niebo", 36, TOM[9:13])]

# obrazy Vilhelma Hammershøia (domena publiczna, Wikimedia Commons)
OBRAZY = {
    "swiatlo": ("Taniec pyłków w promieniach słońca, 1900", "https://commons.wikimedia.org/wiki/File:Hammersh%C3%B8i_Dust_motes_dancing.jpg"),
    "kanapa": ("Słońce w salonie III, 1903", "https://commons.wikimedia.org/wiki/File:Vilhelm_Hammersh%C3%B8i,_Sunshine_in_the_Drawing_Room_III,_1903.jpg"),
    "czytajaca": ("Wnętrze, Strandgade 30, 1900", "https://commons.wikimedia.org/wiki/File:Vilhelm_Hammersh%C3%B8i,_Interi%C3%B8r_fra_Strandgade_30,_1900.jpg"),
    "stol": ("Wnętrze ze stołem, regałem i krzesłem, Strandgade 25", "https://commons.wikimedia.org/wiki/File:Vilhelm_Hammersh%C3%B8i_Interior_with_a_Table,_Bookcase_and_Windsor_Chair_Strandgade_25.jpg"),
    "drzwi": ("Białe drzwi, 1913", "https://commons.wikimedia.org/wiki/File:Vilhelm_Hammersh%C3%B8i_-_Hvide_d%C3%B8re._Interi%C3%B8r_fra_Strandgade_25_-_1913.png"),
}


def img(base, key, alt, sizes="(max-width:900px) 100vw, 55vw", eager=False):
    return (f'<img src="{base}img/{key}-1600.jpg" srcset="{base}img/{key}-900.jpg 900w, {base}img/{key}-1600.jpg 1600w" sizes="{sizes}" '
            f'alt="{alt}"{"" if eager else " loading=lazy"} decoding="async">')


def cap(key):
    return f"Vilhelm Hammershøi, {OBRAZY[key][0]}"


def book(base, w=None, cls=""):
    st = f' style="--w:{w}"' if w else ""
    return (f'<div class="book {cls}"{st} role="img" aria-label="Okładka: Philippe Usyk, Stare małe Dziecko, Tom I, Pusta ławka i Niebo">'
            f'<div class="book-art"><img src="{base}img/swiatlo-900.jpg" alt="" loading="lazy"></div>'
            '<div class="book-band"><span class="b-au">Philippe Usyk</span><span class="b-ti">Stare małe Dziecko</span>'
            '<span class="b-vol">Tom I · Pusta ławka i Niebo</span><span class="b-pub">Cisza</span></div></div>')


def nbsp(s):
    out = []
    for part in re.split(r"(<script.*?</script>|<style.*?</style>|<title>.*?</title>|<[^>]+>)", s, flags=re.S):
        if part.startswith("<"):
            out.append(part)
        else:
            out.append(re.sub(r"(?<=[\s(„])([aiouwzAIOUWZ]|na|do|od|po|we|ze|że|to|nie|się|Tom) (?=\S)", r"\1&nbsp;", part))
    return "".join(out)


NAV = [("tom-1/", "Tom I"), ("czytaj/", "Czytaj fragment"), ("o-serii/", "O serii"), ("dla-parafii-i-szkol/", "Dla parafii i szkół")]


def page(path, title, desc, body, schema=None, extra_head="", preload=None):
    depth = path.count("/")
    base = "../" * depth
    home = base or "./"
    nav = "".join(f'<a href="{base}{h}"{" aria-current=page" if h == path else ""}>{t}</a>' for h, t in NAV)
    menu = f'<a href="{home}">Strona główna</a>' + "".join(f'<a href="{base}{h}">{t}</a>' for h, t in NAV) + f'<a href="{base}koszyk/">Koszyk</a>'
    ld = f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>' if schema else ""
    pre = f'\n<link rel="preload" as="image" href="{base}img/{preload}-1600.jpg" imagesrcset="{base}img/{preload}-900.jpg 900w, {base}img/{preload}-1600.jpg 1600w" imagesizes="(max-width:900px) 100vw, 55vw">' if preload else ""
    credits = " · ".join(f'<a href="{u}" rel="noopener">{t}</a>' for t, u in OBRAZY.values())
    doc = f'''<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{URL}{path}">
<meta property="og:type" content="website"><meta property="og:locale" content="pl_PL"><meta property="og:site_name" content="Wydawnictwo Cisza">
<meta property="og:title" content="{title}"><meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{URL}{path}"><meta property="og:image" content="{URL}img/og.jpg">
<meta name="theme-color" content="#24221e">
<link rel="icon" href="{base}favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Public+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}assets/styles.css">{pre}{extra_head}
{ld}
</head>
<body data-base="{base}">
<a class="skip" href="#tresc">Przejdź do treści</a>
<div class="strip">E-booki wysyłamy na e-mail zaraz po płatności · BLIK, przelew, karta</div>
<header class="top"><div class="wrap top-in">
  <a class="brand" href="{home}"><b>Cisza</b><span>wydawnictwo</span></a>
  <nav class="nav" aria-label="Menu główne">{nav}</nav>
  <a class="cart-btn" href="{base}koszyk/">Koszyk (<span data-cart-count>0</span>)</a>
  <button class="burger" aria-label="Menu" aria-expanded="false" aria-controls="menu"><i></i><i></i><i></i></button>
</div>
<nav class="menu" id="menu" aria-label="Menu">{menu}</nav>
</header>
<main id="tresc">
{body}
</main>
<footer class="foot"><div class="wrap">
  <div class="foot-in">
    <div><a class="brand" href="{home}"><b>Cisza</b><span>wydawnictwo</span></a><p style="margin-top:22px;max-width:28em">Wydajemy serię „Stare małe Dziecko” Philippe’a Usyka: powieści o samotności, wierze i o tym, że człowiek przez całe życie pozostaje uczniem.</p><p><a href="{FB}" rel="noopener">Cicha Mądrość na Facebooku</a></p></div>
    <div><h4>Sklep</h4><ul><li><a href="{base}tom-1/">Tom I · Pusta ławka i Niebo</a></li><li><a href="{base}czytaj/">Darmowy fragment</a></li><li><a href="{base}tom-1/?opcja=prezent#kup">E-book na prezent</a></li><li><a href="{base}koszyk/">Koszyk</a></li></ul></div>
    <div><h4>Seria</h4><ul><li><a href="{base}o-serii/">Kim jest Stare Małe Dziecko</a></li><li><a href="{base}o-serii/#autor">O autorze</a></li><li><a href="{base}dla-parafii-i-szkol/">Dla parafii, szkół i bibliotek</a></li></ul></div>
  </div>
  <p class="credits">Obrazy: Vilhelm Hammershøi (1864–1916), domena publiczna, Wikimedia Commons: {credits}.<br>Projekt demonstracyjny przygotowany przez Impulseo. Ceny są przykładowe, okładka robocza, płatności w demo nie są pobierane.</p>
</div></footer>
<script src="{base}assets/app.js" defer></script>
<script src="{base}assets/licznik.js" defer></script>
</body>
</html>
'''
    out = ROOT / path / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(nbsp(doc), encoding="utf-8")


def slug(s):
    return {"Prolog": "prolog", "Epilog": "epilog"}.get(s["label"], "rozdzial-" + ROMAN[s["label"]].lower())


def contents(base):
    def row(s, r):
        free = TOM.index(s) < FREE
        t = f'<a href="{base}czytaj/#{slug(s)}">{s["title"]}</a>' if free else s["title"]
        return f'<div class="row"><span class="r">{r}</span><span>{t}</span>{" <em>fragment</em>" if free else ""}<span class="dots"></span><span>{STRONY[s["label"]]}</span></div>'
    h = '<div class="contents"><h2>Spis treści</h2>' + row(TOM[0], "")
    for name, pg, chs in PARTS:
        h += f'<p class="part">{name}</p>' + "".join(row(s, ROMAN[s["label"]] + ".") for s in chs)
    h += row(TOM[-1], "")
    return h + f'<p class="note">Prolog i dwa pierwsze rozdziały przeczytasz za darmo. <a class="txt-link" href="{base}czytaj/">Otwórz fragment</a></p></div>'


FAQ = [
    ("Jak dostanę e-booka po zakupie?", "Po zaksięgowaniu płatności przychodzi e-mail z linkami do pobrania trzech plików: EPUB, MOBI i PDF. Linki działają wielokrotnie, więc książkę wgrasz na czytnik, telefon i komputer."),
    ("Na czym przeczytam tę książkę?", "Na każdym czytniku (Kindle, PocketBook, Kobo, inkBOOK), na telefonie, tablecie i komputerze. Pliki nie mają blokad DRM."),
    ("Czy mogę kupić książkę komuś w prezencie?", "Tak. Przy zakupie wybierz „Na prezent”, wpisz e-mail obdarowanej osoby, dzień wysyłki i dedykację. Książka przyjdzie do niej w wybranym dniu, a potwierdzenie do Ciebie."),
    ("Czy dostanę fakturę?", "Tak, zaznacz w koszyku „Potrzebuję faktury” i wpisz NIP. Faktura przyjdzie e-mailem razem z e-bookiem."),
    ("Czy książka jest tylko dla osób wierzących?", "Nie. To opowieść dla każdego, kto zadaje pytania o samotność, miłość i sens. Rozmawiają w niej uczony, artystka i ksiądz, a żaden nie musi przegrać, żeby inny miał rację."),
    ("Kiedy ukaże się Tom II?", "Zostaw e-mail w sekcji o kolejnych tomach. Napiszemy w dniu premiery, bez innych wiadomości."),
]


def faq_html():
    return '<div class="faq">' + "".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ) + '</div>'


def opts(gift=False):
    g = ""
    if gift:
        g = '''<div class="gift">
        <div class="field"><label for="g_email">E-mail osoby obdarowanej</label><input id="g_email" name="g_email" type="email" autocomplete="off"></div>
        <div class="field"><label for="g_data">Dzień wysyłki</label><input id="g_data" name="g_data" type="date"><small>Puste pole oznacza wysyłkę od razu.</small></div>
        <div class="field"><label for="g_ded">Dedykacja</label><textarea id="g_ded" name="g_ded" placeholder="Np. Dla Zosi na bierzmowanie, od babci"></textarea></div>
        <p class="err">Wpisz adres e-mail osoby, która ma dostać książkę.</p></div>'''
    return f'''<div class="opts">
      <label class="opt"><input type="radio" name="opcja" value="tom1" checked><div><b>Dla siebie</b><span>e-book na Twój e-mail zaraz po płatności</span></div><span class="p">29,90 zł</span></label>
      <label class="opt"><input type="radio" name="opcja" value="klub"><div><b>Klub Czytelnika</b><span>Tom I teraz, każdy kolejny tom sam przyjdzie w dniu premiery; rezygnujesz, kiedy chcesz</span></div><span class="p">24,90 zł</span></label>
      <label class="opt"><input type="radio" name="opcja" value="prezent"><div><b>Na prezent</b><span>wyślemy e-booka obdarowanej osobie w wybranym dniu, z Twoją dedykacją</span></div><span class="p">29,90 zł</span></label>
    </div>{g}'''


NOTIFY = '''<form class="notify" data-ok="ok-{id}"><label class="sr" for="n-{id}">Twój e-mail</label><input id="n-{id}" type="email" placeholder="Twój e-mail" autocomplete="email" required><button class="btn" type="submit">Powiadom mnie</button></form>
<p class="ok" id="ok-{id}">Dziękujemy. Napiszemy w dniu premiery Tomu II.</p>'''


# ---------- strona główna ----------
def home():
    base = ""
    pr = TOM[0]["paras"]
    left = "".join(f'<p class="t{" f" if i == 0 else ""}">{p}</p>' for i, p in enumerate(pr[:2]))
    right = "".join(f'<p class="t">{p}</p>' for p in pr[2:5])
    FLIP_PAGES = "".join(f'<div class="fpage"><img src="img/strony/s{n:02d}.jpg" alt="Strona {n} książki"></div>' for n in [2] + list(range(4, 20)))
    body = f'''<section class="hero">
  <figure class="hero-art">{img(base, "swiatlo", "Obraz Vilhelma Hammershøia: światło z okna pada smugą do pustego pokoju", eager=True)}<figcaption>{cap("swiatlo")}</figcaption></figure>
  <div class="hero-txt">
    <p class="au">Philippe Usyk</p>
    <h1>Stare małe Dziecko</h1>
    <p class="vol">Tom I. Pusta ławka i Niebo</p>
    <p class="lead">Powieść o człowieku, który przez wiele lat nauczył się żyć bez przytulenia, ale nie pozwolił, żeby jego serce zrobiło się zimne. I o Ciszy, która z pustki staje się przyjaciółką.</p>
    <div class="buyline"><span class="pr">29,90 <small>zł</small></span><a class="btn" href="tom-1/">Kup e-book</a><a class="txt-link" href="czytaj/">Przeczytaj początek za darmo</a></div>
    <p class="meta">EPUB, MOBI i PDF, bez DRM · plik przychodzi na e-mail</p>
  </div>
</section>

<section class="sec"><div class="wrap split top">
  <div>
    <p class="lede">Na pustej ławce w parku Stare Małe Dziecko spotyka Ciszę. Między astronomem, malarką i starym księdzem rodzi się rozmowa nauki, kultury i wiary: trzech języków jednej tęsknoty za Światłem.</p>
    <p style="font-size:1.12rem;color:var(--ink-2);max-width:34em">To nie jest bajka, choć ma w sobie łagodność bajki. To opowieść o tym, jak serce, które długo czekało na ciepło, samo staje się ciepłem. Nie musisz być doskonały, żeby rozpocząć tę drogę.</p>
  </div>
  <div>
    <h2 style="font-size:2rem">Dla kogo</h2>
    <ul class="who">
      <li><b>Młodzież</b><span>dla tych, którzy podejmują pierwsze trudne decyzje i chcą szybko dorosnąć</span></li>
      <li><b>Rodzice i dziadkowie</b><span>historia, od której może zacząć się prawdziwa rozmowa z dzieckiem albo wnukiem</span></li>
      <li><b>Dorośli</b><span>dla tych, którzy mimo doświadczenia wciąż pytają o sens</span></li>
      <li><b>Seniorzy</b><span>okazja, by spojrzeć na przeżyte życie, przebaczenie i to, co zostawiamy innym</span></li>
      <li><b>Poszukujący</b><span>wiara jest tu rozmową, a nie wykładem</span></li>
    </ul>
  </div>
</div></section>

<section class="sec wall"><div class="wrap bench">
  <figure>{img(base, "kanapa", "Obraz Vilhelma Hammershøia: pusta kanapa w słonecznym salonie", "(max-width:860px) 100vw, 60vw")}<figcaption class="cap">{cap("kanapa")}</figcaption></figure>
  <div>
    <blockquote>„Pusta ławka przestała być znakiem przegranej. Stała się znakiem zaproszenia.”</blockquote>
    <p class="src">Rozdział III · Pusta ławka</p>
  </div>
</div></section>

<section class="sec flip-sec" id="fragment"><div class="wrap">
  <h2>Przeczytaj fragment za darmo</h2>
  <p class="sub">Przekartkuj początek książki: okładkę, słowo od autora, prolog i dwa pierwsze rozdziały. Przeciągnij róg strony albo użyj strzałek.</p>
  <div class="flip-stage"><div id="flipbook">
    <div class="fpage" data-density="hard"><img src="img/strony/s01.jpg" alt="Okładka Tomu I"></div>
    {FLIP_PAGES}
    <div class="fpage blank"></div>
    <div class="fpage end" data-density="hard"><h3>Tu kończy się fragment</h3><p>Dalej czeka pusta ławka, astronom, malarka i stary ksiądz.</p><a class="btn light" href="tom-1/">Kup Tom I · 29,90 zł</a></div>
  </div></div>
  <div class="flip-ctrl"><button id="flip-prev" type="button">Poprzednia</button><span id="flip-count"></span><button id="flip-next" type="button">Następna</button></div>
  <div class="flip-cta"><a class="btn" href="tom-1/">Kup Tom I i czytaj dalej</a><p>Wolisz większe litery? <a class="txt-link" href="czytaj/">Otwórz fragment w czytniku</a></p></div>
</div></section>
<script src="assets/page-flip.browser.js" defer></script><script src="assets/flip.js" defer></script>

<section class="sec wall">{contents(base)}</section>

<section class="sec dark"><div class="wrap">
  <h2>Trzy głosy na jednej ławce</h2>
  <p class="intro">Nauka, kultura i wiara zbyt często muszą się ze sobą kłócić. W tej książce siadają obok siebie i uczą się rozmawiać.</p>
  <div class="voices">
    <div class="voice"><p class="who-is">Nauka</p><h3>Profesor Antoni</h3><blockquote>„Im więcej wiem, tym bardziej się dziwię. A zdziwienie to początek modlitwy.”</blockquote><p>Astronom. Latem siada na drugim końcu ławki z teczką pełną liczb. Rozdział V.</p></div>
    <div class="voice"><p class="who-is">Kultura</p><h3>Helena</h3><blockquote>„Cisza nie jest pusta. Cisza jest pełna.”</blockquote><p>Malarka. Jesienią rozstawia sztalugę naprzeciw ławki i maluje to, czego nie widać. Rozdział VI.</p></div>
    <div class="voice"><p class="who-is">Wiara</p><h3>Ksiądz Tomasz</h3><blockquote>„Nauka mówi ci, jak. Wiara mówi ci, po co.”</blockquote><p>Stary proboszcz. Zimą karmi gołębie okruchami z kieszeni i mówi do nich po imieniu. Rozdział VII.</p></div>
  </div>
  <p class="closing">„Całe życie myślałem, że jestem po przeciwnej stronie niż ksiądz. A okazuje się, że patrzymy na tę samą gwiazdę. Tylko ja mierzę odległość, a ksiądz pyta, kto ją zapalił.”<span>Profesor Antoni, rozdział VIII · Trzy języki jednej tęsknoty</span></p>
</div></section>

<section class="sec" id="kup"><div class="wrap shop">
  {book(base)}
  <form data-buy>
    <h2>Kup Tom I</h2>
    <p style="color:var(--ink-2);max-width:34em">Ten sam e-book w trzech formatach. Wybierz, czy czytasz sam, chcesz dostawać kolejne tomy, czy dajesz go komuś w prezencie.</p>
    {opts()}
    <button class="btn" type="submit">Dodaj do koszyka</button>
    <p class="fine">Ceny brutto z 5% VAT. W demo ceny są przykładowe, ustalimy je z autorem.</p>
  </form>
</div></section>

<section class="sec wall"><div class="wrap doors">
  <figure>{img(base, "drzwi", "Obraz Vilhelma Hammershøia: otwarte białe drzwi do kolejnych pokoi", "(max-width:860px) 100vw, 45vw")}<figcaption class="cap">{cap("drzwi")}</figcaption></figure>
  <div>
    <h2>Za progiem czeka dalsza droga</h2>
    <p style="font-size:1.12rem;max-width:32em">„Stare małe Dziecko” to seria wielotomowa. W kolejnych tomach bohater trafia do warsztatów dawnych mistrzów: kowal uczy go cierpliwości, zegarmistrz szacunku do czasu, a rzemieślnik pokazuje, że niedokładność ma konsekwencje.</p>
    <p style="font-size:1.12rem">Tom II jest w przygotowaniu. Zostaw e-mail, napiszemy w dniu premiery.</p>
    {NOTIFY.replace("{id}", "home")}
  </div>
</div></section>

<section class="sec"><div class="wrap parish">
  <figure>{img(base, "stol", "Obraz Vilhelma Hammershøia: stół z jedną miską, regał i krzesło", "(max-width:860px) 100vw, 40vw")}<figcaption class="cap">{cap("stol")}</figcaption></figure>
  <div>
    <h2>Dla parafii, szkół i bibliotek</h2>
    <p style="font-size:1.12rem;max-width:32em">Książka do wspólnego czytania z młodzieżą, grupą formacyjną albo w bibliotece. Dla katechetów i nauczycieli przygotowujemy licencję dla całej grupy i pytania do rozmowy po rozdziałach.</p>
    <p><a class="btn ghost" href="dla-parafii-i-szkol/">Oferta dla grup</a></p>
  </div>
</div></section>

<section class="sec wall"><div class="wrap author">
  <blockquote>„Tę książkę napisano dla każdego, kto nosi w sobie stare małe dziecko, pragnące miłości, bliskości i zrozumienia. Najlepszym Autorem jest sam Pan Bóg. Ja tylko spisałem to, co usłyszałem w ciszy.”</blockquote>
  <p class="sig">Philippe Usyk, od autora</p>
  <p><a class="txt-link" href="o-serii/#autor">O autorze i serii</a></p>
</div></section>

<section class="sec"><div class="wrap"><h2>Pytania przed zakupem</h2>{faq_html()}</div></section>
'''
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "name": "Wydawnictwo Cisza", "url": URL, "inLanguage": "pl"},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}]}
    page("", "Stare małe Dziecko – e-book, Tom I: Pusta ławka i Niebo | Wydawnictwo Cisza",
         "Powieść Philippe’a Usyka o samotności, ciszy i Bogu, który nie gubi ani jednej łzy. E-book EPUB, MOBI i PDF. Przeczytaj prolog i dwa rozdziały za darmo.", body, schema, preload="swiatlo")


# ---------- Tom I ----------
def tom1():
    base = "../"
    body = f'''<div class="wrap"><p class="crumbs"><a href="../">Strona główna</a> / Tom I</p>
<div class="product" id="kup">
  {book(base)}
  <div>
    <h1>Stare małe Dziecko</h1>
    <p class="vol">Tom I. Pusta ławka i Niebo</p>
    <p class="by">Philippe Usyk · Wydawnictwo Cisza · wydanie pierwsze</p>
    <p class="desc">Jest na świecie ktoś taki jak Stare Małe Dziecko: człowiek, który przez wiele lat nauczył się żyć bez przytulenia, lecz nie pozwolił, by jego serce zrobiło się zimne. Towarzyszy mu Cisza, najpierw jak pustka, potem jak wierna przyjaciółka.</p>
    <form data-buy>
      {opts(gift=True)}
      <div style="display:flex;gap:22px;align-items:center;flex-wrap:wrap"><button class="btn" type="submit">Dodaj do koszyka</button><a class="txt-link" href="../czytaj/">Czytaj fragment</a></div>
    </form>
    <table class="spec"><tbody>
      <tr><th>Format</th><td>e-book: EPUB, MOBI, PDF (bez DRM)</td></tr>
      <tr><th>Zawartość</th><td>prolog, 12 rozdziałów w 3 częściach, epilog</td></tr>
      <tr><th>Seria</th><td>„Stare małe Dziecko”, tom I</td></tr>
      <tr><th>Wydawca</th><td>Wydawnictwo Cisza</td></tr>
      <tr><th>Darmowy fragment</th><td><a class="txt-link" href="../czytaj/">prolog i rozdziały I–II</a></td></tr>
    </tbody></table>
  </div>
</div></div>

<section class="sec wall"><div class="wrap split top">
  <div>
    <h2>O książce</h2>
    <p class="lede" style="font-size:1.45rem">Na pustej ławce, między astronomem, malarką i starym księdzem, rodzi się rozmowa nauki, kultury i wiary.</p>
    <p style="font-size:1.12rem;color:var(--ink-2)">Tom I zaczyna się wiosną, kiedy w parku kwitną kasztanowce, a kończy zimą, w której Stare Małe Dziecko po raz pierwszy nie pyta „dlaczego”, tylko mówi „dziękuję”. To nie jest bajka. To prawdziwa opowieść o tym, jak serce, które długo czekało na ciepło, samo staje się ciepłem.</p>
  </div>
  <div>
    <h2>Z książki</h2>
    <ul class="quotes">
      <li><q>Pustka to nie jest miejsce, w którym czegoś nie ma. Pustka to miejsce, w którym przestało się czegoś chcieć.</q><span>Rozdział II · Imię Ciszy</span></li>
      <li><q>Kroków Boga nie słychać w hałasie. Słychać je tylko w ciszy.</q><span>Rozdział IV · Kiedy cisza krzyczy</span></li>
      <li><q>Człowiek przeżywa dzięki tysiącom małych przytuleń, których nie zauważa.</q><span>Rozdział IX · Tysiąc małych przytuleń</span></li>
      <li><q>Serce, które długo czekało na ciepło, czasem samo staje się ciepłem.</q><span>Rozdział X · Druga ławka</span></li>
    </ul>
  </div>
</div></section>

<section class="sec">{contents(base)}</section>
<section class="sec wall"><div class="wrap"><h2>Pytania przed zakupem</h2>{faq_html()}</div></section>
'''
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "Book", "@id": URL + "tom-1/#book", "name": "Stare małe Dziecko. Tom I: Pusta ławka i Niebo", "inLanguage": "pl",
         "author": {"@type": "Person", "name": "Philippe Usyk"}, "publisher": {"@type": "Organization", "name": "Wydawnictwo Cisza"},
         "bookFormat": "https://schema.org/EBook", "bookEdition": "Wydanie pierwsze", "genre": ["powieść", "literatura chrześcijańska"],
         "isPartOf": {"@type": "BookSeries", "name": "Stare małe Dziecko"}, "url": URL + "tom-1/",
         "offers": {"@type": "Offer", "price": "29.90", "priceCurrency": "PLN", "availability": "https://schema.org/InStock", "url": URL + "tom-1/"}},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Strona główna", "item": URL}, {"@type": "ListItem", "position": 2, "name": "Tom I", "item": URL + "tom-1/"}]}]}
    page("tom-1/", "Stare małe Dziecko, Tom I: Pusta ławka i Niebo – e-book | Philippe Usyk",
         "E-book Philippe’a Usyka: powieść o samotności, ciszy i wierze, w której astronom, malarka i ksiądz siadają na jednej ławce. EPUB, MOBI, PDF bez DRM.", body, schema)


# ---------- czytnik ----------
def czytaj():
    free = TOM[:FREE]
    opts_ = "".join(f'<option value="{slug(s)}">{s["label"]}: {s["title"]}</option>' for s in free) + '<option value="dalej">Dalej w pełnej wersji</option>'
    secs = ""
    for s in free:
        ps = "".join(f'<p{" class=first" if i == 0 else ""}>{p}</p>' for i, p in enumerate(s["paras"]))
        secs += f'<section id="{slug(s)}"><p class="rmeta">{s["label"]}</p><h2>{s["title"]}</h2><div class="orn">⁂</div>{ps}</section>'
    rest = "".join(f'<li><span>{ROMAN[s["label"]]}.</span>{s["title"]}</li>' for s in TOM[FREE:])
    body = f'''<div class="reader-bar"><div class="reader-bar-in">
  <label class="sr" for="ch">Rozdział</label><select id="ch">{opts_}</select>
  <div class="grp" role="group" aria-label="Wielkość liter"><button data-size="-0.08" aria-label="Mniejsze litery">A−</button><button data-size="0.08" aria-label="Większe litery">A+</button></div>
  <div class="grp" role="group" aria-label="Tło"><button data-theme-btn="jasny">Białe</button><button data-theme-btn="sepia">Papier</button><button data-theme-btn="noc">Noc</button></div>
  <a class="btn sp" href="../tom-1/">Kup cały tom · 29,90 zł</a>
</div><div class="progress"></div></div>
<div class="reader" id="reader" data-theme="sepia"><article>
<p class="intro-meta">Philippe Usyk · Stare małe Dziecko · Tom I: Pusta ławka i Niebo<br>darmowy fragment</p>
{secs}
<section class="locked" id="dalej"><h2>Tu kończy się darmowy fragment</h2>
<p>Stare Małe Dziecko zostało z Ciszą na ławce. Ale minęło wiele dni… W pełnej wersji czeka jeszcze dziesięć rozdziałów i epilog:</p>
<ol>{rest}</ol>
<a class="btn" href="../tom-1/">Kup e-book · 29,90 zł</a>
<p style="margin-top:16px;font-size:1rem !important;opacity:.75">Po zakupie czytasz dalej od rozdziału III, na czytniku, telefonie albo tutaj.</p>
</section>
</article></div>'''
    page("czytaj/", "Czytaj za darmo: Stare małe Dziecko, prolog i rozdziały I–II",
         "Przeczytaj w przeglądarce prolog i dwa pierwsze rozdziały powieści „Stare małe Dziecko. Pusta ławka i Niebo” Philippe’a Usyka. Bez rejestracji.", body)


# ---------- o serii ----------
def o_serii():
    base = "../"
    body = f'''<section class="page-hero">
  <div class="ph-txt"><h1>Kim jest „Stare Małe Dziecko”?</h1><p>Czy można być jednocześnie starym i małym dzieckiem? Można. Bo ta opowieść nie mówi tylko o wieku.</p></div>
  <figure class="ph-art">{img(base, "czytajaca", "Obraz Vilhelma Hammershøia: kobieta czyta list przy oknie", "(max-width:860px) 100vw, 50vw", eager=True)}</figure>
</section>
<section class="sec"><div class="wrap split top">
  <div class="essay">
    <p>To opowieść o człowieku, który przez całe życie pozostaje uczniem. Kiedy jesteśmy młodzi, wydaje nam się, że dorośli znają już wszystkie odpowiedzi. A później sami dorastamy. Mamy pracę, rodzinę, obowiązki. Podejmujemy ważne decyzje.</p>
    <p>I odkrywamy coś niezwykłego: nadal się uczymy. Cierpliwości. Kochania. Przebaczania. Przyznawania się do błędów. Odpowiedzialności za drugiego człowieka. Wiary i zaufania.</p>
    <p>„Stare Małe Dziecko” może mieć kilkanaście lat. Może mieć czterdzieści. Może mieć siedemdziesiąt. Dopóki człowiek potrafi powiedzieć:</p>
    <p class="say">„Nie wiem. Pomyliłem się. Naucz mnie. Spróbuję jeszcze raz.”</p>
    <p>dopóty pozostaje w nim coś z dziecka. Być może najważniejsze pytanie nie brzmi: „Ile masz lat?”, tylko: „Czego życie próbuje cię jeszcze nauczyć?”</p>
  </div>
  <div>
    <h2 style="font-size:2rem">Mistrzowie dawnych rzemiosł</h2>
    <p style="color:var(--ink-2)">Młody człowiek przychodzi do warsztatu, żeby nauczyć się zawodu. Z czasem okazuje się, że warsztat uczy go czegoś więcej.</p>
    <ul class="who">
      <li><b>Kowal</b><span>uczy cierpliwości</span></li>
      <li><b>Zegarmistrz</b><span>uczy szacunku do czasu</span></li>
      <li><b>Rzemieślnik</b><span>pokazuje, że niedokładność ma konsekwencje</span></li>
      <li><b>Mistrz</b><span>wie, że mądrość nie polega na tym, by nigdy się nie pomylić, bo sam kiedyś był uczniem</span></li>
    </ul>
  </div>
</div></section>
<section class="sec wall"><div class="wrap">
  <h2>Bohaterowie serii</h2>
  <p style="color:var(--ink-2);max-width:36em;margin-bottom:36px">Stare Małe Dziecko to nie jeden bohater. To ktoś, kogo każdy z nas nosi w sobie.</p>
  <div class="list2">
    <div><b>Stare Małe Dziecko</b><span>człowiek, który nie chce dorosnąć na tyle, by przestać się dziwić światu</span></div>
    <div><b>Cisza</b><span>bezcielesna i cierpliwa, nie mówi nic, a mówi wszystko</span></div>
    <div><b>Janek</b><span>stolarz z niewielkiego miasteczka, człowiek zwyczajnych dni i zwyczajnych upadków</span></div>
    <div><b>Hanna</b><span>uczy patrzeć oczami nauki, zanim serce zdąży się oszukać własnym uczuciem</span></div>
    <div><b>Profesor Antoni, Helena, ksiądz Tomasz</b><span>astronom, malarka i kapłan z Tomu I</span></div>
    <div><b>Rzemieślnicy i mieszkańcy wsi</b><span>kowale, tkacze, bartnicy, garncarze; ich jedno zdanie waży czasem więcej niż niejedno kazanie</span></div>
  </div>
</div></section>
<section class="sec"><div class="wrap doors">
  <figure>{img(base, "drzwi", "Obraz Vilhelma Hammershøia: otwarte białe drzwi", "(max-width:860px) 100vw, 45vw")}<figcaption class="cap">{cap("drzwi")}</figcaption></figure>
  <div><h2>Kolejne tomy</h2><p style="font-size:1.12rem">Tom I jest już dostępny. Tom II jest w przygotowaniu, a autor pisze kolejne. W przygotowaniu jest także seria „Stara Mała Dziewczynka”, dla osób szukających pogłębienia wiary i duchowej relacji z Bogiem.</p>{NOTIFY.replace("{id}", "seria")}</div>
</div></section>
<section class="sec wall" id="autor"><div class="wrap author">
  <h2>Philippe Usyk</h2>
  <blockquote>„Nauka, kultura i wiara: tutaj usiądą na jednej ławce i nauczą się rozmawiać. Bo prawda, piękno i dobro nie kłócą się ze sobą, to tylko trzy okna wychodzące na to samo Światło.”</blockquote>
  <p style="max-width:40em;margin:0 auto 18px">Autor serii „Stare małe Dziecko”. Pisze o tym, co dzieje się w człowieku, gdy zostaje sam ze swoimi pytaniami. „Stare małe dziecko to ja. I Ty.”</p>
  <p><a class="txt-link" href="{FB}" rel="noopener">Cicha Mądrość na Facebooku</a></p>
</div></section>'''
    page("o-serii/", "O serii „Stare małe Dziecko” – bohaterowie, autor, kolejne tomy | Wydawnictwo Cisza",
         "Kim jest Stare Małe Dziecko? Seria Philippe’a Usyka o człowieku, który przez całe życie pozostaje uczniem: bohaterowie, mistrzowie dawnych rzemiosł i zapowiedź kolejnych tomów.", body, preload="czytajaca")


# ---------- dla parafii i szkół ----------
def instytucje():
    base = "../"
    qs = [
        ("II", "Imię Ciszy", "Mylisz brak z pustką. To nie to samo.", "Czym różni się brak od pustki? Za czym tęsknisz i co ta tęsknota mówi o twoim sercu?"),
        ("V", "Astronom", "Światło przeżywa swoje źródło.", "Czyje dobro wciąż do ciebie dochodzi, choć tej osoby nie ma już obok? Komu ty możesz dziś świecić?"),
        ("VII", "Stary ksiądz", "Nauka mówi ci, jak. Wiara mówi ci, po co.", "Czy spotkałeś się z tym, że trzeba wybierać między rozumem a wiarą? Co odpowiada na to ksiądz Tomasz?"),
        ("X", "Druga ławka", "Serce, które długo czekało na ciepło, czasem samo staje się ciepłem.", "Kto w twojej klasie, rodzinie albo parafii siedzi sam na ławce? Co znaczy „przesunąć się” dla drugiego człowieka?"),
    ]
    qh = "".join(f'<li><b><small>Rozdział {r}</small>{t}</b><div><blockquote>„{c}”</blockquote><p>{q}</p></div></li>' for r, t, c, q in qs)
    body = f'''<section class="page-hero">
  <div class="ph-txt"><h1>Dla parafii, szkół i bibliotek</h1><p>Książka do wspólnego czytania i rozmowy o samotności, wierze, przebaczeniu i odpowiedzialności za drugiego człowieka.</p></div>
  <figure class="ph-art">{img(base, "stol", "Obraz Vilhelma Hammershøia: stół z miską, regał z książkami i krzesło", "(max-width:860px) 100vw, 50vw", eager=True)}</figure>
</section>
<section class="sec"><div class="wrap">
  <h2>Dla kogo</h2>
  <div class="list2" style="margin-top:30px">
    <div><b>Katecheci i nauczyciele</b><span>lektura na lekcję religii, etyki albo godzinę wychowawczą</span></div>
    <div><b>Duszpasterze i parafie</b><span>spotkania grup młodzieżowych, rekolekcje, przygotowanie do bierzmowania</span></div>
    <div><b>Grupy formacyjne</b><span>rozdział tygodniowo i rozmowa w kręgu</span></div>
    <div><b>Biblioteki i szkoły</b><span>e-booki serii do wypożyczania czytelnikom</span></div>
  </div>
</div></section>
<section class="sec wall"><div class="wrap">
  <h2>Przykład materiału do rozmowy</h2>
  <p style="color:var(--ink-2);max-width:36em;margin-bottom:36px">Jedno zdanie z rozdziału i pytania, od których może zacząć się prawdziwa rozmowa.</p>
  <ol class="qs">{qh}</ol>
</div></section>
<section class="sec"><div class="wrap split top">
  <div><h2>Zamówienie dla grupy</h2><p style="font-size:1.12rem;color:var(--ink-2)">Napisz, ile osób będzie czytać i w jakiej formie. Przygotujemy wycenę licencji dla grupy albo biblioteki i odpiszemy e-mailem.</p></div>
  <form class="form-grid" data-ok="ok-inst" novalidate>
    <div class="field full"><label for="i1">Nazwa parafii, szkoły lub biblioteki</label><input id="i1" required></div>
    <div class="field"><label for="i2">Rodzaj</label><select id="i2"><option>Parafia</option><option>Szkoła</option><option>Biblioteka</option><option>Grupa formacyjna</option><option>Inne</option></select></div>
    <div class="field"><label for="i3">Liczba czytelników</label><input id="i3" inputmode="numeric"></div>
    <div class="field full"><label for="i4">E-mail</label><input id="i4" type="email" autocomplete="email" required></div>
    <div class="field full"><label for="i5">Wiadomość</label><textarea id="i5" placeholder="Np. grupa bierzmowanych, 24 osoby, czytamy od listopada"></textarea></div>
    <div class="full"><button class="btn" type="submit">Wyślij zapytanie</button><p class="ok" id="ok-inst">Dziękujemy. Odpiszemy z wyceną na podany e-mail.</p></div>
  </form>
</div></section>'''
    page("dla-parafii-i-szkol/", "Książka dla parafii, szkół i bibliotek – Stare małe Dziecko | Wydawnictwo Cisza",
         "Powieść „Stare małe Dziecko” dla katechetów, nauczycieli, parafii i bibliotek: licencja dla grupy i pytania do rozmowy po rozdziałach.", body, preload="stol")


# ---------- koszyk ----------
def koszyk():
    base = "../"
    body = f'''<div class="wrap"><p class="crumbs"><a href="../">Strona główna</a> / Koszyk</p>
<template id="mini-cover"><img class="thumb" src="../img/okladka.jpg" alt="" width="70" height="105"></template>
<div class="done" id="done">
  <h1 style="font-size:3rem">Dziękujemy za zamówienie</h1>
  <p>To jest wersja demonstracyjna, więc płatność nie została pobrana. W gotowym sklepie stałoby się to tak:</p>
  <ol class="steps"><li>Otwiera się płatność <b id="done-pay">BLIK</b>.</li><li>Po zaksięgowaniu wysyłamy e-mail na <b id="done-mail"></b> z linkami do plików EPUB, MOBI i PDF.</li><li>Prezenty wychodzą do obdarowanych w wybranym dniu, a Ty dostajesz potwierdzenie.</li></ol>
  <p style="margin-top:26px"><a class="btn" href="../czytaj/">Wróć do czytania</a></p>
</div>
<div id="cart-box"><h1 style="font-size:clamp(2.4rem,4vw,3.4rem);margin-top:22px">Koszyk</h1>
<div class="cart">
  <div>
    <div class="cart-lines" id="cart-lines"></div>
    <form id="checkout" novalidate style="margin-top:50px">
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
      <button class="btn" type="submit" style="width:100%">Zamawiam i płacę&nbsp;<span data-sum></span></button>
    </form>
  </div>
  <aside class="summary"><h2>Podsumowanie</h2>
    <div class="row"><span>Produkty</span><span data-sum>0,00 zł</span></div>
    <div class="row"><span>Dostawa e-mailem</span><span>0,00 zł</span></div>
    <div class="row" style="color:var(--muted);font-size:.95rem"><span>w tym VAT 5%</span><span data-vat>0,00 zł</span></div>
    <div class="row total"><span>Razem</span><span data-sum>0,00 zł</span></div>
    <p style="color:var(--muted);font-size:.92rem;margin:14px 0 0">Ceny w demo są przykładowe.</p>
  </aside>
</div></div></div>'''
    page("koszyk/", "Koszyk | Wydawnictwo Cisza", "Koszyk sklepu Wydawnictwa Cisza.", body, extra_head='\n<meta name="robots" content="noindex">')


def extras():
    (ROOT / "favicon.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="3" fill="#24221e"/><text x="16" y="24" text-anchor="middle" font-family="Georgia,serif" font-size="22" fill="#f2eee5">C</text></svg>', encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {URL}sitemap.xml\n", encoding="utf-8")
    urls = ["", "tom-1/", "czytaj/", "o-serii/", "dla-parafii-i-szkol/"]
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
                                      "".join(f"  <url><loc>{URL}{u}</loc></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")


home(); tom1(); czytaj(); o_serii(); instytucje(); koszyk(); extras()
print("ok")
