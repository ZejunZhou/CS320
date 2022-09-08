# project: p5
# submitter: zzhou443
# partner: none
# hours: 7

from bisect import bisect
import re
import netaddr
import pandas as pd

ips = pd.read_csv("ip2location.csv")
list_low = list(ips["low"])
def lookup_region(ip):
    ip = re.sub(r"[a-z]", "0", ip)
    ip_address = int(netaddr.IPAddress(ip))
    idx = bisect(list_low, ip_address)
    region = ips.iloc[idx-1]["region"]
    return region 

    
class Filing:
    def __init__(self, html):
        self.dates = [i[0] for i in re.findall(r"((19|20)\d{2}-\d{2}-\d{2})", html)]
        sic = None
        if len(re.findall(r"SIC=(\d+)", html)) != 0:
            sic = int(re.findall(r"SIC=(\d+)", html)[0])
        self.sic = sic
        
        address = []
        for addr_html in re.findall(r'<div class="mailer">([\s\S]+?)</div>', html):
            lines = []
            for line in re.findall(r'<span class="mailerAddress">([\s\S]+?)</span>', addr_html):
                    lines.append(line.strip())
            if len(lines) != 0:
                address.append("\n".join(lines))
        
        self.addresses = address

    def state(self):
        for i in self.addresses:
            state_number = re.findall(r'([A-Z]{2})[\s][\d]{5}', i)
            if len(state_number) == 0:
                continue
            else:
                return state_number[0]
            return None