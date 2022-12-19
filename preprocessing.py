import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Analyse exploratoire

def var_categories(df):
    """Cette fonction renvoie la liste des variables qualitative et quantitative"""
    # code
    nature = {"Qualitatives":[],"Quantitatives":[]}
    for col in df.columns:
        if df[col].dtype == object :
            nature["Qualitatives"].append(col)
        else:
            nature["Quantitatives"].append(col)
    return nature


def plot_missing_values(df):
        """Cette fonction dessine le graphique des valeurs manquantes"""
        # code
        df = (df.isna().sum().sort_values()/df.shape[0])*100
        df = df[df!=0]
        if df.empty:
                return 'No missing data!'
        else:
                df.plot(kind='barh',title = 'missing values',
                        xlabel = 'Pourcentages',
                        ylabel = 'Variables')
                return plt.show()
            

def missing_values(df):
        "Cette fonction renvoie les valeurs manquantes"
        # code
        df,taille = df.isna().sum().sort_values(),df.shape[0]
        df = df[df!=0]
        if df.empty :
                return 'No missing data !'
        else:
                df = pd.DataFrame({"Variable":list(df.index),"Count":list(df),"Percentage (%)":list((df/taille)*100)})
                return df
            
def drop_na(df,var):
    """Cette fonction supprime les valeurs manquantes d'une variable."""
    # code
    df.dropna(subset = var,inplace=True)
    return "validate !"

# Analyse sur le jeu de données beer_reviews.csv

def date_time_year(df,var):
    """Cette fonction crée transforme une date coder en entier en une date normale
        et en extrait l'année """
    # code
    df['date_time'] = pd.to_datetime(df[var],unit ="s")
    df['year'] = df['date_time'].dt.year
    return "validate !"

def strong_brewery(df,criteria,year=0):
    """Cette fonction retourne la brasserie qui fabrique la biere la plus alcoolisé.
    
        Parametres:
        
            - df : DataFrame
            - criteria : Critere de recherche
            - year : année de récherche
            """
    # code
    if year == 0 :
        df = df[df[criteria]==df[criteria].max()]
        df["best_abv"] = df[criteria].max()
        df = df[["brewery_id","brewery_name","beer_name","year","best_abv"]]
        return df
    elif year in df["year"]:
        
        return "This year dot not exist! Try again please !"
    else:
        mask = df["year"] == year
        df = df[mask]
        df = df[df[criteria]==df[criteria].max()]
        df["best_abv"] = df[criteria].max()
        df = df[["brewery_id","brewery_name","beer_name","year","best_abv"]]
        return df

def select_start_year(df,y):
    """Cette fonction donnes les informations des bieres à partir d'une année en tenant compte des historiques """
    #code
    beer_id = list(df[df["year"]>=y]['beer_beerid'])
    return df[df['beer_beerid'].isin(beer_id)]

def beer_rating(df,key):
    """Cette fonction renvoies le nombre de fois qu'une bieres à été notée."""
    #code
    df = df.groupby(by=key).agg(Count=(key,"count"))
    return df.reset_index()

def top_beers(df,thresold):
    """Cette fonction renvoies les meilleures bieres.
        Parametres:
            - df : le dataFrame
            - thresold : Le nombre minimale de fois que la bieres à été notée"""
    #code
    tmp = df.groupby(['beer_beerid']).aggregate({'review_overall': 'mean',
                                                 'review_taste': 'mean'})
    rating_beer_id = beer_rating(df,'beer_beerid')
    tmp = pd.merge(tmp, rating_beer_id, 
                   how='inner', 
                   on='beer_beerid')
    mask1 = tmp['Count'] > thresold
    tmp = tmp[mask1]
    tmp = tmp.sort_values(by=['review_overall','review_taste'],ascending=False)
    df = df[df['beer_beerid'].isin(tmp.beer_beerid.unique())]
    df = df[['brewery_id','brewery_name','beer_beerid','beer_name']].drop_duplicates()

    return tmp,df

def most_influence_factor(df):
    """Cette fonction renvoie le facteurs le plus important pour déterminer la  note global."""
    # code
    df3 = df[["review_overall",'review_aroma',"review_appearance","review_taste","review_palate"]]
    corr = df3.corr().drop(index="review_overall")[["review_overall"]]\
                   .sort_values(by="review_overall",ascending=False)
    corr.columns = ["correlation_with_overall"]
    res = corr[corr["correlation_with_overall"]==corr["correlation_with_overall"].max()]
    return corr, res

def best_beer_style(df,thresold):
    """Cette fonction renvoies les meilleures bieres.
        Parametres:
            - df : le dataFrame
            - thresold : Le nombre minimale de fois que la bieres à été notée"""
    # code
    tmp = df.groupby(['beer_style']).aggregate({'review_aroma': 'mean',
                                                 'review_appearance': 'mean'})
    rating_beer_style = beer_rating(df,'beer_style')
    tmp = pd.merge(tmp, rating_beer_style, 
                   how='inner', 
                   on='beer_style')
    mask = tmp['Count'] > thresold
    tmp = tmp[mask]
    tmp = tmp.sort_values(by=['review_aroma','review_appearance'],ascending=False)
    df = tmp.drop_duplicates().drop(columns="Count")
    
    return df