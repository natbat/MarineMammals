from bs4 import BeautifulSoup
import requests
import datetime
import json


def get_tables(url):
    html = requests.get(url).content
    soup = BeautifulSoup(html, "html5lib")
    tables = soup.findAll("table")
    return tables


def check_headings(headings, animal_table):
    assert headings == [th.text.lower().strip() for th in animal_table.findAll("th")]


def scape_current():
    tables = get_tables(
        "http://www.marinemammalcenter.org/patients/current-patients-page/"
    )
    animal_table = tables[0]
    check_headings(
        [
            "admit date",
            "name",
            "common name",
            "stranding location",
            "class",
            "sex",
            "admit weight (kg)",
            "diagnosis",
        ],
        animal_table,
    )

    animals = []

    return


def scrape_past():
    tables = get_tables(
        "http://www.marinemammalcenter.org/patients/current-patients-page/"
    )
    animal_table = tables[0]
    check_headings(
        [
            "admit date",
            "name",
            "common name",
            "stranding location",
            "class",
            "sex",
            "admit weight (kg)",
            "diagnosis",
        ],
        animal_table,
    )

    return


def parse_date(date):
    # US Date format to ISO
    datetime.datetime.strptime(date, "%m/%d/%y").date().isoformat()
    return date


def dictionary_current(date):
    for tr in animal_table.find("tbody").findAll("tr"):
        tds = tr.findAll("td")

        admit_date_ISO = parse_date(tds[0].getText())
        name = tds[1].getText()  # given name
        species_common_name = tds[2].getText()  # seperate table?
        stranding_location = tds[3].getText()  # seperate table or location lookup?
        age_class = tds[4].getText()  # seperate table?
        sex = tds[5].getText()
        admit_weight = tds[6].getText()  # kg
        diagnosis = tds[7].getText()  # Could seperate this by comma?
        status = "current patient"
        status_date = admit_date_ISO
        status_location = ""

        # maybe a seperate status table? for released/restrand/deceased/current etc so that it references the animal?
        restrand = False
        if "(restrand)" in name:
            restrand = True
            name = name.replace("(restrand)", "").strip()

        animals.append(
            {
                "name": name,
                "restrand": restrand,
                "species": species_common_name,
                "stranding_location": stranding_location,
                "admitted": admit_date_ISO,
                "admit_weight": float(admit_weight),
                "age_class": age_class,
                "sex": sex,
                "diagnosis": [s.strip() for s in diagnosis.split(",") if s.strip()],
                "status": status,
                "status_date": status_date,
                "status_location": status_location,
            }
        )

    print(json.dumps(animals, indent=4))


def dictionary_this_year_past():
    return


def build_animals():
    """
        load previous animals json as list
        change to dictionary animals_dictionary

        scrape list of current animals in center as list current_animals

        scrape past animals from this year into in memory list past_animals
        scrape and follow each past year link
            put animals into in memory list past_animals

        for item in and current animals list
            add any new animals
            update animals with changes
            (every animal should have the same fields but some being blank)

        for item in past_animals list
            add any new animals that were housecalls etc or found dead
            update animals with changes
            (every animal should have the same fields but some being blank)

        override animals_dictionary with information from current_animals and past_animals
        if a column exists on a pabge we overwrite it otherwise we leave it alone, eg admit date

        take dictionary
        turn into list
        sort list on id
        overwrite animals.json
    """
    return


if __name__ == "__main__":
    animals = build_animals()
