import requests
import json
from bs4 import BeautifulSoup
import os


class Config:
    data = json.load(open("settings.json"))
    url_ar = data["BCRA"]
    url_uy = data["BROU"]


def get_usd_uy():
    r = requests.get(Config.url_uy)
    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.select_one("table")
    table_data = [[cell.text for cell in row("td")]
                          for row in table("tr")]
    d = {}
    for i in table_data:
        try:
            d[i[0].strip()] = [float(i[2].replace(",", ".").strip()), float(i[4].replace(",",".").strip())]
        except ValueError:
            pass
    return d["Dólar"][1]  # DOLAR UY VENTA


def get_usd_ar():
    token = os.environ.get("BCRA_TOKEN")
    print(f"token {token}")
    headers = {
      'Content-Type': 'application/json',
      'Authorization': f"BEARER {token}"
    }
    r = requests.get(Config.url_ar, headers=headers)
    d = r.json()
    d.reverse()
    return d[0]["v"]


class Calc(object):
    def __init__(self):
        self.usd_ar = 63.03
        self.usd_uy = 38.31
        self.data_uy = None

    def uy2ar(self, uy, tax=0.3 ):
        usds = uy / self.usd_uy
        ar = usds * self.usd_ar + (usds * self.usd_ar * tax)
        return ar


"""
1 uds ----- 38.31
x uds ----- 250

1 uds ---   63.03
6 uds ----  x ar


uds = ury / uds_uy
uds * usd_ar
"""