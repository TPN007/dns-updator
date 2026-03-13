# DNS-UPDATOR
# V1
# by TPN

# IMPORTS

import os
import ovh
from dotenv import load_dotenv

# VARS

check = 0


# FONCTIONS

def add_record(dns_zone, record_type, subdomain, target):
    print("Ajout d'un record DNS")

    try:
        new_record = client.post(f'/domain/zone/{dns_zone}/record',
            fieldType=record_type,
            subDomain=subdomain,
            target=target,
            ttl=60
        )
        print(f"Record créé avec l'ID : {new_record['id']}")

        client.post(f'/domain/zone/{dns_zone}/refresh')
        print(f"Zone {dns_zone} rafraîchie avec succès ! Les DNS se propagent.")

    except ovh.exceptions.APIError as e:
        print(f"Erreur lors de l'ajout du record : {e}")

def delete_record(dns_zone, record_type, subdomain):
    print("Suppression d'un record DNS")

    try:
        ids = client.get(f'/domain/zone/{dns_zone}/record', 
                        subDomain=subdomain, 
                        fieldType=record_type)

        if not ids:
            print(f"Aucun record {record_type} trouvé pour {subdomain}.{dns_zone}")
            return

        for record_id in ids:
            client.delete(f'/domain/zone/{dns_zone}/record/{record_id}')
            print(f"Record ID {record_id} supprimé.")

        client.post(f'/domain/zone/{dns_zone}/refresh')
        print(f"Zone {dns_zone} rafraîchie.")

    except ovh.exceptions.APIError as e:
        print(f"Erreur OVH : {e}")

def edit_record(dns_zone, subdomain, record_type, target):
    print("Modification d'un record DNS")

    try:
        ids = client.get(f'/domain/zone/{dns_zone}/record', 
                        subDomain=subdomain, 
                        fieldType=record_type)

        if not ids:
            print(f"Aucun record {record_type} trouvé pour {sub_domain}.{dns_zone}")
            return

        for record_id in ids:
            client.put(f'/domain/zone/{dns_zone}/record/{record_id}',
                target=target,
                subDomain=subdomain
            )
            print(f"Record {record_id} mis à jour vers : {target}")

        client.post(f'/domain/zone/{dns_zone}/refresh')
        print(f"Zone {dns_zone} rafraîchie.")

    except ovh.exceptions.APIError as e:
        print(f"Erreur lors de la modification : {e}")


load_dotenv()

required_keys = ['OVH_ENDPOINT', 'OVH_APPLICATION_KEY', 'OVH_APPLICATION_SECRET', 'OVH_CONSUMER_KEY']
missing_keys = [key for key in required_keys if not os.getenv(key)]

if missing_keys:
    exit(f"Erreur : Les variables suivantes sont manquantes dans le .env : {', '.join(missing_keys)}")

client = ovh.Client(
    endpoint=os.getenv('OVH_ENDPOINT'),
    application_key=os.getenv('OVH_APPLICATION_KEY'),
    application_secret=os.getenv('OVH_APPLICATION_SECRET'),
    consumer_key=os.getenv('OVH_CONSUMER_KEY'),
)

try:
    # Test de connexion
    me = client.get('/me')
    print(f"OVH API : Connexion réussie ! Bienvenue {me['firstname']}")
except ovh.exceptions.APIError as e:
    print(f"OVH API : Erreur lors de la connexion : {e}")

while check == 0:
    print("")
    print("[1] Ajouter un record")
    print("[2] Supprimer un record")
    print("[3] Modifier un record")
    print("[4] Quitter")
    print("")

    choix=int(input("Sélectionnez votre choix : "))


    if choix == 1:
        dns_zone=input("Nom de la zone DNS : ")
        record_type=input("Type d'enregistrement ? [A/AAAA/CNAME/TXT/NS] : ")
        subdomain=input("Sous domaine : ")
        target=input("Cible (pensez au . à la fin pour un CNAME): ")
        add_record(dns_zone, record_type, subdomain, target)
        check=1
    elif choix == 2:
        dns_zone=input("Nom de la zone DNS : ")
        record_type=input("Type d'enregistrement ? [A/AAAA/CNAME/TXT/NS] : ")
        subdomain=input("Sous domaine : ")
        delete_record(dns_zone, record_type, subdomain)
        check=1
    elif choix == 3:
        dns_zone=input("Nom de la zone DNS : ")
        record_type=input("Type d'enregistrement ? [A/AAAA/CNAME/TXT/NS] : ")
        subdomain=input("Sous domaine : ")
        target=input("Nouvelle cible (pensez au . à la fin pour un CNAME): ")
        edit_record(dns_zone, subdomain, record_type, target)
        check=1
    elif choix == 4:
        print("Clôture du script...")
        exit(0)
    else:
        print("Veuillez sélectionner le bon choix")