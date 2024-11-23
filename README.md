# ssi : sécurité du système d'information

------ Terraform ------ 

création des ressources suivantes:

  - Load balancer x1
  - cluster x1
  - pool x1
  - noeud x1
  - ip public x1
  - private virtual network

la configuration est dans ./infra/infra.tf

------ GitHub Action ------

configuration nécéssaire : Oui (clé API de scw et de Hashicorp cloud sur Github secret manager)

- création de deux workflow :
  -> deploy : instancie les ressources sur SCW
  -> destroy_all : détruit toutes les ressources sur SCW

- workflow pour installer les chartes helm :
  -> deploy helm charts


les fichiers de configurations sont situé dans :
.github/workflows/

------- Hashicorp cloud ------

configuration nécéssaire : Oui (clé API de scw dans le secret manager/ déclenchement manuel)

création d'un cloud pour stocker en temps réel l'état de la configuration cloud SCW.

------- Scaleway

création d'un compte cloud Scaleway



todo network :

kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml
kubectl apply -f ./infra/network.yaml

edit ovh dns : il faut que dans l'entrée 'A record' il y est l'adresse ip du load balancer
dans scaleway:
dans l'onglet du load balancer : 
  créer un certificat SSL avec le bon nom de domaine : exemple : prometheus.my-soc.fr
  créer un backend : mettre les ip privée des nodes (serveurs)
  créer un frontend : port 443, applicquer le certificat / appliquer le backend





