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





