#####################################################################
# Programme Python : First Table [Module data Warehouse 01]         #
# Récupérez automatiquement tous les CSV du dossier customer et     #
# les mettre dans une table 'customers'                              #
#                                                                   #
# Auteur : A.Lamizana, Angouleme, janvier-2025                      #
# -*-coding:Utf-8 -*                                                #
#                                       https://github.com/Lamizana #
#####################################################################
# Importations de fonctions externes :
import psycopg2

#####################################################################
# Variables globales
# Configuration de la connexion à PostgreSQL :
DB_NAME = "piscineds"
DB_CONFIG = {
    "host": "localhost",            # Adresse du serveur PostgreSQL
    "port": 5432,                   # Port PostgreSQL
    "database": DB_NAME,        # Nom de votre base de données
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

TABLE_NAME = "customers"

ADD_TABLE = f"""
INSERT INTO {TABLE_NAME}
SELECT * FROM data_2022_oct
UNION ALL
SELECT * FROM data_2022_nov
UNION ALL
SELECT * FROM data_2022_dec
UNION ALL
SELECT * FROM data_2023_jan
UNION ALL
SELECT * FROM data_2023_feb;
"""


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
def create_table(table: str, cursor, conn) -> None:
    """
    Permet de creer une table dans la base de donnees 'piscineds'
    - table : nom de la Table.
    - conn : objet connection valide a postgres.
    - cursor : Pour faire des requetes.
    """

    headers = [col for col in COLUNM_TYPES]
        
    # Création de la table :
    colunms_with_type = ", ".join([f"{col} {COLUNM_TYPES[col]}" for col in headers])
    create_table_query = f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} ({colunms_with_type});"
    cursor.execute(create_table_query)
    conn.commit()

    print(color(f"- Header :", 33, 4))
    print(color(f"\t- {colunms_with_type}", 33, 2))
    print(color(f"\nTables '{table}' créée avec succès !\n", 36, 1))
        


# ---------------------------------------------------------------- #
def main() -> int:
    """
    Fonction programme principal.
    """

    print(color("\n\t-------------------------------------", 35, 1))
    print(color("\tLANCEMENT DU PROGRAMME : Customers !!", 35, 1))
    print(color("\t-------------------------------------", 35, 1), "\n")

    # Connexion à PostgreSQL :
    conn = connect_postgres(DB_CONFIG, DB_NAME)
    cursor = conn.cursor()

    try:
        # Creation de la table clients :
        create_table(TABLE_NAME, cursor, conn)

        # Ajout des tables dans la table customers :
        print("- Script psql:", color(ADD_TABLE, 33, 3))
        cursor.execute(ADD_TABLE)
        conn.commit()

    except Exception as e:
        print(color(f"Erreur: {e}", 31, 3))
    finally:
        cursor.close()
        conn.close()

    print(color("\n\t-------------------------", 35, 1))
    print(color("\tFERMETURE DU PROGRAMME !!", 35, 1))
    print(color("\t-------------------------", 35, 1), "\n")
    return (0)


#####################################################################
# Programme principal
if __name__ == "__main__":
    main()
