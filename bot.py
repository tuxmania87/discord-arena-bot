import configparser
import requests
import datetime
import json 
from datetime import timezone
import time


def check_arena(user):

    url = f"https://lichess.org/api/user/{user}/tournament/created?status=10&status=20"
    #url = f"https://lichess.org/api/user/{user}/tournament/created"

    r = requests.get(url)

    content = r.content.decode("utf-8")

    dt = datetime.datetime.now(timezone.utc)
  
    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()

    now = int(utc_timestamp)

    for line in content.split("\n"):
        if line.strip() == "":
            continue

        t = json.loads(line)

        starts_in = int(t["startsAt"]/ 1000) - now
        finishes_in = int(t["finishesAt"]/ 1000) - now
        turl = "https://lichess.org/tournament/" + t["id"]
        rated = "gewertet" if t["rated"] else "nicht gewertet"

        
        if starts_in > 0 and t["id"] not in created:
            created.append(t["id"])

            clock_limit = int(t["clock"]["limit"] / 60)
            clock_increment = t["clock"]["increment"]

            
            
            starts_string = f"{starts_in} Sekunden {turl}"

            if starts_in > 59:
                starts_string = str(starts_in // 60) + " Minuten und " + str(starts_in - (starts_in // 60) * 60) + f" Sekunden: {turl}"
                

                #print(starts_in, starts_in // 60, (starts_in // 60) * 60, starts_in - (starts_in // 60) * 60)

            anounce_string = f"Neues Turnier ({rated}) von {user}, Format: {clock_limit}+{clock_increment} Startet in {starts_string}"

            data = {"content":anounce_string}
            requests.post(announce_url, json=data)
            print(anounce_string)

        if starts_in < 0 and finishes_in > 0 and t["id"] not in started:
            started.append(t["id"])

            clock_limit = int(t["clock"]["limit"] / 60)
            clock_increment = t["clock"]["increment"]

           
            anounce_string = f"Turnier ({rated}) von {user}, Format: {clock_limit}+{clock_increment} hat jetzt angefangen: {turl}"
            data = {"content":anounce_string}
            requests.post(announce_url, json=data)
            print(anounce_string)


c = configparser.ConfigParser()
c.read("general.conf")

announce_url = c["DEFAULT"]["webhook"]
players =  c["DEFAULT"]["players"].split(",")


created = []
started = []

while True:
    for p in players:
        print("Checking for ",p)
        check_arena(p)
        time.sleep(1)
    print("waiting for 60...")
    time.sleep(60)