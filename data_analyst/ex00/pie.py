#####################################################################
# Programme Python : American apple Pie [Module data analyst]       #
# Recupere les events de la table customers dans la base de         #
# donnees picsineds et les affiches sous la forme d'un              #
# diagramme circulaire.                                             #
#                                                                   #
# Auteur : A.Lamizana, Angouleme, Mai-2025                          #
# -*-coding:Utf-8 -*                                                #
#                                       https://github.com/Lamizana #
#####################################################################
# Importations de fonctions externes
import pandas as pd
import psycopg2
import sys
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


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
SELECT event_type, COUNT(*) AS TOTAL 
FROM customers 
GROUP BY event_type;
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
def get_request(request: str, db_config) -> pd.DataFrame:
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
def df_sorted(df_data: pd.DataFrame) -> pd.DataFrame:
    """
    Trie un DataFrame selon un ordre personnalisé de la colonne 'event_type'.

    Cette fonction convertit la colonne `event_type` en type catégoriel
    avec un ordre défini : ["view", "cart", "remove_from_cart", "purchase"].
    Elle trie ensuite les lignes du DataFrame selon cet ordre.

    Args:
        df_data (pd.DataFrame): 
            Le DataFrame contenant une colonne `event_type` à trier.

    Returns:
        pd.DataFrame: 
            Le DataFrame trié avec `event_type` comme catégorie ordonnée.
    """

    custom_order = ["view", "cart", "remove_from_cart", "purchase"]

    df_data["event_type"] = pd.Categorical(df_data["event_type"], categories=custom_order, ordered=True)
    df_data = df_data.sort_values("event_type")
    return (df_data)


# ---------------------------------------------------------------- #
def diagram_df(df_data: pd.DataFrame) -> None:
    """
    Affiche un diagramme circulaire à partir des données d'un DataFrame.

    Cette fonction génère un camembert (`pie chart`) représentant la répartition 
    des événements en fonction des types d'événements (`event_type`) et de leur 
    quantité (`total`). Elle capture également les interruptions clavier (`Ctrl + C`) 
    pour éviter les erreurs à l'affichage.

    Args:
        df_data (pd.DataFrame): 
            Un DataFrame contenant au minimum deux colonnes :
                - "event_type" : les catégories à afficher (étiquettes),
                - "total" : les valeurs numériques associées à chaque type.

    Raises:
        KeyboardInterrupt:
            Si l'utilisateur interrompt l'affichage du graphique avec Ctrl + C.
    """

    labels = df_data["event_type"]
    values = df_data["total"]

    try:
        plt.figure(figsize=(6, 6))
        plt.pie(values,
            labels=labels,
            autopct='%1.1f%%',
            startangle=0,
            wedgeprops={'edgecolor': 'white', 'linewidth': 1})
        plt.axis('equal')
        plt.show()
    except KeyboardInterrupt as e:
        print(color(f"\n⛔ Affichage interrompu par l'utilisateur (Ctrl + C)", 31, 3))


# ---------------------------------------------------------------- #
def main() -> int:
    """
    Fonction programme principal.
    """

    print(color("\n\t---------------------------------------------", 35, 1))
    print(color("\t LANCEMENT DU PROGRAMME American apple Pie!!", 35, 1))
    print(color("\t---------------------------------------------", 35, 1), "\n")

    df_data = get_request(REQUEST_SQL, DB_CONFIG)
    df_data = df_sorted(df_data)
    diagram_df(df_data) 

    print(color("\n\t-------------------------", 35, 1))
    print(color("\tFERMETURE DU PROGRAMME !!", 35, 1))
    print(color("\t-------------------------", 35, 1), "\n")
    return (0)


#####################################################################
# Programme principal
if __name__ == "__main__":
    main()
