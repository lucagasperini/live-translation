# Copyright (C) 2021 Luca Gasperini <luca.gasperini@xsoftware.it>
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


lang_dict = {"ab": "Abkhazian", "sq": "Albanian", "ak": "Akan", "ar": "Arabic", "an": "Aragonese", "am": "Amharic", "as": "Assamese", "az": "Azerbaijani", "ast": "Asturian", "nch": "Central Huasteca Nahuatl", "ee": "Ewe", "ay": "Aymara", "ga": "Irish", "et": "Estonian", "oj": "Ojibwa", "oc": "Occitan", "or": "Oriya", "om": "Oromo", "os": "Ossetian", "tpi": "Tok Pisin", "ba": "Bashkir", "eu": "Basque", "be": "Belarusian", "ber": "Berber languages", "bm": "Bambara", "pag": "Pangasinan", "bg": "Bulgarian", "se": "Northern Sami", "bem": "Bemba (Zambia)", "byn": "Blin", "bi": "Bislama", "bal": "Baluchi", "is": "Icelandic", "pl": "Polish", "bs": "Bosnian", "fa": "Persian", "bho": "Bhojpuri", "br": "Breton", "ch": "Chamorro", "cbk": "Chavacano", "cv": "Chuvash", "ts": "Tsonga", "tt": "Tatar", "da": "Danish", "shn": "Shan", "tet": "Tetum", "de": "German", "nds": "Low German", "sco": "Scots", "dv": "Dhivehi", "kdx": "Kam", "dtp": "Kadazan Dusun", "ru": "Russian", "fo": "Faroese", "fr": "French", "sa": "Sanskrit", "fil": "Filipino", "fj": "Fijian", "fi": "Finnish", "fur": "Friulian", "fvr": "Fur", "kg": "Kongo", "km": "Khmer", "ngu": "Guerrero Nahuatl", "kl": "Kalaallisut", "ka": "Georgian", "gos": "Gronings", "gu": "Gujarati", "gn": "Guarani", "kk": "Kazakh", "ht": "Haitian", "ko": "Korean", "ha": "Hausa", "nl": "Dutch", "cnr": "Montenegrin", "hup": "Hupa", "gil": "Gilbertese", "rn": "Rundi", "quc": "K'iche'", "ky": "Kirghiz", "gl": "Galician", "ca": "Catalan", "cs": "Czech", "kab": "Kabyle", "kn": "Kannada", "kr": "Kanuri", "csb": "Kashubian", "kha": "Khasi", "kw": "Cornish", "xh": "Xhosa", "co": "Corsican", "mus": "Creek", "crh": "Crimean Tatar", "tlh": "Klingon", "hbs": "Serbo-Croatian", "qu": "Quechua", "ks": "Kashmiri", "ku": "Kurdish", "la": "Latin", "ltg": "Latgalian", "lv": "Latvian", "lo": "Lao", "lt": "Lithuanian", "li": "Limburgish", "ln": "Lingala", "lg": "Ganda", "lb": "Letzeburgesch",
             "rue": "Rusyn", "rw": "Kinyarwanda", "ro": "Romanian", "rm": "Romansh", "rom": "Romany", "jbo": "Lojban", "mg": "Malagasy", "gv": "Manx", "mt": "Maltese", "mr": "Marathi", "ml": "Malayalam", "ms": "Malay", "chm": "Mari (Russia)", "mk": "Macedonian", "mh": "Marshallese", "kek": "Kekchí", "mai": "Maithili", "mfe": "Morisyen", "mi": "Maori", "mn": "Mongolian", "bn": "Bengali", "my": "Burmese", "hmn": "Hmong", "umb": "Umbundu", "nv": "Navajo", "af": "Afrikaans", "ne": "Nepali", "niu": "Niuean", "no": "Norwegian", "pmn": "Pam", "pap": "Papiamento", "pa": "Panjabi", "pt": "Portuguese", "ps": "Pushto", "ny": "Nyanja", "tw": "Twi", "chr": "Cherokee", "ja": "Japanese", "sv": "Swedish", "sm": "Samoan", "sg": "Sango", "si": "Sinhala", "hsb": "Upper Sorbian", "eo": "Esperanto", "sl": "Slovenian", "sw": "Swahili", "so": "Somali", "sk": "Slovak", "tl": "Tagalog", "tg": "Tajik", "ty": "Tahitian", "te": "Telugu", "ta": "Tamil", "th": "Thai", "to": "Tonga (Tonga Islands)", "toi": "Tonga (Zambia)", "ti": "Tigrinya", "tvl": "Tuvalu", "tyv": "Tuvinian", "tr": "Turkish", "tk": "Turkmen", "wa": "Walloon", "war": "Waray (Philippines)", "cy": "Welsh", "ve": "Venda", "vo": "Volapük", "wo": "Wolof", "udm": "Udmurt", "ur": "Urdu", "uz": "Uzbek", "es": "Spanish", "ie": "Interlingue", "fy": "Western Frisian", "szl": "Silesian", "he": "Hebrew", "hil": "Hiligaynon", "haw": "Hawaiian", "el": "Modern Greek", "lfn": "Lingua Franca Nova", "sd": "Sindhi", "hu": "Hungarian", "sn": "Shona", "ceb": "Cebuano", "syr": "Syriac", "su": "Sundanese", "hy": "Armenian", "ace": "Achinese", "iba": "Iban", "ig": "Igbo", "io": "Ido", "ilo": "Iloko", "iu": "Inuktitut", "it": "Italian", "yi": "Yiddish", "ia": "Interlingua", "hi": "Hindi", "id": "Indonesia", "inh": "Ingush", "en": "English", "yo": "Yoruba", "vi": "Vietnamese", "zza": "Zaza", "jv": "Javanese", "zh": "Chinese", "zh-tw": "Traditional Chinese", "yue": "Cantonese", "zu": "Zulu"}


def get_lang_names():
    out = []
    for i in lang_dict:
        out.append(lang_dict[i])

    return out


def get_lang_codes():
    out = []
    for i in lang_dict:
        out.append(i)

    return out


def get_lang_by_code(code):
    for i in lang_dict:
        if code == i:
            return lang_dict[i]


def get_lang_by_name(name):
    for i in lang_dict:
        if name == lang_dict[i]:
            return i
