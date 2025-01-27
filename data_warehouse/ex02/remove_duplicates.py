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
COLUNM = [
    "event_time",
    "event_type",
    "product_id",
    "price",
    "user_id",
    "user_session"
]

TABLE_NAME = "customers"

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
    Connexion à la base de données PostgreSQL
    - conn: retourne un objet qui represente la connection active.
    """

    try:
        conn = psycopg2.connect(**db_config)
        print(color(f"Connexion à la base de données '{db_name}' réussie !\n", 36, 3))
        return (conn)
    except psycopg2.Error as e:
        print(color(f"Erreur lors de la connexion à PostgreSQL : {e}", 31, 3))
        exit(1)


# ---------------------------------------------------------------- #
def remove_doublon(conn, cursor) -> None:
    """
    Supprime tous les doublons.
    """

    colunms_str = ", ".join([f"{col}" for col in COLUNM])
    print("Verification des colonnes: ", colunms_str)

    str_1 = f"DELETE FROM {TABLE_NAME} WHERE ctid NOT IN (SELECT MIN(ctid) "
    str_2 = f"FROM {TABLE_NAME} GROUP BY {colunms_str});"
    
    rm_doublon = str_1 + str_2
    print("\nScript a executer:", rm_doublon)

    cursor.execute(rm_doublon)

    # Validation des modifications
    conn.commit()

    print(color(f"\nDoublons supprimee avec succès dans la Table '{TABLE_NAME}' !", 32, 1))


# ---------------------------------------------------------------- #
def main() -> int:
    """
    Fonction programme principal.
    """

    print(color("\n\t-------------------------", 35, 1))
    print(color("\tLANCEMENT DU PROGRAMME !!", 35, 1))
    print(color("\t-------------------------", 35, 1), "\n")

    # Connexion à PostgreSQL :
    conn = connect_postgres(DB_CONFIG, DB_NAME)
    cursor = conn.cursor()

    # Suppression des doublons :
    remove_doublon(conn, cursor)

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
# Programme principal
if __name__ == "__main__":
    main()