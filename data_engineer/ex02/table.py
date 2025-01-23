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

#####################################################################
# Variables globales
# Configuration de la connexion à PostgreSQL :
DB_CONFIG = {
    "host": "localhost",            # Adresse du serveur PostgreSQL
    "port": 5432,                   # Port PostgreSQL
    "database": "piscineds",        # Nom de votre base de données
    "user": "postgres",             # Nom de l'utilisateur PostgreSQL
    "password": "Lamizana@1987"     # Mot de passe PostgreSQL
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

# Utilisateur qui aura tout les droits :
TARGET_USER = 'alamizan'

# Chemin vers le fichier CSV et nom de la table :
CSV_PATH = "/home/lamizana/subject/customer2/toto.csv"
TABLE_NAME = "data_2022_dec"

#####################################################################
# Definitions locales de fonctions
def color(texte, couleur="37", style="0") -> str:
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
            raise Exception ("Le programme doit prendre le chemin du fichier.")
        with open(sys.argv[1], 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
    except Exception as e:
        print(color(f"\nErreur lors de la lecture du fichier CSV: {e}\n", 31, 3))
        return False
    
    print(color("\t- Le fichier CSV est lisible.", 32, 3))
    return (True)


# ---------------------------------------------------------------- #
def create_table(csv_path: str) -> bool:
    """
    Permet de creer une table dans la base de donnees 'piscineds' a partir
    d'un fichier CSV :
    - csv_path : chemin du fichiers.
    - table : nom de la Table.
    """

    table_name = sys.argv[1].split("/")
    table_name = str(table_name[-1][:-4])
    print(color(f"\nCreation de la Table '{table_name}':", 33, 4))
    print(color(f"\t- Emplacement: {csv_path}...", 33, 3))


    return (True)


# ---------------------------------------------------------------- #
def main() -> int:
    """
    Fonction programme principal.
    """

    print(color("\n\t-------------------------", 32, 1))
    print(color("\tLANCEMENT DU PROGRAMME !!", 32, 1))
    print(color("\t-------------------------", 32, 1), "\n")

    # ------------------------------------------------------- #
    if csv_is_valid() is False:
        return(1)

    # ------------------------------------------------------- #
    if create_table(sys.argv[1]) is False:
        return(1)
    
    print(color("\n\t-------------------------", 32, 1))
    print(color("\tFERMETURE DU PROGRAMME !!", 32, 1))
    print(color("\t-------------------------", 32, 1), "\n")
    return (0)


#####################################################################
"""Programme principal"""
if __name__ == "__main__":
    main()