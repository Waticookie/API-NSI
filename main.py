import requests
import json
import matplotlib.pyplot as plt
import numpy as np

datedebut = (input("Entrez la date de début de recherche d'astéroide sous le format : YYYY-MM-DD : "))
datefin = (input("Entrez la date de début de recherche d'astéroide sous le format : YYYY-MM-DD : "))
key = (input("Entrez votre clé d'API provenant de https://api.nasa.gov/ : "))

def asteroide_en_date(datedebut, datefin, key): #cette fct retourne le nom, la dangereusité et la distance à la Terre des astéroides entre 2 dates demandées
    res = []
    r = requests.get(f'https://api.nasa.gov/neo/rest/v1/feed?start_date={datedebut}&end_date={datefin}&api_key={key}')
    rdico = r.json()
    astero = rdico['near_earth_objects']
    for date, asteroides in astero.items():
        print(f"\n Date : {date}")
        for a in asteroides:
            nom = a['name']
            dangereux = a['is_potentially_hazardous_asteroid']
            distance = a['close_approach_data'][0]['miss_distance']['kilometers']
            
            print(f" L'astéroide se nomme {nom}")
            print(f"   Est-il dangereux ? : {dangereux}")
            print(f"   Distance la plus proche à laquelle l'astéroide a été par rapport à la Terre : {distance} km")

def distances_asteroides(datedebut, datefin, key): #cette fonction permet de retourner seulement la distance des astéroides afin de les trier dans le graphique
    r = requests.get(f'https://api.nasa.gov/neo/rest/v1/feed?start_date={datedebut}&end_date={datefin}&api_key={key}')
    rdico = r.json()
    neos = rdico['near_earth_objects']

    distances = []

    for date, asteroides in neos.items():
        for a in asteroides:
            distance_km = float(a['close_approach_data'][0]['miss_distance']['kilometers'])
            distances.append(distance_km)

    return distances

distances = distances_asteroides(datedebut, datefin, key)

#créer un graphique avec la distance à la Terre et une ligne de danger 
plt.figure(figsize=(10, 5)) 
plt.scatter(range(len(distances)), distances)
plt.axhline(y=7_500_000,color='red',linestyle='--',label='7,5 millions de km')
plt.title("Distances de passage des astéroïdes")
plt.xlabel("Nombre d'Astéroïdes")
plt.ylabel("Distance (km)")
plt.grid(True)
plt.show()
print(asteroide_en_date(datedebut, datefin, key))
