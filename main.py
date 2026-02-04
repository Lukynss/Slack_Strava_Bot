import os
from datetime import datetime
from time import strptime
import re
import requests
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
from strava_cz import StravaCZ, MealType, OrderType

# Načte klíče ze souboru .env
load_dotenv()

# Inicializace bota
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

cisloJidelny = "kod vaší jídelny"
strava = StravaCZ(
    username="vaše username",
    password="vaše password",
    canteen_number=cisloJidelny
)


@app.message(re.compile("menu", re.IGNORECASE))
def say_menu(message, say):
    say("Momentík, stahuju celý jídelníček... 📜")

    try:
        cookies = {
            'NEXT_LOCALE': 'en',
            'multiContextSession': '%7B%22printOpen%22%3A%7B%22value%22%3Afalse%2C%22expiration%22%3A-1%7D%2C%22lastUser%22%3A%7B%22value%22%3A%22%7B%5C%22jmeno%5C%22%3A%20%5C%22svasek.lukas%5C%22%2C%20%5C%22cislo%5C%22%3A%5C%2210343%5C%22%7D%22%2C%22expiration%22%3A1769830514481%7D%7D',
            'multiContext': '%7B%7D',
        }
        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.7',
            'content-type': 'text/plain;charset=UTF-8',
            'origin': 'https://app.strava.cz',
            'priority': 'u=1, i',
            'referer': 'https://app.strava.cz/en',
            'sec-ch-ua': '"Brave";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
        }
        data_payload = '{"cislo":"10343","sid":"A43AHJDKSV","s5url":"","lang":"EN","konto":0,"podminka":"","ignoreCert":"false"}'

        response = requests.post('https://app.strava.cz/api/objednavky', cookies=cookies, headers=headers,
                                 data=data_payload)
        json_data = response.json()

        vystup = "🍴 *Aktuální jídelníček na příští měsíc 📆:*\n"

        for key, items in json_data.items():
            if isinstance(items, list) and len(items) > 0:
                datum = items[0]['datum']

                vystup += "\n➖➖➖➖➖➖➖➖➖➖➖\n"
                vystup += f"📅 *{datum}*\n"

                for meal in items:
                    nazev = meal['nazev']
                    druh = meal.get('druh_popis', 'jidlo')

                    if "polévka" in druh.lower() or "polevka" in druh.lower():
                        ikona = "🥣"
                    else:
                        ikona = "🥘"

                    vystup += f"  {ikona} *{nazev}*\n"

        say(vystup)
    except Exception as e:
        print(f"CHYBA: {e}")
        say(f"Něco se pokazilo: {e}")


@app.message(re.compile("week", re.IGNORECASE))
def say_menu_week(message, say):
    say("Momentík, stahuju menu na týden... 📅")

    try:
        cookies = {
            'NEXT_LOCALE': 'en',
            'multiContextSession': '%7B%22printOpen%22%3A%7B%22value%22%3Afalse%2C%22expiration%22%3A-1%7D%2C%22lastUser%22%3A%7B%22value%22%3A%22%7B%5C%22jmeno%5C%22%3A%20%5C%22svasek.lukas%5C%22%2C%20%5C%22cislo%5C%22%3A%5C%2210343%5C%22%7D%22%2C%22expiration%22%3A1769830514481%7D%7D',
            'multiContext': '%7B%7D',
        }
        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.7',
            'content-type': 'text/plain;charset=UTF-8',
            'origin': 'https://app.strava.cz',
            'priority': 'u=1, i',
            'referer': 'https://app.strava.cz/en',
            'sec-ch-ua': '"Brave";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
        }
        data_payload = '{"cislo":"10343","sid":"A43AHJDKSV","s5url":"","lang":"EN","konto":0,"podminka":"","ignoreCert":"false"}'

        response = requests.post('https://app.strava.cz/api/objednavky', cookies=cookies, headers=headers,
                                 data=data_payload)
        json_data = response.json()

        vystup = "🍴 *Jídelníček na tento týden:*\n"

        pocet_dni = 0
        delka_commandu = 4

        for key, items in json_data.items():
            if isinstance(items, list) and len(items) > 0:
                if pocet_dni > delka_commandu:
                    break

                datum = items[0]['datum']

                vystup += "\n➖➖➖➖➖➖➖➖➖➖➖\n"
                vystup += f"📅 *{datum}*\n"

                for meal in items:
                    nazev = meal['nazev']
                    druh = meal.get('druh_popis', 'jidlo')

                    if "polévka" in druh.lower() or "polevka" in druh.lower():
                        ikona = "🥣"
                    else:
                        ikona = "🥘"

                    vystup += f"  {ikona} *{nazev}*\n"

                pocet_dni += 1

        say(vystup)

    except Exception as e:
        print(f"CHYBA: {e}")
        say(f"Něco se pokazilo: {e}")


