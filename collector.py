from pathlib import Path
from time import sleep
import requests
import json

apikey = "f5b9ed4f-2e16-454a-bed3-3f38eba799ce"

patches = ["5.11", "5.14"]
queue_types = ["RANKED_SOLO", "NORMAL_5X5"]
regions = ["NA", "EUW", "EUNE", "RU", "TR", "BR", "KR", "LAN", "LAS", "OCE"]
# region , matchId
uri = "https://global.api.pvp.net/api/lol/%s/v2.2/match/%i?api_key=" + apikey

settings = {}
settings_path = Path(".") / "settings.json"
try:
    settings_path.touch()
    settings = {
        "patch_id": 0,
        "queue_id": 0,
        "region_id": 0,
        "match_id": 0
    }
except FileExistsError:
    with settings_path.open() as f:
        settings = json.load(f)
    
p = Path(".") / "matchids"
for patch in patches:
    print("Patch:", patch)
    for queue in queue_types:
        print("Queue type:", queue)
        for region in regions:
            lregion = region.lower()
            print("Region:", region)
            matchesData = []
            q = p / patch / queue / (region + ".json")
            ids = []
            with q.open() as f:
                ids = json.load(f)
            
            i = 0
            saveTo = Path(".") / "jsondata" / patch / queue / (region + ".json")
            for id in ids:
                r = requests.get(uri % (lregion, id))
                while r.status_code != 200:
                    print("Status: ", r.status_code)
                    if r.status_code == 429:
                        print("Match", id, "failed to retrieve. Rate limit exceeded. Trying again in 10")
                        print(r.headers)
                        sleep(10)
                    else:
                        print("Match", id, "failed to retrieve. Trying again in 5")
                        sleep(5)
                    r = requests.get(uri % (lregion, id))
                matchesData.append(r.json())
                print("Match", id, "successfully retrieved!")
                i += 1
                
                if i > 10:
                    with saveTo.open("w") as f:
                        json.dump(matchesData, f)
                    print("Data from", region, "region successfully saved!")
                    i = 0
                sleep(1.5)
            
            
            with saveTo.open("w") as f:
                json.dump(matchesData, f)
            print("Data from", region, "region successfully saved!")