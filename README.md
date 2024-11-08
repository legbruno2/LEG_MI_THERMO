## Gestion centralisée du thermomètre Xiaomi LYWSD03MMC
--------------------------------------------------
Petite gestion centralisée de la température des différentes pièces de la maison.

Utilisation du thermomètre Xiaomi LYWSD03MMC Bluetooth ( avec firmware modifié )

![image](https://github.com/legbruno2/LEG_MI_THERMO/assets/152851976/af1b1380-22df-42b6-a78d-fa6d2170fdc9)

Projet majoritairement inspiré de : https://github.com/atc1441/ATC_MiThermometer/blob/master/README.md

Les thermomètres Xiaomi ont été achetés en janvier 2024 sur aliexpress.com ( modèle LYWSD03MMC Bluetooth ) 

![image](https://github.com/legbruno2/LEG_MI_THERMO/assets/152851976/471e73b4-5d71-4dab-a208-8f77034073b1)
----------------------------------------------------
Procédure pour le remplacement du firmware :
=

A) Télécharger le firmware "ATC_Thermomètre.bin"  
   Dernière update disponible à l'adresse : https://github.com/atc1441/ATC_MiThermometer/tree/master

B) Utiliser le programmateur en ligne : https://atc1441.github.io/TelinkFlasher.html

B1) Lancer le TelinkFlasher sur un smartphone ou sur un ordinateur portable ayant le bluetooth activé :

![image](https://github.com/legbruno2/LEG_MI_THERMO/assets/152851976/e6bee399-cdb1-4539-b531-f7611412ab2e)

B2) Appuyer sur [Connect]  et sélectionner l'appareil nommé : LYWSD03MMC

B3) Une fois 'connecté' : appuyer sur [Do Activation]
    
si tout se passe bien , les champs 'Devide known ID' , 'Mi Token' et 'Mi Bind Key' doivent se remplir

![image](https://github.com/legbruno2/LEG_MI_THERMO/assets/152851976/4e36ef82-ff20-4832-b72a-5eabbddeb217)

B4) Appuyer sur [Choisir un fichier]   et sélectionner le fichier 'ATC_Thermomètre.bin' téléchargé plus haut.

B5) Appuyer sur [Start Flashing] pour télécharger le nouveau firmware

==> A la fin du téléchargement, le thermometre doit redémarrer.

Une fois redémarré, appuyer à nouveau sur [connect]

dans la liste proposée, le thermomètre doit apparaitre sous le nom ATC_xxyyzz  ou xxyyzz correspond aux 3 derniers octets de l'adresse MAC(voir plus bas)

Une fois connecté, le status doit indiqué : " Detected custom Firmware "

A partir de là, il est possible de modifier différents parametres du thermometre ( en cliquant directement sur l'un des boutons correspondants).

Adresse MAC du thermomètre : 
=
Au démarrage, le micrologiciel personnalisé affichera les trois derniers octets de l'adresse MAC dans la partie d'affichage de l'humidité sur l'écran LCD pendant 2 secondes chacun, les trois premiers octets sont toujours les mêmes (A4:C1:38) et ne sont donc pas affichés. 

Sinon : l'adresse MAC se retrouve aussi dans le nom BLE du thermometre , format : ACT_AABBCC ou AABBCC correspond aux trois derniers octets de l'adresse MAC.

RECUPERATION des INFOS (Température/Humidité) via un appareil bluetooth 
=
De mon coté, j'ai utilisé une raspberry PI 3B avec un petit scénario en Python

Principe: le thermomètre envoie toutes les minutes une notification bluetooth dans laquelle a été inscrit les valeurs de température, d'humidité et % de la batterie.

le scénario python récupère toutes les notifications bluetooth et en extrait les infos quand la notification concerne un des thermomètres XIAOMI.

le scénario utilise la librairie pybluez

merci à https://hackaday.com/2020/12/08/exploring-custom-firmware-on-xiaomi-thermometers/

INSTALLATION :
=
==> installer bluetooth and pybluez

sudo apt-get update

sudo apt-get install bluetooth libbluetooth-dev

sudo pip install pybluez


==> autoriser 'admin' pour le python3  (pour qu'il aie acces à l'interface bluetooth)

sudo setcap cap_net_raw,cap_net_admin+eip $(eval readlink -f `which python3`)

==> récuperer les deux fichiers bluetooth_utils.py et scanThermoXiaomi.py

==> lancer le scénario python : scanThermoXiaomi.py
 
