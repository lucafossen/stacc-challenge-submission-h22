# Stacc code challenge 2021 - Luca Blaauw Fossen

#### *English tldr: I submitted a Flask web app to stacc's semesterly [code challenge](https://github.com/stacc/stacc-code-challenge-public)*

## Oppgavebeskrivelse
Hei! Jeg har laget en web-app som lar brukere sende inn søknader om lån. En sjekk blir gjort for å se om de er politisk eksponerte personer, og deres data blir lagret. Ansatte kan også se alle søknader som har blitt sendt inn.

## Hvordan kjøre prosjektet
### Du trenger:
* Python (testet på 3.10.7)
   * https://www.python.org/downloads/
* Flask (testet på 2.2.2)
   * `pip install flask`
* requests (testet på 2.28.1)
   * `pip install requests`

### For å kjøre:
* Naviger til rotkatalogen, og kjør `flask run`.
* Siden kjører ved default på http://127.0.0.1:5000/.

## Kommentarer

Dette var mitt første skikkelige prosjekt med Flask (og web-utvikling generelt for den del) så jeg var ganske usikker på hvor mye jeg kom til å klare på en helg! Jeg er uerfaren med web-utvikling, så det har vært mye prøving og feiling (spesielt på CSS-fronten).
Jeg ble glad i Flask! Det viste seg å være ganske lett å sende data frem og tilbake med hjelp av den innebygde template-motoren, [Jinja](https://jinja.palletsprojects.com/en/3.1.x/).

Jeg har holdt på med appen en stund nå, og har fortsatt lyst å lage en side for en "Ansatt", som kan se de ulike søknadene som har kommet inn og godta/avslå dem. Men det blir om jeg får nok tid! (edit: jeg fikk til å vise søknadene(!), men har ikke prøvd meg på godta/avslå funksjonaliteten!)

Jeg har prøvd å unngå bruk av JavaScript, ettersom jeg ikke har særlig erfaring med språket og hadde allerede tatt et dykk inn i Flask.

De rike fargene er jo ikke nødvendigvis bank-aktig, men jeg hadde lyst å sette min egen rare vri på siden. Den skal jo tross alt ikke brukes av kunder!

Jeg fant nylig ut at [Flask støtter form-validering](https://flask-wtf.readthedocs.io/en/1.0.x/), så i fremtiden hadde jeg nok brukt dette istedenfor å validere manuelt i Python, men det er god lærdom!