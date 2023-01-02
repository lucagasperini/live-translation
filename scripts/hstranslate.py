# Copyright (C) 2022 Luca Gasperini <luca.gasperini@xsoftware.it>
#
# This file is part of Live Translation.
#
# Live Translation is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Live Translation is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Live Translation.  If not, see <http://www.gnu.org/licenses/>.

from urllib.request import urlopen, Request
import json
import sys

HSJSON_ENDPOINT = "https://api.hearthstonejson.com/v1/latest"

SOURCE_LANG = "itIT"
TARGET_LANG = ["itIT", "zhCN"]


def translate_startup(lang):
    cards_url = f"{HSJSON_ENDPOINT}/{lang}/cards.json"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    req = Request(url=cards_url, headers=headers)
    cards_file = urlopen(req).read().decode("utf8")

    return json.loads(cards_file)


def find_set_request(lang, cards, searchkey):
    result = dict()
    for l in lang:
        result[l] = []
        for card in cards[l]:
            if card["set"].lower() == searchkey.lower():
                result[l].append(card)

    return result


def find_name_request(lang, cards, searchkey):
    key = searchkey.lower()
    result = dict()
    for l in lang:
        result[l] = []
        for card in cards[l]:
            if key in card["name"].lower():
                result[l].append(card)

    return result


def id_request(lang, cards, searchkey):

    for card in cards[lang]:
        if int(card["dbfId"]) == int(searchkey):
            return card

    return False


def name_by_id_request(lang, cards, searchkey):

    for card in cards[lang]:
        if int(card["dbfId"]) == int(searchkey):
            return card["name"]

    return False


def id_by_name_request(lang, cards, searchkey):
    for card in cards[lang]:
        if card["name"] == searchkey:
            return str(card["dbfId"])
    return False


def main():
    cards = dict()

    cards[SOURCE_LANG] = translate_startup(SOURCE_LANG)

    for lang in TARGET_LANG:
        cards[lang] = translate_startup(lang)

    searchkey = True
    buffer = None

    while searchkey:
        searchkey = input()
        if searchkey[0] == "!":
            buffer = None
            continue

        if searchkey[0] == "/":
            tmp = find_name_request(TARGET_LANG, cards, searchkey[1:])
            for card in tmp[SOURCE_LANG]:
                print(f"{card['dbfId']}: {card['name']}")
            continue

        if searchkey[0] == "$":
            # $BATTLEGROUNDS
            buffer = find_set_request(
                TARGET_LANG, cards, searchkey[1:])
            continue

        if searchkey[0] == "=":
            if searchkey[1:]:
                lang = searchkey[1:]
            else:
                lang = SOURCE_LANG

            for card in buffer[lang]:
                print(f"{card['dbfId']}: {card['name']}")
            continue

        if searchkey[0] == ":":
            card = id_request(SOURCE_LANG, buffer, searchkey[1:])
            print(card)
            continue

        if buffer == None:
            buffer = cards

        if not searchkey.isnumeric():
            card_id = id_by_name_request(SOURCE_LANG, buffer, searchkey)
        else:
            card_id = searchkey

        for lang in TARGET_LANG:
            name = name_by_id_request(lang, buffer, card_id)
            print(f"{lang}: {name}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
