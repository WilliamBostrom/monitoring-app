# Python DevOps Slutuppgift - Systemövervakning

## Rapportmall: Systemutveckling i Python – Individuell slutuppgift

### Studentinformation

- **Namn:** William Boström
- **Klass:** doe25
- **Datum:** 2025-10-20
- **GitHub-länk:** https://github.com/WilliamBostrom/monitoring-app

## 1. Inledning

I denna uppgift har jag utvecklat en övervakningsapplikation i Python som samlar in systeminformation och visar den i terminalen. Programmet kan starta övervakning, visa status, skapa och visa larm, samt hantera övervakningsläge. Syftet är att visa hur man kan använda Python för systemutveckling inom DevOps, med fokus på struktur, funktioner och objektorientering.

## 2. Planering och design

Jag började med att läsa igenom kravspecifikationen och dela upp den i fem huvuddelar: starta övervakning, visa status, skapa larm, visa larm och starta övervakningsläge. Jag ritade sedan ett enkelt flöde över hur användaren navigerar i menyn och vilka funktioner som behövs.

## 3. Programstruktur

Programmet är uppdelat i flera filer. Filen `main.py` innehåller huvudmenyn och startpunkten. Klassen `Alarm` ansvarar för larmlogik, medan `AlarmManager` håller reda på alla aktiva larm och sparar dem till JSON-fil. Systeminformation hämtas via `utils/system_info.py` med hjälp av biblioteket psutil.

## 4. Viktiga funktioner eller klasser

**AlarmManager-klassen** har metoden `check_alarms()` som kontrollerar om några larm är aktiverade baserat på aktuell systemanvändning. Jag valde att använda en klass för att kunna återanvända samma kod både i menyn och i övervakningsläget.

**alarm_monitor()-funktionen** kör kontinuerlig övervakning med 2-sekunders intervall och visar varningar när larm triggas.

## 5. Bibliotek och verktyg

- **psutil** – för att läsa systemresurser (CPU, minne, disk)
- **json** – för att spara och läsa in larm till fil
- **time** – för att skapa loopar i övervakningsläget
- **os** – för filhantering

**Git och GitHub:** Projektet versionshanteras med Git. Huvudkoden finns i main-branchen, medan en frontend-implementation i Svelte finns i `frontend`-branchen. Frontend kan köras med Docker genom att uppdatera URL:en från Raspberry Pi IP till localhost.

## 6. Testa terminalversionen

För att köra applikationen:

```bash
# Navigera till projektmappen
cd monitoring-app

# Sätt Python-version (om du använder pyenv)
pyenv shell 3.12.11

# Installera dependencies
pip install -r requirements.txt

# Starta applikationen
python main.py
```

Applikationen startar med en meny där du kan:

- Starta systemövervakning
- Visa aktuell status
- Skapa larm (CPU, minne, disk)
- Visa befintliga larm
- Editera/ta bort larm
- Starta övervakningsläge med kontinuerlig monitoring

## 7. Testning och felsökning

Jag testade alla menyval manuellt genom att köra programmet i terminalen. För att undvika krascher använde jag try/except vid inmatning av siffror. Jag lade även till print()-utskrifter för att förstå flödet och debugga cirkulära imports.

## 8. Resultat

Jag är nöjd med hur programmet hanterar flera larm samtidigt och sparar dem persistent till JSON-fil. Menystrukturen är tydlig och användarvänlig med svenska texter.

## 9. Reflektion och lärdomar

Jag har lärt mig mycket om hur klasser gör program mer strukturerade och lättare att underhålla. Jag har även förstått vikten av att planera innan man börjar koda och att använda Git ofta för att undvika konflikter.

## 10. Möjliga förbättringar och vidareutveckling

Jag skulle vilja lägga till e-postnotifiering vid aktiverat larm och förbättra frontend-implementationen. Jag skulle också vilja skriva enhetstester för vissa funktioner.

## 11. Sammanfattning

Projektet visar hur man kan använda Python för att skapa en enkel men effektiv övervakningsapplikation. Jag har tillämpat objektorientering, filhantering, felhantering och versionshantering i praktiken. Frontend-implementationen i Svelte visar även hur samma backend kan användas för webbapplikationer.

## 12. Docker, Nginx och Frontend-implementation

Projektet inkluderar en komplett webbapplikation med Docker-containerisering och Nginx-proxy. Frontend-implementationen finns i `frontend`-branchen och är byggd med SvelteKit + TypeScript.

**Teknisk stack:**

- **Frontend:** SvelteKit + Vite + TypeScript
- **Backend:** Python med FastAPI + Uvicorn ASGI-server
- **Proxy:** Nginx för API-routing
- **Containerisering:** Docker Compose för hela stacken

**Docker-struktur:**

- `frontend` container: Servar SvelteKit-appen
- `nginx` container: Proxy på port 3000
- `backend` container: Python API på port 8000

**Snabbstart:**

```bash
# Lokal utveckling
git checkout feature/10-frontend
cd frontend && npm install && npm run dev
cd monitoring-app && uvicorn main:app --reload

# Docker
docker compose up --build
```

**Hosting:** Applikationen är hostad på en Raspberry Pi med automatisk deployment via Docker. Nginx fungerar som reverse proxy och routar API-anrop till backend-containern. Säkerheten säkerställs genom Tailscale VPN med SSH-tunnel, vilket gör att endast jag kan komma åt Raspberry Pi sidan från min mobil och dator. För lokal testning ändra API URL i frontend/src/config.ts från "ip adressen" till "localhost".

Detaljerade instruktioner finns i README-filen i `frontend`-branchen.
