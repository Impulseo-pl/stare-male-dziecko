# Stare małe Dziecko – demo sklepu z e-bookami (Wydawnictwo CISZA)

Klient: autor Philippe Usyk, seria „Stare małe Dziecko” (FB „Cicha Mądrość”: https://www.facebook.com/profile.php?id=61593939705947).
Demo: https://impulseo-pl.github.io/stare-male-dziecko/ (sprawdzamy **zawsze z `?team=1`**).

Źródła treści: PDF Tomu I (`Downloads\Stare Male Dziecko Tom_I.pdf`, 54 s.) + opis grup docelowych i post FB od klienta (07.10.2026).
Cen klient nie podał – w demo przykładowe (29,90 / Klub 24,90 za tom), oznaczone na stronie. Okładka robocza w SVG.
Liczby „540 tomów” z FB celowo nie używamy (klient pisze też, że dopiero je napisze).

Podstrony: główna, /tom-1/ (karta produktu, prezent z dedykacją), /czytaj/ (czytnik: prolog + rozdz. I–II, sepia/noc, A−/A+),
/o-serii/, /dla-parafii-i-szkol/ (pytania do rozmowy, zapytanie grupowe), /koszyk/ (localStorage, BLIK/P24/karta, zgoda na treść cyfrową, VAT 5%).

Budowanie: `python _src/wyciagnij.py` (PDF -> `_src/tom1.json`), `python _src/build.py` (strony).
Zrzuty: `python _src/shots.py 1440|390` (serwer `python -m http.server 8125` z `C:\Users\kluch`).

## v2 (08.10.2026): nowy projekt po „widać AI slop”
v1 (granatowe niebo, gwiazdy, rysowana ławka w SVG, złote przyciski, 3 karty cen) odrzucona.
v2 = wygląd wydawnictwa literackiego: obrazy Vilhelma Hammershøia (domena publiczna, Commons) zamiast rysunków,
EB Garamond + Public Sans, czerń/szarość ścian/papier, jeden akcent (ceglasta czerwień). Okładka jako komponent CSS (`.book`),
rozkładówka prologu, spis treści z numerami stron z PDF, oferty jako lista z radiem. `img/okladka.jpg` i `img/og.jpg` to zrzuty.

## Flipbook (08.10.2026)
Klient poprosił o „interaktywną książkę” (Heyzine/Flipsnack). Zrobione u nas: StPageFlip 2.0.7 (MIT, `assets/page-flip.browser.js`, bez abonamentu),
strony z PDF renderowane PyMuPDF do `img/strony/` (okładka s01, s02, s04–s19 = do końca rozdz. II), sekcja #fragment na stronie głównej.
