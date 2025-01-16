# Commandes psql

> Created by alex lamizana 14/01/2025
----------------------------------------------------------------------------

## [Index](/README.md)

### Sommaire

1. [Introduction.](#introduction)
2. [Commandes principales.](#commandes-principales)
3. [General.](#general)
4. [help.](#help)
5. [Query Buffer.](#query-buffer)

----------------------------------------------------------------------------

## Introduction

Pour acceder a Postgres :

```bash
$> sudo -i -u postgres
postgres@alex-Vm:~$ psql
postgres=# 
```

----------------------------------------------------------------------------

## Commandes principales

### Commandes de base

```sql
\l                      - Afficher les bases de données.
\c nom_de_la_base       - Se connecter à une base de données spécifique.
\dt                     - Lister les tables dans la base.
\d nom_de_la_table      - Afficher les colonnes d'une table .
\du                     - Liste tous les utilisateurs.
```

### Gestion des bases de données

- Créer une base de données :

  ```sql
  CREATE DATABASE nom_base;
  ```

- Supprimer une base de données :

  ```sql
  DROP DATABASE nom_base;
  ```

### Gestion des utilisateurs

- Créer un utilisateur :

  ```sql
  CREATE USER nom_utilisateur WITH PASSWORD 'mot_de_passe';
  ```

- Supprimer un utilisateur :

  ```sql
  DROP USER nom_utilisateur;
  ```

- Attribuer des droits à un utilisateur :

  ```sql
  GRANT ALL PRIVILEGES ON DATABASE nom_base TO nom_utilisateur;
  ```

- Retirer des droits à un utilisateur :

  ```sql
  REVOKE ALL PRIVILEGES ON DATABASE nom_base FROM nom_utilisateur;
  ```

### Gestion des tables

- Créer une table :

  ```sql
  CREATE TABLE nom_table (
    colonne1 TYPE1,
    colonne2 TYPE2,
    ...
  );
  ```

- Supprimer une table :

  ```sql
  DROP TABLE nom_table;
  ```

- Modifier une table (ajouter une colonne) :

  ```sql
  ALTER TABLE nom_table ADD COLUMN nom_colonne TYPE;
  ```

- Modifier une table (supprimer une colonne) :

  ```sql
  ALTER TABLE nom_table DROP COLUMN nom_colonne;
  ```

### Gestion des donnees

- Insérer des données :

  ```sql
  INSERT INTO nom_table (colonne1, colonne2) VALUES (valeur1, valeur2);
  ```

- Mettre à jour des données :

  ```sql
  UPDATE nom_table SET colonne1 = nouvelle_valeur WHERE condition;
  ```

- Supprimer des données :

  ```sql
  DELETE FROM nom_table WHERE condition;
  ```

- Lire des données :

  ```sql
  SELECT colonne1, colonne2 FROM nom_table WHERE condition;
  ```

----------------------------------------------------------------------------

## General

```sql
\bind [PARAM]...        - Définir les paramètres de la requête.

\copyright              - Montrer les conditions d'utilisation et de 
                          distribution de PostgreSQL.

\crosstabview [COLUMNS] - Exécuter la requête et afficher le résultat dans 
                            un tableau croisé

\errverbose             - Afficher le message d'erreur le plus récent à 
                            la verbosité maximale.

\g [(OPTIONS)] [FILE]   - Exécute la requête (et envoie le résultat 
                          dans un fichier ou dans le tuyau) ;
                            - \g sans argument est équivalent à un point-virgule.

\gdesc                  - Décrire le résultat d'une requête, sans l'exécuter.

\gexec                  - Exécuter la requête, puis exécuter chaque valeur 
                          dans son résultat.

\gset [PREFIX]          - Exécuter une requête et stocker le résultat dans 
                          des variables psql.

\gx [(OPTIONS)] [FILE]  - Comme \g, mais force le mode de sortie étendu.

\q                      - Quitte psql.

\watch [[i=]SEC] [c=N]  - Exécuter la requête toutes les SEC secondes, 
                            jusqu'à N fois.
```

----------------------------------------------------------------------------

## Help

```bash
\? [commands]         - Afficher l'aide sur les commandes backslash.

\? options            - Afficher l'aide sur les options de la ligne de commande psql.

\? variables          - Afficher l'aide sur les variables spéciales.

\h [NAME]             - Aide sur la syntaxe des commandes SQL, 
                        * pour toutes les commandes.
```

----------------------------------------------------------------------------

## Query Buffer

```bash
\e [FILE] [LINE]       edit the query buffer (or file) with external editor
\ef [FUNCNAME [LINE]]  edit function definition with external editor
\ev [VIEWNAME [LINE]]  edit view definition with external editor
\p                     show the contents of the query buffer
\r                     reset (clear) the query buffer
\s [FILE]              display history or save it to file
\w FILE                write query buffer to file
```

----------------------------------------------------------------------------

## Input/Output

```bash
  \copy ...              perform SQL COPY with data stream to the client host
  \echo [-n] [STRING]    write string to standard output (-n for no newline)
  \i FILE                execute commands from file
  \ir FILE               as \i, but relative to location of current script
  \o [FILE]              send all query results to file or |pipe
  \qecho [-n] [STRING]   write string to \o output stream (-n for no newline)
  \warn [-n] [STRING]    write string to standard error (-n for no newline)
```

----------------------------------------------------------------------------

## Conditional

```bash
  \if EXPR               begin conditional block
  \elif EXPR             alternative within current conditional block
  \else                  final alternative within current conditional block
  \endif                 end conditional block
```

----------------------------------------------------------------------------

## Informational

```bash
  (options: S = show system objects, + = additional detail)
  \d[S+]                 list tables, views, and sequences
  \d[S+]  NAME           describe table, view, sequence, or index
  \da[S]  [PATTERN]      list aggregates
  \dA[+]  [PATTERN]      list access methods
  \dAc[+] [AMPTRN [TYPEPTRN]]  list operator classes
  \dAf[+] [AMPTRN [TYPEPTRN]]  list operator families
  \dAo[+] [AMPTRN [OPFPTRN]]   list operators of operator families
  \dAp[+] [AMPTRN [OPFPTRN]]   list support functions of operator families
  \db[+]  [PATTERN]      list tablespaces
  \dc[S+] [PATTERN]      list conversions
  \dconfig[+] [PATTERN]  list configuration parameters
  \dC[+]  [PATTERN]      list casts
  \dd[S]  [PATTERN]      show object descriptions not displayed elsewhere
  \dD[S+] [PATTERN]      list domains
  \ddp    [PATTERN]      list default privileges
  \dE[S+] [PATTERN]      list foreign tables
  \des[+] [PATTERN]      list foreign servers
  \det[+] [PATTERN]      list foreign tables
  \deu[+] [PATTERN]      list user mappings
  \dew[+] [PATTERN]      list foreign-data wrappers
  \df[anptw][S+] [FUNCPTRN [TYPEPTRN ...]]
                         list [only agg/normal/procedure/trigger/window] functions
  \dF[+]  [PATTERN]      list text search configurations
  \dFd[+] [PATTERN]      list text search dictionaries
  \dFp[+] [PATTERN]      list text search parsers
  \dFt[+] [PATTERN]      list text search templates
  \dg[S+] [PATTERN]      list roles
  \di[S+] [PATTERN]      list indexes
  \dl[+]                 list large objects, same as \lo_list
  \dL[S+] [PATTERN]      list procedural languages
  \dm[S+] [PATTERN]      list materialized views
  \dn[S+] [PATTERN]      list schemas
  \do[S+] [OPPTRN [TYPEPTRN [TYPEPTRN]]]
\dO[S+] [PATTERN]      list collations
  \dp[S]  [PATTERN]      list table, view, and sequence access privileges
  \dP[itn+] [PATTERN]    list [only index/table] partitioned relations [n=nested]
  \drds [ROLEPTRN [DBPTRN]] list per-database role settings
  \drg[S] [PATTERN]      list role grants
  \dRp[+] [PATTERN]      list replication publications
  \dRs[+] [PATTERN]      list replication subscriptions
  \ds[S+] [PATTERN]      list sequences
  \dt[S+] [PATTERN]      list tables
  \dT[S+] [PATTERN]      list data types
  \du[S+] [PATTERN]      list roles
  \dv[S+] [PATTERN]      list views
  \dx[+]  [PATTERN]      list extensions
  \dX     [PATTERN]      list extended statistics
  \dy[+]  [PATTERN]      list event triggers
  \l[+]   [PATTERN]      list databases
  \sf[+]  FUNCNAME       show a function's definition
  \sv[+]  VIEWNAME       show a view's definition
  \z[S]   [PATTERN]      same as \dp
```

----------------------------------------------------------------------------

## Large Objects

```bash
  \lo_export LOBOID FILE write large object to file
  \lo_import FILE [COMMENT]
                         read large object from file
  \lo_list[+]            list large objects
  \lo_unlink LOBOID      delete a large object
```

----------------------------------------------------------------------------

## Formatting

```bash
  \a                     toggle between unaligned and aligned output mode
  \C [STRING]            set table title, or unset if none
  \f [STRING]            show or set field separator for unaligned query output
  \H                     toggle HTML output mode (currently off)
  \pset [NAME [VALUE]]   set table output option
                         (border|columns|csv_fieldsep|expanded|fieldsep|
                         fieldsep_zero|footer|format|linestyle|null|
                         numericlocale|pager|pager_min_lines|recordsep|
                         recordsep_zero|tableattr|title|tuples_only|
                         unicode_border_linestyle|unicode_column_linestyle|
                         unicode_header_linestyle)
  \t [on|off]            show only rows (currently off)
  \T [STRING]            set HTML <table> tag attributes, or unset if none
  \x [on|off|auto]       toggle expanded output (currently off)
```

----------------------------------------------------------------------------

## Connection

```bash
  \c[onnect] {[DBNAME|- USER|- HOST|- PORT|-] | conninfo}
                         connect to new database (currently "piscineds")
  \conninfo              display information about current connection
  \encoding [ENCODING]   show or set client encoding
  \password [USERNAME]   securely change the password for a user
```

----------------------------------------------------------------------------

## Operating System

```bash
  \cd [DIR]              change the current working directory
  \getenv PSQLVAR ENVVAR fetch environment variable
  \setenv NAME [VALUE]   set or unset environment variable
  \timing [on|off]       toggle timing of commands (currently off)
  \! [COMMAND]           execute command in shell or start interactive shell
```

----------------------------------------------------------------------------

## Variables

```bash
  \prompt [TEXT] NAME    prompt user to set internal variable
  \set [NAME [VALUE]]    set internal variable, or list all if no parameters
  \unset NAME            unset (delete) internal variable
```
