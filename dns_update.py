import sys
import ovh

# Vérifie que l'adresse IP a été fournie en argument
if len(sys.argv) != 2:
    print("Usage: python dns_update.py <public_ip>")
    sys.exit(1)

public_ip = sys.argv[1]

client = ovh.Client(
    endpoint='ovh-eu',
    application_key=os.getenv("OVH_APP_KEY"),
    application_secret=os.getenv("OVH_APP_SECRET"),
    consumer_key=os.getenv("OVH_CONSUMER_KEY")
)


# Liste des domaines à mettre à jour
domains = [
    {"zone": "my-soc.fr", "subdomain": "prometheus"},
    {"zone": "my-soc.fr", "subdomain": "iris"},
    {"zone": "my-soc.fr", "subdomain": "kibana"},
    {"zone": "my-soc.fr", "subdomain": "doctobobo"}
]

# Met à jour chaque enregistrement DNS
for domain in domains:
    zone = domain["zone"]
    subdomain = domain["subdomain"]

    try:
        # Récupère l'enregistrement DNS existant
        records = client.get(f"/domain/zone/{zone}/record", subDomain=subdomain, fieldType="A")
        if not records:
            print(f"Aucun enregistrement trouvé pour {subdomain}.{zone}")
            continue

        record_id = records[0]  # Prend le premier ID (on suppose un seul enregistrement par sous-domaine)
        print(f"Found record ID {record_id} for {subdomain}.{zone}")

        # Met à jour l'enregistrement avec la nouvelle adresse IP
        client.put(f"/domain/zone/{zone}/record/{record_id}", target=public_ip)
        print(f"Updated {subdomain}.{zone} to {public_ip}")

    except ovh.exceptions.APIError as e:
        print(f"Erreur lors de la mise à jour de {subdomain}.{zone}: {e}")

# Applique les changements
try:
    client.post("/domain/zone/my-soc.fr/refresh")
    print("Zone DNS actualisée avec succès.")
except ovh.exceptions.APIError as e:
    print(f"Erreur lors de l'actualisation de la zone DNS: {e}")