@app.message(re.compile("today", re.IGNORECASE))
def say_today(message, say):
    say("Momentík, kouknu co je dnes... 🍽️")

    try:
        cookies = {
            'NEXT_LOCALE': 'en',
            'multiContextSession': '%7B%22printOpen%22%3A%7B%22value%22%3Afalse%2C%22expiration%22%3A-1%7D%2C%22lastUser%22%3A%7B%22value%22%3A%22%7B%5C%22jmeno%5C%22%3A%20%5C%22svasek.lukas%5C%22%2C%20%5C%22cislo%5C%22%3A%5C%2210343%5C%22%7D%22%2C%22expiration%22%3A1769830514481%7D%7D',
            'multiContext': '%7B%7D',
        }
        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.7',
            'content-type': 'text/plain;charset=UTF-8',
            'origin': 'https://app.strava.cz',
            'priority': 'u=1, i',
            'referer': 'https://app.strava.cz/en',
            'sec-ch-ua': '"Brave";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
        }
        data_payload = '{"cislo":"10343","sid":"A43AHJDKSV","s5url":"","lang":"EN","konto":0,"podminka":"","ignoreCert":"false"}'

        response = requests.post('https://app.strava.cz/api/objednavky', cookies=cookies, headers=headers,
                                 data=data_payload)
        json_data = response.json()

        vystup = "🍴 *Dnešní nabídka:*\n"

        pocet_dni = 0
        delka_commandu = 0

        for key, items in json_data.items():
            if isinstance(items, list) and len(items) > 0:
                if pocet_dni > delka_commandu:
                    break

                datum = items[0]['datum']

                vystup += "\n➖➖➖➖➖➖➖➖➖➖➖\n"
                vystup += f"📅 *{datum}*\n"

                for meal in items:
                    nazev = meal['nazev']
                    druh = meal.get('druh_popis', 'jidlo')

                    if "polévka" in druh.lower() or "polevka" in druh.lower():
                        ikona = "🥣"
                    else:
                        ikona = "🥘"

                    vystup += f"  {ikona} *{nazev}*\n"

                pocet_dni += 1
        say(vystup)
    except Exception as e:
        print(f"CHYBA: {e}")
        say(f"Něco se pokazilo: {e}")


@app.message(re.compile("balance", re.IGNORECASE))
def say_balance(message, say):
    try:
        say(f"💰 Zůstatek na účtě: *{strava.user.balance} Kč*")
    except:
        say("💰 Zůstatek: _(nepodařilo se zjistit)_")


@app.message(re.compile("help", re.IGNORECASE))
def say_help(message, say):
    vystup = (
        "ℹ️ *Seznam dostupných příkazů:*\n\n"
        "💰 *balance* – vypíše aktuální zůstatek\n"
        "📅 *week* – vypíše menu na tento týden\n"
        "📜 *menu* – vypíše celé dostupné menu (na měsíc)\n"
        "🍽️ *today* – vypíše, co vaří dnes\n"
        "🏫 *cislo jidelny* – vypíše číslo tvé jídelny\n"
        "👤 *jmeno jidelny* – vypíše název jídelny"
    )
    say(vystup)


@app.message(re.compile("cislo jidelny", re.IGNORECASE))
def say_jidelna(message, say):
    say(f"🏫 Jídelna, kam chodíš, má číslo: *{cisloJidelny}*")


@app.message(re.compile("jmeno jidelny", re.IGNORECASE))
def say_ucet(message, say):
    say(f"👤 Na obědy chodíš do: *{strava.user.canteen_name}*")


if __name__ == "__main__":
    print("Bot běží...")
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()