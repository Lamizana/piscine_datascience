#####################################################################
# Programme Python : Initial data exploration [Module data analyst] #
# Recupere les donnees de purchase dans customers et affiche        #
# differents graphiques>                                            #
#                                                                   #
# Auteur : A.Lamizana, Angouleme, Mai-2025                          #
# -*-coding:Utf-8 -*                                                #
#                                       https://github.com/Lamizana #
#####################################################################
# Importations de fonctions externes
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import psycopg2
import sys

#####################################################################
## VARIABLES GLOBALES
# Configuration de la base de donnees postgreSQL :
DB_CONFIG = {
    "host": "localhost",            # Adresse du serveur PostgreSQL
    "port": 5432,                   # Port PostgreSQL
    "database": "piscineds",        # Nom de votre base de données
    "user": "alamizan",             # Nom de l'utilisateur PostgreSQL
    "password": "mysecretpassword"  # Mot de passe PostgreSQL
}

REQUEST_SQL = f"""
SELECT * FROM customers
    WHERE event_type = 'purchase';
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
def get_request(request: str, db_config: dict) -> pd.DataFrame:
    """
    Exécute une requête SQL sur une base de données PostgreSQL et retourne le résultat sous forme de DataFrame.

    Connexion à la base de données définie dans la variable globale `DB_CONFIG`.
    La fonction exécute la requête SQL passée en argument, extrait les résultats,
    puis les convertit en un pandas.DataFrame avec les noms de colonnes correspondants.

    Affiche un message de succès en cas de connexion, ou une erreur formatée en cas d'échec.
    Termine l'exécution du programme (`sys.exit(1)`) en cas d'exception.

    Args:
        request (str): Requête SQL à exécuter (par exemple, un SELECT).

    Returns:
        pd.DataFrame: Résultat de la requête SQL sous forme de DataFrame pandas.

    Raises:
        Affiche l’erreur rencontrée à l'exécution (ex: erreur de connexion, erreur SQL),
        puis quitte le programme avec `sys.exit(1)`.

    Example:
        >>> df = get_request("SELECT * FROM customers LIMIT 10;")
        >>> print(df.head())

    Note:
        - Nécessite que la variable globale `DB_CONFIG` soit correctement définie.
        - Utilise la bibliothèque `psycopg2` pour la connexion PostgreSQL.
    """

    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        print(color(f"- Connexion Postgres DB {db_config['database']} reussi", 33, 3))

        # Envoi la requete et recupere les donnees :
        cursor.execute(request)

        # Extrait valeurs et les noms des colonnes depuis le curseur :
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        df = pd.DataFrame(rows, columns=columns)

    except Exception as e:
        print(color(f"Erreur: {e}", 31, 3))
        sys.exit(1)
    finally:
        conn.close()
        cursor.close()
    return (df)


# ---------------------------------------------------------------- #
def graphiq_df(df: pd.DataFrame) -> None:

    print(df.head())

    format_data = "%d/%m/%y %H:%M:%S.%f"



    date = datetime.strptime("24/10/01 00:05:16.12", format_data)


    labels = df["event_time"]
    data = [value for value in labels.tolist() if value < date]

    print("DATE: ", date)
    print("\nDATA: ", data)

    print("Event :", labels)
    # print("Valeurs :", df_values)

    
    plt.plot(df["event_time"], df["price"])
    plt.show()

# ---------------------------------------------------------------- #
def main() -> int:
    """
    Fonction programme principal.
    """

    print(color("\n\t--------------------------------------------------", 35, 1))
    print(color("\t LANCEMENT DU PROGRAMME Initial data exploration!!", 35, 1))
    print(color("\t--------------------------------------------------", 35, 1), "\n")

    df_data = get_request(REQUEST_SQL, DB_CONFIG)
    graphiq_df(df_data)

    print(color("\n\t-------------------------", 35, 1))
    print(color("\tFERMETURE DU PROGRAMME !!", 35, 1))
    print(color("\t-------------------------", 35, 1), "\n")
    return (0)


#####################################################################
# Programme principal
if __name__ == "__main__":
    main()
