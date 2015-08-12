import requests
import json
from pathlib import Path

apikey = "f5b9ed4f-2e16-454a-bed3-3f38eba799ce"
uri = "https://global.api.pvp.net/api/lol/%s/v2.2/match/%i?api_key=" + apikey
region = "br"
id = 542478739

r = requests.get(uri % (region, id))
print(r.status_code)
p = Path(".") / "test.json"
with p.open("w") as f:
    json.dump(r.json(), f)