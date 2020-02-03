from flask import Flask, render_template
import os
import urllib.parse as urlparse
from calc import get_usd_uy, get_usd_ar
import redis


class Currencies(Flask):
    def __init__(self, __name__):
        super(Currencies, self).__init__(__name__)
        try:
            rconf = urlparse.urlparse(os.environ.get("REDISCLOUD_URL"))
            self.r = redis.Redis(host=rconf.hostname, port=rconf.port, password=rconf.password)
        except TypeError:
            self.r = None
        self.usd_uy = None
        self.usd_ar = None

    def get_data(self):
        try:
            self.usd_ar = float(self.r.get("USDAR").decode())
            self.usd_uy = float(self.r.get("USDUY").decode())
        except TypeError:
            self.usd_uy = self.usd_ar = None
        except AttributeError:
            self.usd_uy = self.usd_ar = None

        if not self.usd_ar or not self.usd_uy:
            self.usd_ar = get_usd_ar()
            self.usd_uy = get_usd_uy()
            try:
                self.r.set("USDAR", self.usd_ar, 60*60*2)
                self.r.set("USDUY", self.usd_uy, 60*60*2)
            except TypeError:
                pass

        return {"ar": self.usd_ar, "uy": self.usd_uy}


app = Currencies(__name__)


@app.route('/')
def index():
    data = app.get_data()
    return render_template("index.html", data=data)


def main():
    app.run(host="0.0.0.0", port=5001, debug=True)


if __name__ == '__main__':
    main()

