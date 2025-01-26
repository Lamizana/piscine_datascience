#####################################################################
# Programme Python : First Table [Module data Warehouse 01]         #
# Récupérez automatiquement tous les CSV du dossier customer et     #
# les mettre dans une table 'clients'                               #                             #
#                                                                   #
# Auteur : A.Lamizana, Angouleme, janvier-2025                      #
# -*-coding:Utf-8 -*                                                #
#                                       https://github.com/Lamizana #
#####################################################################
# Importations de fonctions externes :
import os
import sys
import csv
import psycopg2

#####################################################################
# Variables globales
# Configuration de la connexion à PostgreSQL :
DB_CONFIG = {
    "host": "localhost",            # Adresse du serveur PostgreSQL
    "port": 5432,                   # Port PostgreSQL
    "database": "piscineds",        # Nom de votre base de données
    "user": "alamizan",             # Nom de l'utilisateur PostgreSQL
    "password": "mysecretpassword"  # Mot de passe PostgreSQL
}

DB_NAME = "piscineds"

# Définition des types de colonnes
COLUNM_TYPES = {
    "event_time": "TIMESTAMP",
    "event_type": "VARCHAR(50)",
    "product_id": "INTEGER",
    "price": "DECIMAL(10,2)",
    "user_id": "INTEGER",
    "user_session": "VARCHAR(50)"
}

# Chemin vers le fichier CSV et nom de la table :
CSV_PATH = "/home/lamizana/subject/customer2/"
TABLE_NAME = "clients"

#####################################################################
# Definitions locales de fonctions :
def color(texte: str, couleur="37", style="0") -> str:
    """
    Applique une couleur et un style à un texte.
    - couleur : Code couleur de 30 a 47 (ex: '31' pour rouge)
    - style : Style du texte de 0 a 5(ex: '1' pour gras)
    """

    return (f"\033[{style};{couleur}m{texte}\033[0m")


# ---------------------------------------------------------------- #
def connect_postgres(DB_CONFIG, db_name):
    """
    Connexion à la base de données PostgreSQL
    - conn: retourne un objet qui represente la connection active.
    """

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print(color(f"Connexion à la base de données '{db_name}' réussie !\n", 36, 3))
        return (conn)
    except psycopg2.Error as e:
        print(color(f"Erreur lors de la connexion à PostgreSQL : {e}", 31, 3))
        exit(1)


# ---------------------------------------------------------------- #
def csv_is_valid(path: str) -> bool:
    """
    Verifie la validite du fichier csv.
    """

    print(color("\nVerification du fichiers CSV...", 30, 4))
    try:
        with open(path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
    except Exception as e:
        print(color(f"\nErreur lors de la lecture du fichier CSV: {e}\n", 31, 3))
        return False
    
    print(color("\t- Le fichier CSV est lisible.", 32, 3))
    return (True)


# ---------------------------------------------------------------- #
def create_table(table: str, cursor, conn) -> None:
    """
    Permet de creer une table dans la base de donnees 'piscineds'
    - table : nom de la Table.
    - conn : objet connection valide a postgres.
    - cursor : Pour faire des requetes.
    """

    try:
        headers = [col for col in COLUNM_TYPES]
        
        # Création de la table :
        colunms_with_type = ", ".join([f"{col} {COLUNM_TYPES[col]}" for col in headers])
        create_table_query = f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} ({colunms_with_type});"
        cursor.execute(create_table_query)

        # Commit des changements :
        conn.commit()

        print(color(f"- Header :", 33, 4))
        print(color(f"\t- {colunms_with_type}", 33, 2))
        print(color(f"\nTables '{table}' créée avec succès !\n", 36, 1))

    except Exception as e:
        print(color(f"Erreur: {e}", 31, 3))


# ---------------------------------------------------------------- #
def add_data_on_table(table: str, csv_directory: str, cursor, conn) -> None:
    """
    Réunir toutes les tables 'data_202*_***' dans une table.
    - table: nom de la table
    - csv_drectory : chemin du dossier.
    """

    try:
        print(color(f"csv_directory : ", 36, 1), color(CSV_PATH, 33, 4))
        
        # Parcourir tous les fichiers dans le dossier CSV
        for filename in os.listdir(csv_directory):
            if filename.endswith('.csv'):
                # Construire le chemin complet du fichier CSV
                csv_file_path = os.path.join(csv_directory, filename)

                print(color("\n------------------------------------------------------", 36, 1))
                print(color(f"- Fichier '{filename}': ", 32, 1), color(csv_file_path, 32, 4))

                if filename[:8] != "data_202":
                    print(color(f"Erreur: Le fichier doit commencer par 'data_202*_***' ", 31, 3))
                    continue

                if csv_is_valid(csv_file_path) is False:
                    continue
                
                # Lecture du fichier CSV pour détecter les colonnes :
                with open(csv_file_path, 'r') as csv_file:
                    csv_reader = csv.reader(csv_file)
                    headers = next(csv_reader)
                print(color(f"\nHeader :", 33, 4), headers)

                # Validation des colonnes par rapport aux types définis :
                for col in headers:
                    if col not in COLUNM_TYPES:
                        raise ValueError(f"Aucun type défini pour la colonne '{col}'.")

                # Utiliser COPY pour insérer les données directement dans la table
                with open(csv_file_path, 'r') as f:
                    next(f)
                    cursor.copy_from(f, table, sep=',', null='')

                print(color(f"\nAjout des donnees {filename} reussi !", 34, 1))
        
            # Commit des changements :
            conn.commit()
        

    except Exception as e:
        print(color(f"Erreur: {e}", 31, 3))
    else:
        print(color(f"\nAjout de toutes les donnees '{csv_directory}' reussi !", 32, 1))

    
# ---------------------------------------------------------------- #
def main() -> int:
    """
    Fonction programme principal.
    """

    print(color("\n\t---------------------------------------", 35, 1))
    print(color("\tLANCEMENT DU PROGRAMME : First Table !!", 35, 1))
    print(color("\t---------------------------------------", 35, 1), "\n")

    # Connexion à PostgreSQL :
    conn = connect_postgres(DB_CONFIG, DB_NAME)
    cursor = conn.cursor()

    # Creation de la table clients :
    create_table(TABLE_NAME, cursor, conn)

    # Ajout des fichier csv dans la table clients
    add_data_on_table(TABLE_NAME, CSV_PATH, cursor, conn)

    # Fermeture des connexions :
    if cursor:
        cursor.close()
    if conn:
        conn.close()

    print(color("\n\t-------------------------", 35, 1))
    print(color("\tFERMETURE DU PROGRAMME !!", 35, 1))
    print(color("\t-------------------------", 35, 1), "\n")
    return (0)


#####################################################################
"""Programme principal"""
if __name__ == "__main__":
    main()