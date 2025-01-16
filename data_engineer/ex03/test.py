import psycopg2
import csv
import os
from psycopg2 import sql

# Configuration de la connexion à PostgreSQL
db_config = {
    "host": "localhost",          # Adresse du serveur PostgreSQL
    "port": 5432,                 # Port PostgreSQL
    "database": "piscineds",  # Nom de votre base de données
    "user": "postgres",          # Nom de l'utilisateur PostgreSQL
    "password": "Lamizana@1987"   # Mot de passe PostgreSQL
}

target_user = 'alamizan'

# Chemin vers le fichier CSV
csv_file_path = "/tmp/subject/customer/data_2022_nov.csv"

# Nom de la table à créer/importer
table_name = "data_2022_dec"

# Définition des types de colonnes
column_types = {
    "event_time": "TIMESTAMP",
    "event_type": "VARCHAR(50)",
    "product_id": "INTEGER",
    "price": "DECIMAL(10,2)",
    "user_id": "INTEGER",
    "user_session": "VARCHAR(50)"
}

def create_table_and_import_csv_with_types(csv_path, table, db_params, column_types):
    try:
        # Connexion à PostgreSQL
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Lecture du fichier CSV pour détecter les colonnes
        with open(csv_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            headers = next(csv_reader)  # Extraction des colonnes (première ligne du CSV)


        # Validation des colonnes par rapport aux types définis
        for col in headers:
            if col not in column_types:
                raise ValueError(f"Aucun type défini pour la colonne '{col}'.")

            # Création de la table
            columns_with_types = ", ".join([f"{col} {column_types[col]}" for col in headers])
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table} ({columns_with_types});"
            cursor.execute(create_table_query)
            print(f"Table '{table}' créée avec succès ou déjà existante.")

            # Utiliser COPY pour insérer les données directement dans la table
            with open(csv_file_path, 'r') as f:
                # table_name = os.path.splitext(f)[0]  # Enlever l'extension .csv
                next(f)  # Ignore the header row
                cursor.copy_from(f, table_name, sep=',', null='')  # Charger les données du CSV dans la table
            
 
            # --------------------------------------------------------------- #
            # 1. Accorder tous les privilèges sur la base de données
            cursor.execute(sql.SQL("GRANT ALL PRIVILEGES ON DATABASE {} TO {};").format(
                sql.Identifier("piscineds"),
                sql.Identifier(target_user)
            ))

            # 2. Accorder tous les privilèges sur toutes les tables existantes dans le schéma public
            cursor.execute(sql.SQL("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO {};").format(
            sql.Identifier(target_user)
            ))
            # --------------------------------------------------------------- #


            # Validation des modifications
            conn.commit()
            print(f"Les données du fichier '{csv_path}' ont été importées avec succès dans la table '{table}'.")

    except Exception as e:
        print(f"Erreur : {e}")

    finally:
        # Fermeture des connexions
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Appel de la fonction
create_table_and_import_csv_with_types(csv_file_path, table_name, db_config, column_types)
