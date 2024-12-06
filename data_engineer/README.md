# Piscine datascience [0]

> Created by alex lamizana in 06/12/2024
----------------------------------------------------------------------------

## Data Ingineer: Creation d'une DataBase

## [Index](/README.md)

## Sommaire

1. [Règles générales.](#règles-générales)
2. [Introduction.](#introduction)
3. [Exercice 00: First python script.](#exercice-00)
4. [Exercice 01: First use of package.](#exercice-01)
5. [Exercice 02: First function python.](#exercice-02)
6. [Exercice 03: NULL not found.](#exercice-03)
7. [Exercice 04: The Even and the Odd.](#exercice-04)

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

Dans les deux prochains modules, on va voir le rôle d'un ***Data ingénieur***.

Il est important de comprendre cette deuxième étape. **L'ingénieur des données « nettoie » les données et les transforme** afin de disposer de données prêtes à être analysées par les analystes/scientifiques des données.

Le module suivant concerne le nettoyage des données. Cette deuxième étape est importante pour comprendre que l'ingénieur des données « nettoie » les données et les transforme.
L'objectif est d'avoir des données prêtes à être analysées par les analystes/scientifiques des données.

Nous sommes fin février 2022, c'est votre premier jour dans une entreprise de vente d'articles sur Internet. Avant de partir en voyage, votre patron vous remet les ventes des 4 derniers mois.
*Vous devrez les exploiter et proposer des solutions pour augmenter le chiffre d'affaires de l'entreprise.*

> [!WARNING]
> Attention à cette "piscine". Même si vous parvenez à valider un module
> module, vous risquez d'être bloqué plus tard si vous n'avez pas nettoyé ou stocké
> ou stocké vos données correctement.

----------------------------------------------------------------------------

## Exercice 00

### Create postgres DB

- Turn-in directory : ***ex00/***
- Files to turn in : None
- Allowed functions : All

Pour cet exercice, on peut utiliser directement *postgres* s'il est installé sur votre campus ou passer par une VM, sinon utiliser docker compose.

- Le nom d'utilisateur est votre login étudiant.
- Le nom de la base de données est **piscineds**.
- Le mot de passe est **"mysecretpassword"**.

Nous devons être en mesure de nous connecter à votre base de données posgress avec cette commande :

```bash
$> psql -U your_login -d piscineds -h localhost -W
mysecretpassword
piscineds=#
```
