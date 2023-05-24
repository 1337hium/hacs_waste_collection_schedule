import logging
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from waste_collection_schedule import Collection

TITLE = "Alchenstorf"
DESCRIPTION = " Source for 'Alchenstorf, CH'"
URL = "https://www.alchenstorf.ch"
TEST_CASES = {"TEST": {}}

ICON_MAP = {
    "Grünabfuhr Alchenstorf": "mdi:leaf",
    "Kehrichtabfuhr Alchenstorf": "mdi:trash-can-outline",
    "Kartonsammlung Alchenstorf": "mdi:recycle",
    "Papiersammlung Alchenstorf": "mdi:newspaper-variant-multiple-outline",
    #   "Häckselservice": "mdi:leaf-off",
    "Alteisenabfuhr Alchenstorf": "mdi:desktop-classic",
    # "Zusätzliche Gratis-Laubabfuhr": "mdi:leaf",
}

_LOGGER = logging.getLogger(__name__)


class Source:
    def __init__(self):
        self = None

    def fetch(self):
        r = requests.get("https://www.alchenstorf.ch/abfalldaten")

        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")

        entries = []

        for tag in soup.find_all(class_="InstList-institution InstDetail-termin"):
            for typ in tag.find_all("strong"):
                # print(typ.string)
                waste_type = typ.string
            for date in tag.find_all("span", class_="mobile"):
                # print(date.string[-8:])
                waste_date = datetime.strptime(date.string[-8:], "%d.%m.%y").date()

            entries.append(Collection(waste_date, waste_type, ICON_MAP.get(waste_type)))

        return entries
