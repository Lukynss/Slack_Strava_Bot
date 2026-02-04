# 🤖 StravaCZ Slack Bot

Vítej u mého studentského projektu! 👋

Tohle je **Slack bot** napsaný v Pythonu, který umí zjistit, co je dnes (nebo celý týden) k obědu ve tvé jídelně na portálu [Strava.cz](https://www.strava.cz/).

Protože oficiální knihovny na mojí jídelně nefungovaly, napsal jsem si **vlastní scraper**, který tahá data přímo z API jídelny.

## 🚀 Co bot umí?
- **`today`** – Vypíše dnešní oběd 🍽️
- **`week`** – Vypíše jídelníček na celý týden 📅
- **`menu`** – Stáhne kompletní dostupný jídelníček (třeba na měsíc) 📜
- **`balance`** – Zobrazí aktuální zůstatek na účtu 💰
- **`help`** – Zobrazí nápovědu

## ⚠️ DŮLEŽITÉ: Nastavení IDček (Jak to zprovoznit)

Aby bot fungoval na tvoji jídelnu a tvůj účet, **musíš do kódu vložit své vlastní údaje**. Bot funguje tak, že se tváří jako tvůj prohlížeč, takže potřebuje tvoje sušenky (cookies).

### 1. Získání údajů
1. Otevři v prohlížeči Strava.cz a přihlas se.
2. Otevři vývojářské nástroje (**F12** -> záložka **Network**).
3. Klikni v jídelníčku na nějaký den nebo obnov stránku.
4. Najdi požadavek na `objednavky` (nebo podobný API call).
5. Zkopíruj si **Cookie** hlavičku a payload data (hlavně `sid` a číslo jídelny).

### 2. Úprava `main.py`
Otevři soubor `main.py` a najdi tuto část (přibližně řádek 20-40). **Musíš přepsat hodnoty svými údaji:**

```python
# Příklad:
cisloJidelny = "12345"  # <-- TADY DEJ ČÍSLO SVÉ JÍDELNY

# Ve funkci stahni_data():
cookies = {
    # ... zkopíruj sem své cookies z prohlížeče ...
}

data_payload = '{"cislo":"12345","sid":"TVOJE_SESSION_ID", ...}' # <-- TADY MUSÍŠ DÁT SVÉ SID
