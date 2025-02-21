#####################################################################
# Programme Python : Fusion [Module data Warehouse 03]              #
# Combine les tables 'customers' et 'items' de la table customers.  #
#                                                                   #
# Auteur : A.Lamizana, Angouleme, janvier-2025                      #
# -*-coding:Utf-8 -*                                                #
#                                       https://github.com/Lamizana #
#####################################################################
# Importations de fonctions externes :
import psycopg2
from psycopg2 import errors, sql

#####################################################################
# Variables globales :
# Configuration de la connexion à PostgreSQL :
DB_NAME = "piscineds"
DB_CONFIG = {
    "host": "localhost",            # Adresse du serveur PostgreSQL
    "port": 5432,                   # Port PostgreSQL
    "database": DB_NAME,        # Nom de votre base de données
    "user": "alamizan",             # Nom de l'utilisateur PostgreSQL
    "password": "mysecretpassword"  # Mot de passe PostgreSQL
}

TABLE_NAME = "customers"

ITEM_TMP = """
CREATE TABLE items_tmp AS
SELECT
    product_id,
    COALESCE(MAX(category_id), NULL) AS category_id,
    COALESCE(MAX(category_code), NULL) AS category_code,
    COALESCE(MAX(brand), NULL) AS brand
FROM
    items
GROUP BY
    product_id;
"""

# script psql: Ajout de nouvelle colonne :
ALTER_TABLE = f"""
ALTER TABLE {TABLE_NAME}
ADD COLUMN category_id INT8,
ADD COLUMN category_code TEXT,
ADD COLUMN brand VARCHAR(255);
"""

# script psql: Fusion de deux tables par rapport a product_id :
UPDATE = f"""
UPDATE {TABLE_NAME} c
SET
    category_id = i.category_id,
    category_code = i.category_code,
    brand = i.brand
FROM items_tmp i
WHERE c.product_id = i.product_id;
"""

CLEAN = f"""
DROP TABLE items_tmp;
"""

#####################################################################
# Definitions locales de fonctions :
def color(texte: str, couleur="37", style="0") -> str:
    """
    Applique une couleur et un style à un texte.
    - couleur : Code couleur de 30 a 47 (ex: '31' pour rouge).
    - style : Style du texte de 0 a 5(ex: '1' pour gras).
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
        print(color(f"La table '{TABLE_NAME}' contient des données. Poursuite de l'exécution.\n", 36, 3))
        return (connection)

    except errors.UndefinedTable:
        print(color(f"Erreur : La table '{TABLE_NAME}' n'existe pas. Fin de l'exécution.", 31, 3))
        exit(1)
    except psycopg2.Error as e:
        print(color(f"Erreur lors de la connexion ou de l'exécution SQL : {e}", 31, 3))
        exit(1)

# ---------------------------------------------------------------- #
def join_table(conn, cursor) -> None:
    """
    Fusion des tables customers et items.
    """

    try:
        # Execute les requetes :
        print("Exécution de la requête SQL...")
        print("- Script a executer:", color(ITEM_TMP, 33, 3))
        cursor.execute(ITEM_TMP)

        print("- Script a executer:", color(ALTER_TABLE, 33, 3))
        cursor.execute(ALTER_TABLE)

        print("- Script a executer:", color(UPDATE, 33, 3))
        cursor.execute(UPDATE)

        print("- Script a executer:", color(CLEAN, 33, 3))
        cursor.execute(CLEAN)

        conn.commit()
        print("Requête exécutée avec succès !")

    except Exception as e:
        print(color(f"Erreur lors de la fusion des tables: {e}", 31, 3))


# ---------------------------------------------------------------- #
def main() -> int:
    """
    Fonction programme principal.
    """

    print(color("\n\t-------------------------------", 35, 1))
    print(color("\tLANCEMENT DU PROGRAMME Fusion!!", 35, 1))
    print(color("\t-------------------------------", 35, 1), "\n")

    # Connexion à PostgreSQL :
    conn = connect_postgres(DB_CONFIG, DB_NAME)
    cursor = conn.cursor()

    join_table(conn, cursor)

    # Fermeture des connexions :
    cursor.close()
    conn.close()

    print(color("\n\t-------------------------", 35, 1))
    print(color("\tFERMETURE DU PROGRAMME !!", 35, 1))
    print(color("\t-------------------------", 35, 1), "\n")
    return (0)


#####################################################################
# Programme principal :
if __name__ == "__main__":
    main()
