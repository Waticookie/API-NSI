import requests
import json
import matplotlib.pyplot as plt
import numpy as np

datedebut = (input("Entrez la date de début de recherche d'astéroide sous le format : YYYY-MM-DD : "))
datefin = (input("Entrez la date de fin de recherche d'astéroide sous le format : YYYY-MM-DD : "))
key = (input("Entrez votre clé d'API provenant de https://api.nasa.gov/ : "))

def asteroide_en_date_csv(datedebut, datefin, key):
    r = requests.get(f'https://api.nasa.gov/neo/rest/v1/feed?start_date={datedebut}&end_date={datefin}&api_key={key}')
    rdico = r.json()
    astero = rdico['near_earth_objects']

    with open("asteroides.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # en-têtes du CSV
        writer.writerow(["date", "nom", "dangereux", "distance_km"])

        for date, asteroides in astero.items():
            for a in asteroides:
                nom = a['name']
                dangereux = a['is_potentially_hazardous_asteroid']
                distance = a['close_approach_data'][0]['miss_distance']['kilometers']

                writer.writerow([date, nom, dangereux, distance])

    print("Fichier 'asteroides.csv' créé avec succès")


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

print(asteroide_en_date_csv(datedebut, datefin, key))

#créer un graphique avec la distance à la Terre et une ligne de danger 
plt.figure(figsize=(10, 5)) 
plt.scatter(range(len(distances)), distances)
plt.axhline(y=7_500_000,color='red',linestyle='--',label='7,5 millions de km')
plt.title("Distances de passage des astéroïdes")
plt.xlabel("Nombre d'Astéroïdes")
plt.ylabel("Distance (km)")
plt.grid(True)
plt.show()
