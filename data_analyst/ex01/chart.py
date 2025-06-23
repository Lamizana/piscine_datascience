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
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import pandas as pd
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
        print(color(f"- Connexion Postgres DB {db_config['database']} reussi...", 33, 3))

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
def df_sorted(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filtre et agrège les données pour compter le nombre de clients uniques par jour
    dans une plage de dates spécifiée (du 1er octobre au 1er février inclus).

    Args:
        df (pd.DataFrame): DataFrame contenant au moins les colonnes
            'event_time' (dates au format texte ou datetime) et 'user_id'.

    Returns:
        pd.DataFrame: DataFrame avec deux colonnes :
            - 'day' (datetime.date) : date sans heure
            - 'nb_customers' (int) : nombre de clients uniques ce jour-là

    Comportement :
        - Convertit 'event_time' en datetime si nécessaire.
        - Filtre les événements entre le 1er octobre 2022 et le 1er février 2023.
        - Regroupe par jour et calcule le nombre d'utilisateurs uniques par jour.
    """

    # 1. Convertir la colonne 'event_time' en datetime
    df['event_time'] = pd.to_datetime(df['event_time'])

    # 2. Extraire la date (sans l'heure)
    df['day'] = df['event_time'].dt.date

    # 3. Filtrer entre le 1er octobre et le 28/29 février :
    start_date = pd.to_datetime('2022-10-01')
    end_date = pd.to_datetime('2023-02-28') 

    df_filtered = df[(df['event_time'] >= start_date) & (df['event_time'] <= end_date)]

    # 4. Grouper par jour et compter les clients uniques
    daily_unique_customers = df_filtered.groupby(df_filtered['event_time'].dt.date)['user_id'].nunique().reset_index()
    daily_unique_customers.columns = ['day', 'nb_customers']

    return (daily_unique_customers)


# ---------------------------------------------------------------- #
def graphiq_line(daily_unique_customers: pd.DataFrame) -> None:
    """
    Affiche un graphique en ligne du nombre de clients uniques par jour sur une période donnée.

    Args:
        daily_unique_customers (pd.DataFrame): DataFrame contenant deux colonnes :
            - 'day' (datetime.date) : dates des observations
            - 'nb_customers' (int) : nombre de clients uniques pour chaque date

    Comportement :
        - Trace une courbe avec une ligne continue représentant le nombre de clients uniques par jour.
        - L'axe des x est limité entre le 1er octobre 2022 et le 28 février 2023.
        - Le graphique est personnalisé avec titre, labels, rotation des dates et grille.
        - Gère l'interruption clavier (Ctrl + C) pour afficher un message d'arrêt propre.

    Returns:
        None: affiche uniquement le graphique.
    """

    try:
        plt.figure(figsize=(8, 6))
        plt.plot(daily_unique_customers['day'],
                 daily_unique_customers['nb_customers'],
                 linestyle='-')
        # Fixer la limite de l'axe des x (dates)
        plt.xlim(pd.to_datetime('2022-10-01'), pd.to_datetime('2023-02-28'))

        # Formatage de l'axe X pour afficher les mois (ex: Oct 2022)
        ax = plt.gca()
        ax.xaxis.set_major_locator(mdates.MonthLocator())  # un tick par mois
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))  # format 'Oct 2022'

        plt.title('Nombre de clients uniques par mois')
        plt.xlabel('Month')
        plt.ylabel('Numbers of customers')
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    except KeyboardInterrupt as e:
        print(color(f"\n⛔ Affichage interrompu par l'utilisateur (Ctrl + C)", 31, 3))


# ---------------------------------------------------------------- #
def ventes_totales_par_mois(df: pd.DataFrame) -> None:
    """
    Affiche un graphique en barres représentant les ventes mensuelles totales 
    (en millions d'Altariens) entre octobre 2022 et février 2023.

    - Convertit les dates
    - Filtre les données sur la période donnée
    - Convertit les prix en float, puis en Altariens
    - Agrège les ventes par mois
    - Affiche un graphique lisible et correctement étiqueté

    :param df: DataFrame contenant une colonne 'event_time' (datetime) et 'price' (float ou Decimal)
    """

    try:
        # 1. Conversion des dates
        df['event_time'] = pd.to_datetime(df['event_time'])

        # 2. Filtrage sur la période souhaitée
        start_date = pd.to_datetime('2022-10-01')
        end_date = pd.to_datetime('2023-02-28')
        df_filtered = df[(df['event_time'] >= start_date) & (df['event_time'] <= end_date)].copy()

        # 3. Conversion en float si nécessaire
        df_filtered['price'] = df_filtered['price'].astype(float)

        # 4. Extraire année + mois pour regrouper
        df_filtered['year_month'] = df_filtered['event_time'].dt.to_period('M').dt.to_timestamp()

        # 5. Regrouper par mois et sommer les ventes
        monthly_sales = df_filtered.groupby('year_month')['price'].sum()

        # 6. Convertir les ventes en millions d'Altariens (1€ = 0.8🪙)
        monthly_sales_million_altarien = (monthly_sales * 0.8) / 1_000_000

        # 7. Tracer
        plt.figure(figsize=(10, 6))
        plt.bar(monthly_sales_million_altarien.index,
                monthly_sales_million_altarien.values,
                color='steelblue', width=20)

        ax = plt.gca()
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%B %Y'))

        plt.xlabel("Month")
        plt.ylabel("Total sales in million Altariens")
        plt.grid(axis='y')
        plt.tight_layout()
        plt.show()

    except KeyboardInterrupt:
        print("\n⛔ Affichage interrompu par l'utilisateur (Ctrl + C)")

    except Exception as e:
        print(f"\n❌ Erreur lors de l'affichage : {e}")


import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

def plot_avg_customer_spending_altarien(df: pd.DataFrame) -> None:
    """
    Affiche un graphique en ligne des dépenses moyennes par client
    (en Altariens) par jour entre octobre 2022 et février 2023.

    :param df: DataFrame avec colonnes 'event_time', 'price' et 'user_id'
    """
    
    try:
        # 1. Convertir 'event_time' en datetime
        df['event_time'] = pd.to_datetime(df['event_time'])

        # 2. Filtrer la période
        start_date = pd.to_datetime('2022-10-01')
        end_date = pd.to_datetime('2023-02-28')
        df_filtered = df[(df['event_time'] >= start_date) & (df['event_time'] <= end_date)].copy()

        # 3. Convertir 'price' en float
        df_filtered['price'] = df_filtered['price'].astype(float)

        # 4. Conversion en Altariens (1€ = 0.8🪙)
        df_filtered['price_altarien'] = df_filtered['price'] * 0.8

        # 5. Grouper par jour
        df_filtered['day'] = df_filtered['event_time'].dt.date
        daily_total = df_filtered.groupby('day')['price_altarien'].sum()
        daily_customers = df_filtered.groupby('day')['user_id'].nunique()

        # 6. Moyenne journalière
        daily_avg = (daily_total / daily_customers).reset_index()
        daily_avg.columns = ['day', 'avg_spending']

        # 7. Tracer le graphique
        plt.figure(figsize=(8, 6))
        plt.plot(pd.to_datetime(daily_avg['day']),
                 daily_avg['avg_spending'],
                 linestyle='-', color='deepskyblue', linewidth=2)
        plt.fill_between(pd.to_datetime(daily_avg['day']),
                         daily_avg['avg_spending'], color='deepskyblue', alpha=0.3)

        plt.xlabel("Month")
        plt.ylabel("Average spend/customers in A")
        plt.grid(True)
        plt.xlim(start_date, end_date)
        plt.ylim(0, 45)
        plt.yticks(range(0, 46, 5))

        ax = plt.gca()
        ax.xaxis.set_major_locator(mdates.MonthLocator())        # ticks au début de chaque mois
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b')) # format abrégé (Oct, Nov, ...)

        plt.tight_layout()
        plt.show()

    except KeyboardInterrupt:
        print("\n⛔ Affichage interrompu par l'utilisateur.")
    except Exception as e:
        print(f"\n❌ Erreur : {e}")


# ---------------------------------------------------------------- #
def main() -> int:
    """
    Fonction programme principal.
    """

    print(color("\n\t-------------------------------------------------", 35, 1))
    print(color("\t LANCEMENT DU PROGRAMME Initial data exploration!!", 35, 1))
    print(color("\t-------------------------------------------------", 35, 1), "\n")

    df_data = get_request(REQUEST_SQL, DB_CONFIG)

    # df = df_sorted(df_data)
    # graphiq_line(df)

    # ventes_totales_par_mois(df_data)
    plot_avg_customer_spending_altarien(df_data)



    print(color("\n\t-------------------------", 35, 1))
    print(color("\tFERMETURE DU PROGRAMME !!", 35, 1))
    print(color("\t-------------------------", 35, 1), "\n")
    return (0)


#####################################################################
# Programme principal
if __name__ == "__main__":
    main()
