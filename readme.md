<<<<<<< Updated upstream

# Python DevOps Slutuppgift - Systemövervakning

## Projektstatus: 4:e Oktober

### ✅ Genomförda delar (G-nivå):

**Krav 1-2: Grundläggande övervakning** ✅

- Starta övervakning - Live-övervakning av CPU, minne och disk
- Lista aktiv övervakning - Snapshot med procent och GB-information

**Teknisk struktur** ✅

- Modulär kodstruktur (flera filer)
- Funktionell programmering
- Svenska användargränssnitt

### 📋 Kvar att implementera (G-nivå):

**Krav 3-5: Larmhantering**

- Skapa larm (CPU/minne/disk med procentuell nivå)
- Visa larm (sorterade efter typ)
- Starta övervakningsläge (kontinuerlig övervakning med larmvarningar)

### VG-nivå (valfritt):

- Loggning av alla händelser
- Ta bort larm
- # Persistera larm till disk (JSON)

# Python DevOps Slutuppgift - Systemövervakning

## Projektstatus: 8:e Oktober

### ✅ **GODKÄND NIVÅ - ALLA KRAV UPPFYLLDA** ✅

**Krav 1-2: Grundläggande övervakning** ✅

- Starta övervakning - Live-övervakning av CPU, minne och disk
- Lista aktiv övervakning - Snapshot med procent och GB-information

**Krav 3-5: Larmhantering** ✅

- Skapa larm (CPU/minne/disk med procentuell nivå) - Med validering 1-100%
- Visa larm (sorterade efter typ) - Alfabetisk sortering med lambda-funktioner
- Starta övervakningsläge (kontinuerlig övervakning med larmvarningar) - Med Enter/Ctrl+C avslut

**Teknisk struktur** ✅

- Modulär kodstruktur (flera filer) - 7 aktiva filer
- Objektorienterad programmering - Alarm-klass implementerad
- Funktionell programmering - Lambda-funktioner för sortering
- Svenska användargränssnitt
- Välskriven kod med tydliga variabelnamn och kommentarer
- Input sanitization - Validering av användarinput
- Bugfri funktionalitet

**Arkitektur:**

- `main.py` - Programstart
- `menus/menu.py` - Huvudmeny och navigation
- `menus/larm_menu.py` - Larm-skapande meny
- `alarms/alarm.py` - Alarm-klass och övervakningslogik
- `monitoring/monitoring.py` - Övervakningsfunktioner
- `utils/system_info.py` - Systemdata-hämtning
- `utils/monitoring_display.py` - Display-funktioner
- `utils/utils.py` - Hjälpfunktioner

### VG-nivå (valfritt):

- Loggning av alla händelser
- Ta bort larm
- Persistera larm till disk (JSON)
  > > > > > > > Stashed changes
