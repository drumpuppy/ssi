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



- supprimer le load balancer de terraform (Ip, pvn)
- git hub workflow :creer un nouveau workflow network par exemple
    ajouter une étape :
    kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml
    kubectl apply -f ./Ingress/network.yaml
    ajouter l'étape OVH:
      modifier les entrée dns avec l'ip du nouveau load balancer : récupérer l'adresse ip de scaleway du load.
    dernière étape du workflow 
    kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.11.0/cert-manager.yaml
    kubectl apply -f ./ingress/clusterIssuer.yaml

- modifier le workflow Delete_All()
      - kubectl delete -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml
        kubectl delete -f ./Ingress/network.yaml
        kubectl delete -f https://github.com/cert-manager/cert-manager/releases/download/v1.11.0/cert-manager.yaml
        kubectl delete -f ./ingress/clusterIssuer.yaml




