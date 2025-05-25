# Piscine datascience [1]

> Created by alex lamizana in 26/01/2025
----------------------------------------------------------------------------

## Data Warehouse: Gestion et comprehension ETL

### [Index](/README.md)

### Sommaire

- [Règles générales](#règles-générales)
- [Introduction](#introduction)
- [Exercice 00 : American apple Pie](#exercice-00)
- [Exercice 01 : initial data exploration](#exercice-01)
- [Exercice 02: Remove duplicates](#exercice-02)
- [Exercice 03: Fusion](#exercice-03)

----------------------------------------------------------------------------

## Règles générales

- Effectuer le rendu des modules à partir d'un ordinateur du cluster, soit en utilisant une machine virtuelle :
  - Choisir le système d'exploitation à utiliser pour votre machine virtuelle
  - Votre machine virtuelle doit disposer de tous les logiciels nécessaires à la réalisation de votre projet.
  - Ces logiciels doivent être configurés et installés.

- On peux également utiliser l'ordinateur directement si les outils sont disponibles.
  - S'assurer d'avoir l'espace nécessaire sur notre session pour installer ce dont on à besoin pour tous les modules (utilisez le goinfre si votre campus en dispose).
  - Tous doit etre installé installé avant les évaluations.

- On peux également utiliser l'ordinateur directement si les outils sont disponibles.
  - S'assurer d'avoir l'espace nécessaire sur notre session pour installer ce dont on à besoin pour tous les modules (utilisez le goinfre si votre campus en dispose).
  - Tous doit etre installé installé avant les évaluations.

- Nos fonctions ne doivent pas se terminer de manière inattendue (erreur de segmentation, erreur de bus, double libération, etc.)

> Si cela se produit, votre projet sera considéré comme non fonctionnel et recevra un 0 lors de l'évaluation.

- Nous vous encourageons à créer des programmes de test pour votre projet, même si ce travail ne devra pas être présenté et ne sera pas noté.
Cela vous donnera l'occasion de tester facilement votre travail et celui de vos camarades.
Ces tests vous seront particulièrement utiles lors de votre soutenance.
En effet, lors de la soutenance, vous êtes libre d'utiliser vos tests
et/ou les tests du pair que vous évaluez.

- Soumettez votre travail au dépôt git qui vous a été attribué. Seul le travail dans le dépôt git sera noté. Si Deepthought est chargé de noter votre travail, il le fera
après l'évaluation par les pairs.

> [!NOTE]
> Si une erreur se produit dans une section de votre travail
> pendant l'évaluation de Deepthought, l'évaluation sera interrompue.

----------------------------------------------------------------------------

## Introduction

Le rôle du data analyst est de comprendre les données passées et présentes, de faire des graphiques pour expliquer aux équipes les " chiffres " (reporting), et d'être force de proposition pour apporter des solutions, de créer des outils d'aide à la décision.
Ils utilisent souvent des outils tels que techno R, Excel, Power BI, Jupyter Notebook>
A vous de trouver les outils qui vous conviennent. Vous êtes libre d'utiliser la langue de votre choix pour ce module.

> [!NOTE]
> Attention à cette "piscine". Même si vous parvenez à valider un module,vous risquez d'être bloqué plus tard si vous n'avez pas nettoyé ou stocké vos données correctement.

Tous les graphiques ont été réalisés sans les données de février, vous devez les refaire avec les nouvelles données.

Connexion a la base de donnees piscineds :

```bash
$> psql -U your_login -d piscineds -h localhost -W
mysecretpassword
piscineds=#
```

----------------------------------------------------------------------------

## Exercice 00

### American apple Pie

|                                   |
| :-------------------------------- |
| **Turn-in directory** :  *ex00/*  |
| **Files to turn in**  :  *pie.**   |
| **Allowed functions** :  *All*    |

> [pie.py](/data_analyst/ex00/pie.py)

- Créez votre propre **diagramme circulaire** pour comprendre ce que les gens font sur le site..
- Vous devez vous connecter à votre base de données data Warehouse du ***module 01***.

----------------------------------------------------------------------------

## Exercice 01

### Initial data exploration

|                                                   |
| :------------------------------------------------ |
| **Turn-in directory** :  *ex01/*                  |
| **Files to turn in**  :  **chart.***    |
| **Allowed functions** :  *All*                    |

> [chart.py](/data_analyst/ex01/chart.py)

- Ne conservez que les données ***« purchase »*** de la colonne ***« event_type »***. Vous devez vous connecter à votre Data Warehouse du module 01.

- Tous les prix sont en Dollars Altairiens, vous savez l'argent qui est dans votre portefeuille ?

- Vous devez créer 3 graphiques du début du mois d'octobre 2022 à la fin du mois de février 2023.

----------------------------------------------------------------------------

## Exercice 02

----------------------------------------------------------------------------

### Remove duplicates

|                                                     |
| :------------------------------------------------   |
| **Turn-in directory** :  *ex02/*                    |
| **Files to turn in**  :  **remove_duplicates.***    |
| **Allowed functions** :  *All*                      |

> [remove_duplicates.py](/data_warehouse/ex02/remove_duplicates.py)

- Supprimer les lignes en double dans la table ***"customers"***.

> [!WARNING]
> Parfois, le serveur envoie la même instruction à 1 seconde d'intervalle.
> Vous devez donc également les supprimer.

```sql
DELETE FROM customers
WHERE ctid NOT IN (
    SELECT MIN(ctid)
    FROM customers
    GROUP BY  event_time, event_type, product_id, price, user_id, user_session
);
```

----------------------------------------------------------------------------

## Exercice 03

----------------------------------------------------------------------------

### Fusion

|                                                     |
| :------------------------------------------------   |
| **Turn-in directory** :  *ex03/*                    |
| **Files to turn in**  :  **fusion.***               |
| **Allowed functions** :  *All*                      |

> [fusion.py](/data_warehouse/ex03/fusion.py)

- Combiner les tables ***"customers"*** avec les ***"items"*** de la table ***"customers"***.

Commandes :