#####################################################################
# Programme Python : Automatic table [Module data engineer 03]      #
# Récupérez automatiquement tous les CSV du dossier customer et     #
# nommez les tableaux selon le nom du CSV, mais sans l'extension    #
# fichier.                                                          #
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

# Définition des types de colonnes
COLUNM_TYPES = {
    "event_time": "TIMESTAMP",
    "event_type": "VARCHAR(50)",
    "product_id": "INTEGER",
    "price": "DECIMAL(10,2)",
    "user_id": "INTEGER",
    "user_session": "VARCHAR(50)"
}

CSV_PATH = "/home/lamizana/subject/customer"


#####################################################################
# Definitions locales de fonctions :
def color(texte: str, couleur="37", style="0") -> str:
    """
    Applique une couleur et un style à un texte.
    - couleur : Code couleur de 30 a 47 (ex: '31' pour rouge)
    - style : Style du texte de 0 a 5(ex: '1' pour gras)
    """

    return f"\033[{style};{couleur}m{texte}\033[0m"


# ---------------------------------------------------------------- #
def csv_is_valid(path: str) -> bool:
    """
    Verifie la validite du fichier csv.
    """

    print(color("\nVerification du fichiers CSV...", 30, 4))
    try:
        if not os.path.exists(sys.argv[1]):
            raise Exception("Le fichier ne peut etre lue.")
    except Exception as e:
        print(color(f"\nErreur lors de la lecture du fichier CSV: {e}\n", 31, 3))
        return False

    print(color("\t- Le fichier CSV est lisible.", 32, 3))
    return (True)


# ---------------------------------------------------------------- #
def create_table(csv_path: str, table: str, cursor) -> None:
    """
    Permet de creer une table dans la base de donnees 'piscineds' a partir
    d'un fichier CSV :
    - csv_path : chemin du fichiers.
    - table : nom de la Table.
    """

    try:
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

        print(color(f"\n- Table '{table}' créé !", 32, 3))

    except Exception as e:
        print(color(f"Erreur: {e}", 31, 3))


# ---------------------------------------------------------------- #
def automatic_table() -> None:
    """
    Creer toutes les tables dans la base de donnees 'piscineds' a partir
    d'un dossier:
    - csv_directory : chemin du dossier.
    """

    try:
        # Connexion à PostgreSQL :
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print(color("- Connexion Postgres reussi", 36, 3))

        csv_directory = sys.argv[1]
        print(color("csv_directory : ", 36, 1), color(csv_directory, 33, 4))

        # Parcourir tous les fichiers dans le dossier CSV
        for filename in os.listdir(csv_directory):
            if filename.endswith('.csv'):
                # Construire le chemin complet du fichier CSV
                csv_file_path = os.path.join(csv_directory, filename)

                # Nom de la table basé sur le nom du fichier CSV :
                table = os.path.splitext(filename)[0]  # Enlever l'extension .csv
                print(color("\n------------------------------------------------------", 33, 1))
                print(color(f"- Table '{table}': ", 32, 1), color(csv_file_path, 32, 4))

                if csv_is_valid(csv_file_path) is False:
                    continue

                create_table(csv_file_path, table, cursor)

                # Commit des changements :
                conn.commit()

    except Exception as e:
        print(color(f"Erreur: {e}", 31, 3))
    else:
        print(color("\nTables créée avec succès !", 32, 1))
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

    if len(sys.argv) != 2:
        print(color("Erreur: 2 args necessaires, le programme et le chemin du dossier.", 31, 3))
        exit(1)

    automatic_table()

    print(color("\n\t-------------------------", 35, 1))
    print(color("\tFERMETURE DU PROGRAMME !!", 35, 1))
    print(color("\t-------------------------", 35, 1), "\n")
    return (0)


#####################################################################
"""Programme principal"""
if __name__ == "__main__":
    main()
