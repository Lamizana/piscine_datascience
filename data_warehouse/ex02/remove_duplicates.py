#####################################################################
# Programme Python : Remove_duplicate [Module data Warehouse 02]    #
# Supprimer les lignes en double dans la table "customers".         #
#                                                                   #
# Auteur : A.Lamizana, Angouleme, janvier-2025                      #
# -*-coding:Utf-8 -*                                                #
#                                       https://github.com/Lamizana #
#####################################################################
# Importations de fonctions externes :
import psycopg2
from psycopg2 import errors, sql

#####################################################################
# Variables globales
# Configuration de la connexion à PostgreSQL :
DB_NAME = "piscineds"
DB_CONFIG = {
    "host": "localhost",            # Adresse du serveur PostgreSQL
    "port": 5432,                   # Port PostgreSQL
    "database": DB_NAME,            # Nom de votre base de données
    "user": "alamizan",             # Nom de l'utilisateur PostgreSQL
    "password": "mysecretpassword"  # Mot de passe PostgreSQL
}

TABLE_NAME = "customers"

DOUBLON = f"""
WITH close_duplicates AS (
    SELECT ctid
    FROM (
        SELECT ctid,
               event_time,
               LAG(event_time) OVER (
                   PARTITION BY event_type, product_id, price, user_id, user_session
                   ORDER BY event_time
               ) AS previous_time
        FROM {TABLE_NAME}
    ) subquery
    WHERE event_time - previous_time <= INTERVAL '1 second'
)
DELETE FROM {TABLE_NAME} WHERE ctid IN (SELECT ctid FROM close_duplicates);
"""


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
def connect_postgres(db_config: set, db_name: str):
    """
    Connexion à la base de données PostgreSQL et verification de la 
    table 'customers'
    - conn: retourne un objet qui represente la connection active.
    """

    try:
        # Connexion à la base de données :
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()

        # Vérification si la table 'customers' existe et contient des données :
        query = sql.SQL(f"SELECT 1 FROM {TABLE_NAME} LIMIT 1")
        cursor.execute(query)
        result = cursor.fetchone()  # Récupère la première ligne

        if result is None:
            print(color(f"La table '{TABLE_NAME}' est vide. Fin de l'exécution."))
            exit(1)

        print(color(f"Connexion à la base de données '{db_name}' réussie !", 36, 3))
        print(color(f"La table '{TABLE_NAME}' contient des données. Poursuite de l'exécution.", 36, 3))
        return (connection)

    except errors.UndefinedTable:
        print(color(f"Erreur : La table '{TABLE_NAME}' n'existe pas. Fin de l'exécution.", 31, 3))
        exit(1)
    except psycopg2.Error as e:
        print(color(f"Erreur lors de la connexion ou de l'exécution SQL : {e}", 31, 3))
        exit(1)


# ---------------------------------------------------------------- #
def main() -> int:
    """
    Fonction programme principal.
    """

    print(color("\n\t----------------------------------", 35, 1))
    print(color("\tLANCEMENT DU PROGRAMME : Remove !!", 35, 1))
    print(color("\t----------------------------------", 35, 1), "\n")

    try:
        conn = connect_postgres(DB_CONFIG, DB_NAME)
        cursor = conn.cursor()

        print("- Script a executer:", color(DOUBLON, 33, 3))
        cursor.execute(DOUBLON)
        conn.commit()
        print(color(f"\nDoublons supprimee avec succès dans '{TABLE_NAME}' !", 32, 1))

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
