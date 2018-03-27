# genexis-router
Python3 API for Genexis DRGOS HRG1000

Requires Python>=3.6

#### How to use:
```
import genexis

router = genexis.Router(username="admin", password="admin")

print(router.system())

>>> {'platform': 'HRG1000', 'prodname': 'Platinum-4810', 'prodnum': '99613039', 'proddate': '2014-05-06', 'version': '2', 'serialnum': 'B.0000081358', 'ethaddr': '00:0F:94:41:F1:E0', 'bootloader': 'drgldr-hrg1000-1.4.1-RC16', 'firmware': 'drgos-hrg1000-1.14.3-R'}
```


Other info: `static_hosts()`, `dhcp_leases()`, `port_forwarding()`