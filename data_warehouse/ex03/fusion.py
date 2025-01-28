#####################################################################
# Programme Python : Fusion [Module data Warehouse 03]              #
# Combine les tables 'customers' et 'items' de la table customers.  #
#                                                                   #
# Auteur : A.Lamizana, Angouleme, janvier-2025                      #
# -*-coding:Utf-8 -*                                                #
#                                       https://github.com/Lamizana #
#####################################################################
# Importations de fonctions externes :


#####################################################################
# Variables globales :



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
def main() -> int:
    """
    Fonction programme principal.
    """

    print(color("\n\t-------------------------------", 35, 1))
    print(color("\tLANCEMENT DU PROGRAMME Fusion!!", 35, 1))
    print(color("\t-------------------------------", 35, 1), "\n")

    print(color("\n\t-------------------------", 35, 1))
    print(color("\tFERMETURE DU PROGRAMME !!", 35, 1))
    print(color("\t-------------------------", 35, 1), "\n")
    return (0)


#####################################################################
# Programme principal :
if __name__ == "__main__":
    main()