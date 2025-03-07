# ssi : sécurité du système d'information

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






