# Piscine datascience [1]

> Created by alex lamizana in 26/01/2025
----------------------------------------------------------------------------

## Data Warehouse: Gestion et comprehension ETL

### [Index](/README.md)

### Sommaire

- [Règles générales](#règles-générales)
- [Introduction](#introduction)
- [Exercice 00: Show me your DB](#exercice-00)
- [Exercice 01: First table](#exercice-01)
- [Exercice 02: Remove duplicates](#exercice-02)

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

L'***ETL***, qui signifie *extraction, transformation et chargement*, est un processus d'intégration des données qui consiste à combine des données provenant de plusieurs sources de données en un magasin de données unique et cohérent qui est chargé dans un entrepôt de données.

```
data source : __
                |__ ETL --> Data Warehouse
data source : __|
```

> [!WARNING]
> Attention à cette "piscine". Même si vous parvenez à valider un module
> module, vous risquez d'être bloqué plus tard si vous n'avez pas nettoyé ou stocké
> ou stocké vos données correctement.

----------------------------------------------------------------------------

## Exercice 00

----------------------------------------------------------------------------

### Show me your DB

|                                   |
| :-------------------------------- |
| **Turn-in directory** :  *ex00/*  |
| **Files to turn in**  :  *None*   |
| **Allowed functions** :  *pgadmin, Postico, dbeaver or what you want to see the db easily*    |

- Trouver un moyen de *visualiser facilement la base de données* à l'aide d'un logiciel.
- Le logiciel choisi doit vous permettre de trouver et de manipuler facilement les données en utilisant leur propre ID correspondant.

----------------------------------------------------------------------------

## Exercice 01

----------------------------------------------------------------------------

### First table

|                                                   |
| :------------------------------------------------ |
| **Turn-in directory** :  *ex01/*                  |
| **Files to turn in**  :  **customers_table.***    |
| **Allowed functions** :  *All*                    |

> [customers_table.py](/data_warehouse/ex01/customers_table.py)

- Réunir toutes les tables `data_202*_***` dans une table appelée ***"customers"***.

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
