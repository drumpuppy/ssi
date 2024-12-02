import ovh
import argparse
import os
import sys

def update_domains(ip):
    try:
        # Initialisation du client OVH avec des variables d'environnement
        client = ovh.Client(
            endpoint="ovh-eu",
            application_key=os.getenv("OVH_APP_KEY"),
            application_secret=os.getenv("OVH_APP_SECRET"),
            consumer_key=os.getenv("OVH_CONSUMER_KEY"),
        )

        # Liste des domaines à mettre à jour
        domains = ["prometheus.my-soc.fr", "iris.my-soc.fr", "kibana.my-soc.fr", "doctobobo.my-soc.fr"]

        for domain in domains:
            record_name = domain.split(".")[0]
            zone_name = ".".join(domain.split(".")[1:])
            print(f"Updating {domain} to point to {ip}...")
            
            # Récupération des enregistrements DNS existants
            records = client.get(f"/domain/zone/{zone_name}/record", fieldType="A", subDomain=record_name)

            # Suppression des anciens enregistrements
            for record_id in records:
                client.delete(f"/domain/zone/{zone_name}/record/{record_id}")
                print(f"Deleted record {record_id} for {domain}")

            # Création du nouvel enregistrement
            client.post(f"/domain/zone/{zone_name}/record", fieldType="A", subDomain=record_name, target=ip, ttl=3600)
            print(f"Added new A record for {domain} pointing to {ip}")

            # Rafraîchissement de la zone DNS
            client.post(f"/domain/zone/{zone_name}/refresh")
            print(f"Zone {zone_name} refreshed.")

        print("All domains updated successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update OVH domain records.")
    parser.add_argument("--ip", required=True, help="Load Balancer IP address")
    args = parser.parse_args()

    update_domains(args.ip)
