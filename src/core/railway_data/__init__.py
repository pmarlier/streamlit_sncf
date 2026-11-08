FOREIGN_CITY = [
    "zurich",
    "barcelona",
    "madrid",
    "francfort",
    "italie",
    "lausanne",
    "geneve",
    "stuttgart",
]

MAP_CITY = {
    "lille": "lille-champ-de-mars",
    "paris-lyon": "paris-gare-de-lyon",
    "saint-etienne-chateaucreux": "st-etienne-chateaucreux",
    "angers-saint-laud": "angers-st-laud",
    "macon-loche": "macon-ville",
    "metz": "metz-ville",
    "nancy": "nancy-ville",
    "strasbourg": "strasbourg-ville",
    "valence-alixan-tgv": "valence-tgv",
    "montpellier": "montpellier-sud-de-france",
    "marne-la-vallee": "paris-gare-de-lyon",
    "paris-montparnasse": "paris-montparnasse-pasteur",
    "bellegarde-(ain)": "bellegarde",
    "lyon-part-dieu": "lyon-perrache",
    # as long as we don't have any railway geo coordinates for foreign countries
    # we mapped foreign railstation with the closest city in France
    # that is only for railpath drawing
    "madrid": "perpignan",
    "barcelona": "perpignan",
    "italie": "monaco",
    "francfort": "strasbourg",
    "stuttgart": "strasbourg",
    "zurich": "annecy",
    "lausanne": "annecy",
    "geneve": "annecy",
}

# 590000 - limoges - vierzon
# 690000 - vierzon - bourges
# 750000 - fontainebleau - lyon
# 570000 - paris - orleans
# 930000 - monaco - marseille
# 7000 - paris strasbourg

