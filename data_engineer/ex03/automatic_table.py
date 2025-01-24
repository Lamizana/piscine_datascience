import os
import pandas as pd
import psycopg2
from psycopg2 import sql

# Configuration de la connexion PostgreSQL
DB_HOST = 'localhost'
DB_PORT = '5432'  # Port PostgreSQL par défaut
DB_NAME = 'piscineds'
DB_USER = 'postgres'
DB_PASSWORD = 'Lamizana@1987'

target_user = 'alamizan'

# Dossier contenant les fichiers CSV
csv_directory = '/home/lamizana/subject/customer2/'

# Connexion à la base de données PostgreSQL
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

column_types = {
    "event_time": "TIMESTAMP",
    "event_type": "VARCHAR(50)",
    "product_id": "INTEGER",
    "price": "DECIMAL(10,2)",
    "user_id": "INTEGER",
    "user_session": "VARCHAR(50)"
}

# Création d'un curseur pour exécuter des requêtes
cur = conn.cursor()

# Parcourir tous les fichiers dans le dossier CSV
for filename in os.listdir(csv_directory):
    if filename.endswith('.csv'):
        # Construire le chemin complet du fichier CSV
        csv_file_path = os.path.join(csv_directory, filename)
        
        # Lire le fichier CSV dans un DataFrame
        df = pd.read_csv(csv_file_path)
        
        # Nom de la table basé sur le nom du fichier CSV
        table_name = os.path.splitext(filename)[0]  # Enlever l'extension .csv
        
        # Créer la table dans PostgreSQL à partir du DataFrame
        # Construire la requête CREATE TABLE dynamique
        columns = df.columns
        column_definitions = ', '.join([f"{col} {column_types[col]}" for col in columns])  # Définit chaque colonne comme de type TEXT par défaut
        create_table_query = sql.SQL("""
            CREATE TABLE IF NOT EXISTS {table_name} (
                {columns}
            );
        """).format(
            table_name=sql.Identifier(table_name),
            columns=sql.SQL(column_definitions)
        )
        
        # Exécuter la création de la table
        cur.execute(create_table_query)
        
        # Utiliser COPY pour insérer les données directement dans la table
        with open(csv_file_path, 'r') as f:
            next(f)  # Ignore the header row
            cur.copy_from(f, table_name, sep=',', null='')  # Charger les données du CSV dans la table
        
        # --------------------------------------------------------------- #
        # 1. Accorder tous les privilèges sur la base de données
        cur.execute(sql.SQL("GRANT ALL PRIVILEGES ON DATABASE {} TO {};").format(
            sql.Identifier(DB_NAME),
            sql.Identifier(target_user)
        ))

        # 2. Accorder tous les privilèges sur toutes les tables existantes dans le schéma public
        cur.execute(sql.SQL("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO {};").format(
        sql.Identifier(target_user)
        ))
        # --------------------------------------------------------------- #

        # Commit des changements
        conn.commit()

# Fermer le curseur et la connexion
cur.close()
conn.close()

print("Les fichiers CSV ont été importés avec succès dans la base de données PostgreSQL.")
