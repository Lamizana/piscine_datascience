# Piscine datascience [0]

> Created by alex lamizana in 06/12/2024
----------------------------------------------------------------------------

## Data Ingineer: Creation d'une DataBase

## [Index](/README.md)

## Sommaire

1. [Règles générales.](#règles-générales)
2. [Introduction.](#introduction)
3. [Exercice 00: Create postgres DB.](#exercice-00)
4. [Exercice 01: Show me your DB.](#exercice-01)
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

### Notion abordees

Pour pouvoir créer une base de données, il faut que le serveur ***PostgreSQL*** soit lancé.

Pour verifier si postgres est bien installee:
```bash
$> psql --version
psql (PostgreSQL) 16.6 (Ubuntu 16.6-0ubuntu0.24.04.1)
$>
```

Pour vérifier si le service PostgreSQL est en cours d'exécution sur notre système :

```bash
>$ sudo systemctl status postgresql
● postgresql.service - PostgreSQL RDBMS
     Loaded: loaded (/usr/lib/systemd/system/postgresql.service; enabled; preset: enabled)
     Active: active (exited) since Fri 2024-12-06 16:17:33 CET; 15min ago
   Main PID: 109196 (code=exited, status=0/SUCCESS)
        CPU: 1ms

Dec 06 16:17:33 alex-Vm systemd[1]: Starting postgresql.service - PostgreSQL RDBMS...
Dec 06 16:17:33 alex-Vm systemd[1]: Finished postgresql.service - PostgreSQL RDBMS.
$>
```

Pour acceder a Postgres :
```bash
>$ sudo -i -u postgres
postgres@alex-Vm:~$ psql
psql (16.6 (Ubuntu 16.6-0ubuntu0.24.04.1))
Type "help" for help.

postgres=# 
```

Creation d'un utilisateur avec tous les droits :
```bash
>$ sudo -i -u postgres
postgres@alex-Vm:~$ psql
psql (16.6 (Ubuntu 16.6-0ubuntu0.24.04.1))
Type "help" for help.

postgres=# CREATE ROLE alamizan LOGIN SUPERUSER PASSWORD 'mysecretpassword';
```

Pour creer une base de donnee :
```bash
>$ sudo -i -u postgres
postgres@alex-Vm:~$ createdb ma_base
```

Pour sortir de psql, saisir :

```bash
>$ ma_base=> \q
```

POur avoir toutes les commandes psql :
```bash
>$ ma_base=> \?
>$ ma_base=> \h
```

Pour supprimer une db:
```bash
postgres@alex-Vm:~$ dropdb ma_db
```

----------------------------------------------------------------------------

## Exercice 01

### Show me your DB

- Turn-in directory : ***ex01/***
- Files to turn in : None
- Allowed functions : pgadmin, Postico, dbeaver or what you want to see the db easily

- Trouver un moyen de visualiser facilement la base de données à l'aide d'un logiciel.
- Le logiciel choisi doit vous permettre de trouver et de manipuler facilement les données en utilisant leur propre
ID correspondant

### Notion abordees

Pour installer pgAdmin :
```bash
sudo snap install pgadmin4
```
