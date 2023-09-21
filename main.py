import math
from collections import defaultdict, Counter

from StringProgressBar import progressBar

import telebot
from telebot import types


UNIKAJ_IDENTIGILOJ = defaultdict(set)
LITERA_KIOMO = defaultdict(lambda: defaultdict(int))
LITERA_OFTO = defaultdict(lambda: defaultdict(Counter))
MESAGXA_KIOMO = defaultdict(lambda: defaultdict(int))


with open("token.cfg", "r", encoding="utf-8") as f:
    token = f.read().rstrip()


bot = telebot.TeleBot(token)


def kalkuli_na_entropio(ofto, kiomo):
    entropio = 0
    for k in ofto:
        try:
            probablo = ofto[k] / kiomo
            entropio += probablo * int(math.log2(1/probablo))
        except ZeroDivisionError:
            entropio = 0
    return entropio


def kunigi_po(sxovo, teksto, apartigilo='\n'):
    partfrazaro = teksto.split('\n')
    plenfrazaro = ['\n'.join(partfrazaro[i:i+sxovo]) for i in range(0, len(partfrazaro), sxovo)]
    return plenfrazaro


def taksi(proporciaro, tuta_mesagxa_kiomo, tuta_litera_kiomo):

    teksto = f"The analysis based on {tuta_mesagxa_kiomo} of messages and {tuta_litera_kiomo} of letters:\n"
    for uzantnomo, procento, baro, entropio in proporciaro:
        teksto += f"{uzantnomo}: {procento}% with {entropio} of randomness\n"
        teksto += f"{baro}\n"

    return teksto


def konkludi(proporciaro):
    
    teksto = ""
    sxercaro = [
        "👀 The ideal quantum ghoster 👀\n",
        "💀 To be, or not to be, that is the question! 💀\n",
        "☢  Hazardous correlation, not causation ☢\n",
        "🚃 Here comes the train driver! 🚃\n",
        "🛸 I am ready to pilot UFO with you 🛸\n",
        "🌠 Couples look at the shooting stars 🌠\n",
        "🌌 To infinity and beyond! 🌌\n",
        "🌙 The moon is beautiful, isn't it? 🌙\n",
        "🎃 You are at some intrigant wizard 🎃\n",
        "👻 You are visiting a phantom land, traveller! 👻\n",
        "☠️  Abandon hope all ye who enter here. ☠️\n",
        "💯 It's over, isn't it? 💯\n",
    ]

    for uzantnomo, procento, _, _ in proporciaro:
        match procento:
            case 0: grado = -1
            case _: grado = int(procento // 10)
        teksto += f"La ŝercfrazo pri {uzantnomo}:\n"
        teksto += sxercaro[grado + 1]
    
    konkludaro = kunigi_po(2, teksto)
    
    return konkludaro[:-1]


@bot.message_handler(commands=['start'])
def komenci(message):

    global UNIKAJ_IDENTIGILOJ
    global MESAGXA_KIOMO
    global LITERA_KIOMO
    global LITERA_OFTO

    identigilo = message.from_user.id

    UNIKAJ_IDENTIGILOJ[identigilo].clear()
    MESAGXA_KIOMO[identigilo].clear()
    LITERA_KIOMO[identigilo].clear()
    LITERA_OFTO[identigilo].clear()

    bonvenaro = [
        "Hello, I am a bot analysing conversations, made to measure the writing relation in your relationship!\n",
        "/start for (re)start!\n",
        "/k to calculate the relation and conclusions\n",
        "/m to see all possible conclusions\n",
    ]
    teksto = f"{bonvenaro[0]}{bonvenaro[1]}{bonvenaro[2]}{bonvenaro[3]}"
    bot.send_message(message.from_user.id, teksto)


@bot.message_handler(commands=['m'])
def montri(message):

    proporciaro = [[f"{i}%", i, None, None] for i in range(0, 101, 10)]
    konkludaro = konkludi(proporciaro)
    for konkludo in konkludaro:
        bot.send_message(message.from_user.id, konkludo)


@bot.message_handler(commands=['k'])
def kalkuli(message):

    global UNIKAJ_IDENTIGILOJ
    global MESAGXA_KIOMO
    global LITERA_KIOMO
    global LITERA_OFTO

    identigilo = message.from_user.id
    
    unikaj_identigiloj = UNIKAJ_IDENTIGILOJ[identigilo]
    mesagxa_kiomo = MESAGXA_KIOMO[identigilo]
    litera_kiomo = LITERA_KIOMO[identigilo]
    litera_ofto = LITERA_OFTO[identigilo]

    foriguzantoj = []
    for uzanto in unikaj_identigiloj:
        uzantkasxnomo, uzantnomo = uzanto
        if uzantkasxnomo is not None and uzantkasxnomo.endswith("bot"):
                del mesagxa_kiomo[uzantnomo]
                del litera_kiomo[uzantnomo]
                del litera_ofto[uzantnomo]
                foriguzantoj.append(uzanto)
    for uzanto in foriguzantoj:
       unikaj_identigiloj.remove(uzanto)

    tuta_mesagxa_kiomo = sum(mesagxa_kiomo.values())
    tuta_litera_kiomo = sum(litera_kiomo.values())
    
    proporciaro = []
    for (uzantkasxnomo, uzantnomo) in unikaj_identigiloj:
        entropio = kalkuli_na_entropio(litera_ofto[uzantnomo], litera_kiomo[uzantnomo])
        baro, procento = progressBar.filledBar(tuta_litera_kiomo, litera_kiomo[uzantnomo], size=25)
        procento = round(procento, 1)
        entropio = round(entropio, 1)
        proporciaro.append([uzantnomo, procento, baro, entropio])
    proporciaro.sort(key=lambda l: l[1], reverse=True)
    
    takso = taksi(proporciaro, tuta_mesagxa_kiomo, tuta_litera_kiomo)
    bot.send_message(message.from_user.id, takso)

    konkludaro = konkludi(proporciaro)
    for konkludo in konkludaro:
        bot.send_message(message.from_user.id, konkludo)


@bot.message_handler(content_types="text")
def get_text_messages(message):
    
    global UNIKAJ_IDENTIGILOJ
    global MESAGXA_KIOMO
    global LITERA_KIOMO
    global LITERA_OFTO

    identigilo = message.from_user.id
    try:
        uzantkasxnomo = message.forward_from.username
        uzantnomo = message.forward_from.first_name
    except AttributeError:
        uzantkasxnomo = "@anonimo"
        uzantnomo = "Anonimo"
    uzanto = (uzantkasxnomo, uzantnomo)
    mesagxa_teksto = message.text
    mesagxa_longo = len(mesagxa_teksto)
    
    UNIKAJ_IDENTIGILOJ[identigilo].add(uzanto)
    LITERA_KIOMO[identigilo][uzantnomo] += mesagxa_longo
    LITERA_OFTO[identigilo][uzantnomo].update(mesagxa_teksto)
    MESAGXA_KIOMO[identigilo][uzantnomo] += 1


def main():
    bot.infinity_polling()


if __name__ == "__main__":
    main()
