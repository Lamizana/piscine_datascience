#####################################################################
# Programme Python : First Table [Module data engineer]             #
# Créer une table postgres en utilisant les données d'un CSV        #
#                                                                   #
# Auteur : A.Lamizana, Angouleme, janvier-2025                      #
# -*-coding:Utf-8 -*                                                #
#                                       https://github.com/Lamizana #
#####################################################################
# Importations de fonctions externes
import sys
import csv
import psycopg2
import os

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
CSV_PATH = "/home/lamizana/subject/customer/data_2022_dec.csv"
TABLE_NAME = "data_2022_dec"


#####################################################################
# Definitions locales de fonctions
def color(texte: str, couleur="37", style="0") -> str:
    """
    Applique une couleur et un style à un texte.
    - couleur : Code couleur de 30 a 47 (ex: '31' pour rouge)
    - style : Style du texte de 0 a 5(ex: '1' pour gras)
    """

    return f"\033[{style};{couleur}m{texte}\033[0m"


# ---------------------------------------------------------------- #
def csv_is_valid() -> bool:
    """
    Verifie la validite du fichier csv.
    """

    print(color("Verification du fichiers CSV...", 33, 4))
    try:
        if len(sys.argv) != 2:
            raise ValueError("2 args necessaires, le programme et le chemin du fichier")
        if not os.path.exists(sys.argv[1]):
            raise Exception("Le fichier ne peut etre lue.")
    except Exception as e:
        print(color(f"\nErreur lors de la lecture du fichier CSV: {e}\n", 31, 3))
        return False

    print(color("\t- Le fichier CSV est lisible.", 32, 3))
    return (True)


# ---------------------------------------------------------------- #
def create_table(csv_path: str, table: str) -> None:
    """
    Permet de creer une table dans la base de donnees 'piscineds' a partir
    d'un fichier CSV :
    - csv_path : chemin du fichiers.
    - table : nom de la Table.
    """

    try:
        # Connexion à PostgreSQL :
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print(color("\t- Connexion Postgres reussi", 33, 3))

        # Lecture du fichier CSV pour détecter les colonnes :
        with open(csv_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            headers = next(csv_reader)
        print(color("\nHeader :", 33, 4), headers)

        # Validation des colonnes par rapport aux types définis :
        for col in headers:
            if col not in COLUNM_TYPES:
                raise ValueError(f"Aucun type défini pour la colonne '{col}'.")

        # Création de la table :
        colunms_with_type = ", ".join([f"{col} {COLUNM_TYPES[col]}" for col in headers])
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table} ({colunms_with_type});"
        cursor.execute(create_table_query)

        # Utiliser COPY pour insérer les données directement dans la table
        with open(csv_path, 'r') as f:
            next(f)
            cursor.copy_from(f, table, sep=',', null='')

        # Validation des modifications
        conn.commit()

    except Exception as e:
        print(color(f"Erreur: {e}", 31, 3))
    else:
        print(color(f"\nTable {table} créée avec succès !", 32, 1))
    finally:
        # Fermeture des connexions :
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# ---------------------------------------------------------------- #
def main() -> int:
    """
    Fonction programme principal.
    """

    print(color("\n\t-------------------------", 35, 1))
    print(color("\tLANCEMENT DU PROGRAMME !!", 35, 1))
    print(color("\t-------------------------", 35, 1), "\n")

    if csv_is_valid() is False:
        return (1)

    table_name = sys.argv[1].split("/")
    table_name = str(table_name[-1][:-4])
    print(color(f"\nCreation de la Table '{table_name}':", 33, 4))
    print(color(f"\t- Emplacement: {sys.argv[1]}...", 33, 3))

    create_table(sys.argv[1], table_name)

    print(color("\n\t-------------------------", 35, 1))
    print(color("\tFERMETURE DU PROGRAMME !!", 35, 1))
    print(color("\t-------------------------", 35, 1), "\n")
    return (0)


#####################################################################
# Programme principal
if __name__ == "__main__":
    main()
