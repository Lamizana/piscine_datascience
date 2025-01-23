# Utilisation et commandes PgAdmin4

> Created by alex lamizana 14/01/2025
----------------------------------------------------------------------------

## [Index](/README.md)

## Sommaire

1. [Presentation.](#presentation)
2. [Utilisation.](#utilisation)
3. [Commandes.](#commandes)

----------------------------------------------------------------------------

## Presentation

Pour installer pgAdmin :

```bash
sudo snap install pgadmin4
```

Pour lancer PgAdmin

```bash
sudo snap install pgadmin4
```

----------------------------------------------------------------------------

## Utilisation

### Creation Database

### Creation Table

### Importer un fichier CSV

Utiliser l'outil de requête et saisir une requête SQL. Pour ce faire, utilisez l'instruction **COPY**:

```bash
COPY characters
FROM '/home/lamizana/Documents/datascience/data_engineer'
DELIMITER ','
CSV HEADER;
```

----------------------------------------------------------------------------

## Commandes
