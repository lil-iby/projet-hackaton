# projet-hackaton

Micro-projet pour un ESP32 (MicroPython) qui interroge une API de trafic et pilote un servo + un buzzer selon l'état renvoyé.

## Description
Le script principal ([main.py](main.py)) :
- se connecte au Wi‑Fi via la fonction [`connect_wifi`](main.py),
- appelle l'API de traffic via [`call_api`](main.py),
- mappe la valeur `moyenne_etat` vers un angle grâce à [`value_to_degree`](main.py),
- commande un servo (objet `servo`) en utilisant [`angle_to_duty_ns`](main.py),
- émet un son via le buzzer (`buzzer`) avec la fonction [`beep`](main.py).

## Pré-requis
- ESP32 ou équivalent avec MicroPython installé.
- Modules MicroPython : `machine`, `network`, `urequests`, `time`.
- Connexion Internet pour l'ESP32.

## Configuration
Modifier les constantes Wi‑Fi dans [main.py](main.py) :
- `WIFI_SSID`
- `WIFI_PASS`

Ajuster la position et le rayon de la requête :
- `latitude`, `longitude`, `radius_m`

Ajuster la table de correspondance état→angle : [`value_to_degree`](main.py).

## Déploiement
1. Copier `main.py` sur l'ESP32 (via ampy, rshell, Thonny, ou autre).
2. Redémarrer la carte pour lancer le script automatiquement.

## Comportement attendu
- À chaque boucle, le script appelle l'API et lit `moyenne_etat`.
- Si la valeur change, le servo bouge et le buzzer émet un bip.
- Si la valeur est absente, un message d'erreur est affiché.

## Dépannage
- Vérifier la connexion Wi‑Fi : voir [`connect_wifi`](main.py).
- Vérifier la disponibilité de l'API et le format JSON retourné par [`call_api`](main.py).
- Ajuster les durées/angles si le servo ne répond pas correctement (`angle_to_duty_ns`).

## Licence
À définir.