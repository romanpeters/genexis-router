"""
Python3 API for the Genexis DRGOS HRG1000 router.
"""
import requests
from bs4 import BeautifulSoup
import base64


class Router:
    """Representation of the router"""
    def __init__(self, username, password, ip_address=None):
        token = base64.b64encode(str.encode(f"{username}:{password}")).decode()
        self.base_url = ip_address if ip_address else "http://router"
        self.headers = {"Authorization": f"Basic {token}"}

    def _api_get(self, url: str) -> BeautifulSoup:
        """Send a request to WBW"""
        req = requests.request('get', url, headers=self.headers)
        if req.status_code == 200:
            return BeautifulSoup(req.text, "lxml")
        else:
            raise ConnectionError

    def _get_lines(self, path: str) -> dict():
        url = self.base_url + path
        soup = self._api_get(url)
        content = soup.find("div", {"id": "content"})
        result = dict()

        for item in content.find_all("tr"):
            key = item.get("id")
            value = self._strip(item.find_all("td")[1].get_text())

            result[key] = value
        return result

    def _get_tables(self, path:str, only_with_action=True) -> list:
        url = self.base_url + path
        soup = self._api_get(url)
        content = soup.find("div", {"id": "content"})
        keys = [self._strip(i.get_text()) for i in content.find_all("th")]
        result = list()
        for c in content.find_all("tr")[1:]:
            values = [self._strip(i.get_text()) for i in c.find_all("td")]
            item = dict(zip(keys, values))
            if item.get('Action'):
                item.pop('Action')
                result.append(item)
        return result

    def _strip(self, text: str) -> str:
        text = text.strip()
        junk = ["++TR@", "@TR++", "\xa0", "\n"]
        for i in junk:
            text = text.replace(i, "")
        return text

    def interfaces(self) -> dict:
        """Return status information"""
        return self._get_lines('/cgi-bin/status-interfaces.sh')

    def system(self) -> dict:
        """Return system information"""
        return self._get_lines('/cgi-bin/info-system.sh')

    def static_hosts(self) -> list:
        """Return system information"""
        return self._get_tables('/cgi-bin/network-dhcpiface.sh')

    def dhcp_leases(self) -> list:
        return self._get_tables('/cgi-bin/status-leases.sh')

    def port_forwarding(self) -> list:
        return self._get_tables('/cgi-bin/nat-pfwd.sh')
