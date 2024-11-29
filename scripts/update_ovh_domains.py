import ovh
import argparse

def update_domains(ip):
    client = ovh.Client(
        endpoint="ovh-eu",
        application_key="${{ secrets.OVH_APP_KEY }}",
        application_secret="${{ secrets.OVH_APP_SECRET }}",
        consumer_key="${{ secrets.OVH_CONSUMER_KEY }}"
    )

    domains = ["prometheus.my-soc.fr", "iris.my-soc.fr", "kibana.my-soc.fr", "doctobobo.my-soc.fr"]

    for domain in domains:
        record_name = domain.split(".")[0]
        zone_name = ".".join(domain.split(".")[1:])
        print(f"Updating {domain} to point to {ip}...")
        records = client.get(f"/domain/zone/{zone_name}/record", fieldType="A", subDomain=record_name)

        for record_id in records:
            client.delete(f"/domain/zone/{zone_name}/record/{record_id}")

        client.post(f"/domain/zone/{zone_name}/record", fieldType="A", subDomain=record_name, target=ip, ttl=3600)
        client.post(f"/domain/zone/{zone_name}/refresh")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update OVH domain records.")
    parser.add_argument("--ip", required=True, help="Load Balancer IP address")
    args = parser.parse_args()

    update_domains(args.ip)
