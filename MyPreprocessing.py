import pandas as pd

# function to convert review_time to datetime
def convert_time(df):
    df['date'] = pd.to_datetime(df['review_time'], unit='s')
    df['year'] = df['date'].dt.year
    return df

#Strongest brewery by abv
def strongest_brewery(df):
    max_brewery=df.groupby(["brewery_name","year"]).agg(max=("beer_abv","max")).reset_index()
    return max_brewery[max_brewery["max"]==max_brewery["max"].max()]

# Strongest brewery by abv by year
def strongest_brewery_year(df,year):
    tmp=df[df["year"]==year]
    max_brewery=tmp.groupby(["brewery_name"]).agg(max=("beer_abv","max")).reset_index()
    return max_brewery[max_brewery["max"]==max_brewery["max"].max()]


## Sélectionner les données au delà d'une année


def beer_after_date(df, year):
    mask = df["year"] > year
    df_date = df[mask]
    beer_id_year = list(df_date["beer_beerid"].unique())
    mask_beer = df["beer_beerid"].isin(beer_id_year)
    return  df[mask_beer]

# Nombre de fois qu'une fois qu'une bière a été noté plus d'une fois
def beer_rating(df):
    df=df.groupby("beer_beerid").agg(Count=("beer_beerid","count"))
    return df.reset_index()

# Top beers

def top_bieres(df,seuil):

    tmp = df.groupby(['beer_beerid']).aggregate({'review_overall': 'mean', 'review_taste': 'mean'
                                                 })
    rating_beer_id=beer_rating(df)
    tmp=pd.merge(tmp,
    rating_beer_id,
    how="inner",
    on="beer_beerid")

    mask1=tmp["Count"] > seuil
    tmp=tmp[mask1]
    tmp=tmp.sort_values(by=["review_overall","review_taste"],ascending=False)
    
    df= df[df["beer_beerid"].isin(tmp.beer_beerid)]
    df =df[["brewery_name","beer_beerid","beer_name"]].drop_duplicates()
    return df


##Beer_style rating

def beer_style_rating(df):
    df=df.groupby("beer_style").agg(Count=("beer_style","count"))
    return df.reset_index()


## Beer Style
def beer_style(df,seuil):

    tmp = df.groupby(['beer_style']).aggregate({'review_aroma': 'mean', 'review_appearance': 'mean'
                                                 })
    beer_style_grade=beer_style_rating(df)
    tmp=pd.merge(tmp,
    beer_style_grade,
    how="inner",
    on="beer_style")

    mask1=tmp["Count"] > seuil
    tmp=tmp[mask1]
    tmp=tmp.sort_values(by=["review_aroma","review_appearance"],ascending=False)
    
    df= df[df["beer_style"].isin(tmp.beer_style)]
    df =df[["beer_style","review_aroma","review_appearance"]].drop_duplicates()
    return df