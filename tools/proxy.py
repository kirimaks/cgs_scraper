from random import randrange
import requests
from requests.exceptions import ConnectionError
import re


class ProxyObj:
    def __init__(self, proxy_str):
        self._type = proxy_str.split("://")[0]
        self._addr = proxy_str.split("://")[1].split(":")[0]
        self._port = proxy_str.split(":")[-1]
        self._curl = proxy_str
        self._ip_port = "{}:{}".format(self._addr, self._port)

    @property
    def type(self):
        return self._type

    @property
    def addr(self):
        return self._addr

    @property
    def port(self):
        return self._port

    def __repr__(self):
        """ curl format """
        return self._curl

    @property
    def ipPort(self):
        return self._ip_port


class ProxyFactory:
    def gen_proxy(self):
        while True:
            try:
                n = randrange(10)

                if n == 0:
                    proxy_obj = self.gimmeproxy()
                else:
                    proxy_obj = self.heroku()

                return proxy_obj

            except (TypeError, ConnectionError, AssertionError):
                continue

    def gimmeproxy(self):
        url = "http://gimmeproxy.com/api/getProxy"
        resp = requests.get(url).json['curl']
        self.check_proxy(resp)
        return ProxyObj(resp)

    def heroku(self):
        url = "https://mighty-ridge-44958.herokuapp.com/get_proxy"
        resp = requests.get(url).text
        self.check_proxy(resp)
        return ProxyObj(resp)

    def check_proxy(self, proxy):
        if not re.match(r'https?\:\/\/\d+\.\d+\.\d+\.\d+\:\d+', proxy):
            raise AssertionError


if __name__ == "__main__":
    import time

    px = ProxyFactory()
    for _ in range(100):
        obj = px.gen_proxy()
        print("__str__: ", obj)
        print("addr: ", obj.addr)
        print("port: ", obj.port)
        print("type: ", obj.type)
        print("ipPort: ", obj.ipPort)
        print()
        time.sleep(1)