RAILWAY_ID_NETWORK = {  # OK
    "aix-en-provence-tgv-paris-gare-de-lyon": [752000],
    "paris-gare-de-lyon-aix-en-provence-tgv": [752000],
    # angers - paris ==> angers - le mans - paris
    "angers-st-laud-paris-montparnasse-pasteur": [420000, 450000],
    "paris-montparnasse-pasteur-angers-st-laud": [420000, 450000],
    # OK
    "angouleme-paris-montparnasse-pasteur": [570000],
    "paris-montparnasse-pasteur-angouleme": [570000],
    # 'annecy-paris-gare-de-lyon': [897000, 900000, 890000, 686000,
    # 570000, 569000, 590000, 690000, 750000, 830000, 981000],
    "annecy-paris-gare-de-lyon": [750000, 897000, 900000],
    "paris-gare-de-lyon-annecy": [750000, 897000, 900000],
    # OK
    "arras-paris-nord": [301000, 272000],
    "paris-nord-arras": [272000, 301000],
    # OK
    # 'avignon-tgv-paris-gare-de-lyon': [830000],
    # 'paris-gare-de-lyon-avignon-tgv': [830000],
    "avignon-tgv-paris-gare-de-lyon": [752000],
    "paris-gare-de-lyon-avignon-tgv": [752000],
    "barcelona-paris-gare-de-lyon": [677000, 570000, 640000, 590000],
    "paris-gare-de-lyon-barcelona": [677000, 570000, 640000, 590000],
    # OK
    "bellegarde-paris-gare-de-lyon": [830000, 890000],
    "paris-gare-de-lyon-bellegarde": [830000, 890000],
    "besancon-franche-comte-tgv-paris-gare-de-lyon": [14000, 850000, 830000],
    "paris-gare-de-lyon-besancon-franche-comte-tgv": [14000, 850000, 830000],
    # OK
    "paris-montparnasse-pasteur-bordeaux-st-jean": [570000],
    "bordeaux-st-jean-paris-montparnasse-pasteur": [570000],
    # OK
    "paris-vaugirard-bordeaux-st-jean": [570000],
    "bordeaux-st-jean-paris-vaugirard": [570000],
    # OK
    "bordeaux-st-jean-tourcoing": [278000, 570000, 272000],
    "tourcoing-bordeaux-st-jean": [278000, 570000, 272000],
    # OK
    "paris-montparnasse-pasteur-brest": [420000],
    "brest-paris-montparnasse-pasteur": [420000],
    "chambery-challes-les-eaux-paris-gare-de-lyon": [900000, 890000, 750000],
    "paris-gare-de-lyon-chambery-challes-les-eaux": [900000, 890000, 750000],
    # OK
    "dijon-ville-paris-gare-de-lyon": [830000],
    "paris-gare-de-lyon-dijon-ville": [830000],
    "douai-paris-nord": [272000],
    "paris-nord-douai": [272000],
    # 16
    "dunkerque-paris-nord": [272000, 301000, 302526],
    "paris-nord-dunkerque": [272000, 301000, 302526],
    # 17
    "francfort-paris-est": [70000],
    "paris-est-francfort": [70000],
    # 18
    # geneve - paris ==> geneve - lyon - paris
    "geneve-paris-gare-de-lyon": [890000],
    "paris-gare-de-lyon-geneve": [890000],
    # 19
    "grenoble-paris-gare-de-lyon": [905000, 750000],
    "paris-gare-de-lyon-grenoble": [905000, 750000],
    # 21
    "la-rochelle-ville-paris-montparnasse-pasteur": [420000, 450000, 515000, 530000],
    "paris-montparnasse-pasteur-la-rochelle-ville": [420000, 450000, 515000, 530000],
    # 22 cf. annecy
    "lausanne-paris-gare-de-lyon": [],
    "paris-gare-de-lyon-lausanne": [],
    # 23
    # OK
    "laval-paris-montparnasse-pasteur": [420000],
    "paris-montparnasse-pasteur-laval": [420000],
    # 24
    # OK
    "le-creusot-montceau-montchanin-paris-gare-de-lyon": [767300, 752000],
    "paris-gare-de-lyon-le-creusot-montceau-montchanin": [767300, 752000],
    # 25
    # OK
    "le-mans-paris-montparnasse-pasteur": [420000],
    "paris-montparnasse-pasteur-le-mans": [420000],
    # 26
    # OK
    "lille-champ-de-mars-lyon-perrache": [830000, 272000],
    "lyon-perrache-lille-champ-de-mars": [830000, 272000],
    # 27
    # OK
    "lille-champ-de-mars-marseille-st-charles": [272000, 830000],
    "marseille-st-charles-lille-champ-de-mars": [272000, 830000],
    # 28
    # OK
    "lille-champ-de-mars-paris-nord": [272000],
    "paris-nord-lille-champ-de-mars": [272000],
    # 29 lyon - marne-la-vallee
    # 30
    # OK
    "lyon-perrache-marseille-st-charles": [830000],
    "marseille-st-charles-lyon-perrache": [830000],
    # 31
    "lyon-perrache-montpellier-sud-de-france": [810000, 830000],
    "montpellier-sud-de-france-lyon-perrache": [810000, 830000],
    # 32
    # OK
    "lyon-perrache-paris-gare-de-lyon": [830000],
    "paris-gare-de-lyon-lyon-perrache": [830000],
    # 33
    # OK
    "lyon-perrache-rennes": [830000, 420000],
    "rennes-lyon-perrache": [830000, 420000],
    # 34
    # OK
    "macon-ville-paris-gare-de-lyon": [830000],
    "paris-gare-de-lyon-macon-ville": [830000],
    # 36 marseille - marne la vallee (iso 37)
    # 37
    # OK
    "marseille-st-charles-paris-gare-de-lyon": [830000],
    "paris-gare-de-lyon-marseille-st-charles": [830000],
    # 38
    # OK
    "marseille-st-charles-tourcoing": [830000, 272000, 278000],
    "tourcoing-marseille-st-charles": [830000, 272000, 278000],
    # 39 - jusqu'à nancy seulement
    "paris-est-metz-ville": [70000],
    "metz-ville-paris-est": [70000],
    # 40
    "montpellier-sud-de-france-paris-gare-de-lyon": [810000, 830000],
    "paris-gare-de-lyon-montpellier-sud-de-france": [810000, 830000],
    # 41
    # OK
    "mulhouse-ville-paris-gare-de-lyon": [1000],
    "paris-gare-de-lyon-mulhouse-ville": [1000],
    # 42
    # OK
    "nancy-ville-paris-est": [70000],
    "paris-est-nancy-ville": [70000],
    # 43
    "paris-montparnasse-pasteur-nantes": [420000, 450000, 515000],
    "nantes-paris-montparnasse-pasteur": [420000, 450000, 515000],
    # 44
    "nantes-paris-vaugirard": [420000, 450000, 515000],
    "paris-vaugirard-nantes": [420000, 450000, 515000],
    # 45
    "nantes-strasbourg-ville": [7000, 420000, 450000, 515000],
    "strasbourg-ville-nantes": [7000, 420000, 450000, 515000],
    # 46
    # OK
    "nice-ville-paris-gare-de-lyon": [930000, 830000],
    "paris-gare-de-lyon-nice-ville": [930000, 830000],
    # 47
    "nimes-paris-gare-de-lyon": [810000, 830000],
    "paris-gare-de-lyon-nimes": [810000, 830000],
    # 48
    "reims-paris-est": [70000, 72000, 205000],
    "paris-est-reims": [70000, 72000, 205000],
    # 49
    # OK
    "paris-est-strasbourg-ville": [70000],
    "strasbourg-ville-paris-est": [70000],
    # 51
    # perpignan - montauban - orleans - paris
    "paris-gare-de-lyon-perpignan": [677000, 570000, 640000, 590000],
    "perpignan-paris-gare-de-lyon": [677000, 570000, 640000, 590000],
    # 52
    # OK
    "st-etienne-chateaucreux-paris-gare-de-lyon": [750000],
    "paris-gare-de-lyon-st-etienne-chateaucreux": [750000],
    # 53
    "paris-gare-de-lyon-toulon": [830000, 930000],
    "toulon-paris-gare-de-lyon": [830000, 930000],
    # 54
    # OK
    # 'valence-tgv-paris-gare-de-lyon': [752000, 908000, 905000, 830000], --> grenoble
    "paris-gare-de-lyon-valence-tgv": [830000],
    "valence-tgv-paris-gare-de-lyon": [830000],
    # 55 - zurich
    # 56
    # OK
    "paris-montparnasse-pasteur-poitiers": [570000],
    "poitiers-paris-montparnasse-pasteur": [570000],
    # 57
    "paris-montparnasse-pasteur-quimper": [420000, 468000, 470000],
    "quimper-paris-montparnasse-pasteur": [420000, 468000, 470000],
    # 58
    # OK
    "paris-montparnasse-pasteur-rennes": [420000],
    "rennes-paris-montparnasse-pasteur": [420000],
    # 59
    # OK
    "paris-montparnasse-pasteur-st-malo": [441000, 420000],
    "st-malo-paris-montparnasse-pasteur": [441000, 420000],
    # 60
    # OK
    "paris-montparnasse-pasteur-st-pierre-des-corps": [570000],
    "st-pierre-des-corps-paris-montparnasse-pasteur": [570000, 985000, 990000, 420000],
    # 61
    # OK
    "toulouse-matabiau-paris-montparnasse-pasteur": [640000, 570000],
    "paris-montparnasse-pasteur-toulouse-matabiau": [640000, 570000],
    # 62
    # OK
    # 'tours-paris-montparnasse-pasteur': [564300, 563300, 515000, 450000, 420000],
    "tours-paris-montparnasse-pasteur": [570000],
    "paris-montparnasse-pasteur-tours": [570000],
    # 63
    "vannes-paris-montparnasse-pasteur": [470000, 468000, 420000],
    "paris-montparnasse-pasteur-vannes": [420000, 468000, 470000],
    # 64
    # OK - mais bizarre ?
    "rennes-paris-vaugirard": [420000],
    "paris-vaugirard-rennes": [420000],
    "stuttgart-paris-est": [],
    "paris-est-stuttgart": [],
    "paris-gare-de-lyon-zurich": [],
    "zurich-paris-gare-de-lyon": [],
    "paris-gare-de-lyon-italie": [],
    "italie-paris-gare-de-lyon": [],
    "madrid-marseille-st-charles": [],
    "marseille-st-charles-madrid": [],
}


def get_processed_city_name(city_name: str) -> str:
    """Process the railstation name in SNCF punctuality rate csv file
    to match with railstation name in the other files

    Args:
        city_name (str): the city name from SNCF punctuality rate csv file

    Returns:
        str: the processed name to match with others SNCF files data
    """
    processed_city_name = city_name.lower().replace(" ", "-")

    try:
        processed_city_name = MAP_CITY[processed_city_name]
    except KeyError:
        # if the lowered-case city name is not in the map
        # meaning the name as outputed is correct
        pass

    return processed_city_name
