from bs4 import BeautifulSoup
import requests
import datetime
import json

html = requests.get("http://www.marinemammalcenter.org/patients/current-patients-page/").content
soup = BeautifulSoup(html, "html5lib")
tables = soup.findAll('table')
animalTable = tables[0]
animals = []
for tr in animalTable.find("tbody").findAll("tr"):
    tds = tr.findAll("td")

    admitDateUS = tds[0].getText() # US Date format
    admitDateISO = datetime.datetime.strptime(admitDateUS, "%m/%d/%y").date().isoformat()
    name = tds[1].getText() # given name
    speciesCommonName = tds[2].getText() # seperate table?
    strandingLocation = tds[3].getText() # seperate table or location lookup?
    ageClass = tds[4].getText() # seperate table?
    sex = tds[5].getText()
    admitWeight = tds[6].getText() # kg
    diagnosis = tds[7].getText() # Could seperate this by comma?
    status = "current patient"
    statusDate = admitDateISO
    statusLocation = ""


    # maybe a seperate status table? for released/restrand/deceased/current etc so that it references the animal?
    restrand = False
    if "(restrand)" in name:
        restrand = True
        name = name.replace("(restrand)", "").strip()

    animals.append({
        "name": name,
        "restrand": restrand,
        "species": speciesCommonName,
        "stranding_location": strandingLocation,
        "admitted": admitDateISO,
        "admit_weight": float(admitWeight),
        "age_class": ageClass,
        "sex": sex,
        "diagnosis": [s.strip() for s in diagnosis.split(",") if s.strip()],
        "status": status,
        "status_date" : statusDate,
        "status_location" : statusLocation
    })

print(json.dumps(animals, indent=4))
