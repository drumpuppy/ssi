# ssi : sécurité du système d'information



-------Dépendance--------
terraform
K8s scaleway
dns ovh
slack pour les alertes

--> configurer les secret dans github actions pour utiliser les workflows

------ Terraform ------ 

création des ressources suivantes:

  - Load balancer x1
  - cluster x1
  - pool x1
  - noeud x3
  - ip public x1
  - private virtual network x1

la configuration est dans ./infra/infra.tf

------ GitHub Action ------

configuration nécéssaire : Oui (clé API de scw et de Hashicorp cloud sur Github secret manager)

- création de deux workflow :
  -> deploy all : instancie les ressources sur SCW
  -> destroy_all : détruit toutes les ressources sur SCW

- workflow pour installer les chartes helm :
  -> deploy helm charts

- workflow pour installer les configs réseau :
  -> deploy network

les fichiers de configurations sont situé dans :
.github/workflows/

------- Hashicorp cloud ------

configuration nécéssaire : Oui (clé API de scw dans le secret manager/ déclenchement manuel)

création d'un cloud pour stocker en temps réel l'état de la configuration cloud SCW.

------- Scaleway

création d'un compte cloud Scaleway



------- Stack helm/kustomize

SIEM :
- filebeat -> logstash -> elasticsearch -> kibana
Detection
- istio / falco
SOAR :
- wazuh

--------Stack reseau
- load balancer ingress nginx 

------ Accès réseau
kibana2.my-soc.fr :
- elastic
- kubectl get secret elasticsearch-master-credentials -n default -o jsonpath='{.data.password}' | base64 --decode && echo

wazuh:
kubectl get secret dashboard-cred -n wazuh -o jsonpath='{.data.username}' | base64 --decode && echo
kubectl get secret dashboard-cred -n wazuh -o jsonpath='{.data.password}' | base64 --decode && echo


----------- Annexe 


falco
helm upgrade --install falco falcosecurity/falco -f ./values-falco.yaml --namespace default

istio
helm upgrade --install istio-base istio/base -n istio-system --create-namespace
helm upgrade --install istiod istio/istiod -f values-istio.yaml -n istio-system

opensearch
helm repo add opensearch https://opensearch-project.github.io/helm-charts/
helm install opensearch opensearch/opensearch -f values-opensearch.yaml

opensearch dashboard
helm install opensearch-dashboards opensearch/opensearch-dashboards -f values-opensearch-dashboard.yaml


wazuh
git clone https://github.com/wazuh/wazuh-kubernetes.git -b v4.11.0 --depth=1
cd wazuh-kubernetes


# Générer les certificats pour l'indexeur Wazuh
openssl genrsa -out root-ca-key.pem 2048
openssl req -x509 -new -nodes -key root-ca-key.pem -sha256 -days 3650 -out root-ca.pem -subj "//C=US\ST=California\L=San Francisco\O=Company\CN=root-ca"

openssl genrsa -out admin-key.pem 2048
openssl req -new -key admin-key.pem -out admin.csr -subj "//C=US\ST=California\L=San Francisco\O=Company\CN=admin"
openssl x509 -req -in admin.csr -CA root-ca.pem -CAkey root-ca-key.pem -CAcreateserial -out admin.pem -days 3650 -sha256

openssl genrsa -out node-key.pem 2048
openssl req -new -key node-key.pem -out node.csr -subj "//C=US\ST=California\L=San Francisco\O=Company\CN=node"
openssl x509 -req -in node.csr -CA root-ca.pem -CAkey root-ca-key.pem -CAcreateserial -out node.pem -days 3650 -sha256

openssl genrsa -out dashboard-key.pem 2048
openssl req -new -key dashboard-key.pem -out dashboard.csr -subj "//C=US\ST=California\L=San Francisco\O=Company\CN=dashboard"
openssl x509 -req -in dashboard.csr -CA root-ca.pem -CAkey root-ca-key.pem -CAcreateserial -out dashboard.pem -days 3650 -sha256

openssl genrsa -out filebeat-key.pem 2048
openssl req -new -key filebeat-key.pem -out filebeat.csr -subj "//C=US\ST=California\L=San Francisco\O=Company\CN=filebeat"
openssl x509 -req -in filebeat.csr -CA root-ca.pem -CAkey root-ca-key.pem -CAcreateserial -out filebeat.pem -days 3650 -sha256


# Générer les certificats pour le Dashboard Wazuh
bash wazuh/certs/dashboard_http/generate_certs.sh


edit wazuh/base/storage-class with 

apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: wazuh-storage
provisioner: csi.scaleway.com


retirer le management des storage dans kustomize

edit les sts avec 1 replicas, plus de mem ram, et 10Gi de stockage

kubectl apply -k wazuh/




