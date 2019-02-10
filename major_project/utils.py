import pandas as pd
import matplotlib.pyplot as plt


def cleaning_columns(filename):
    df = pd.read_csv(filename, index_col='title')
    df.loc[:, 'price'] = df.price.str.replace(',', '')
    df.loc[:, 'price'] = df.price.str.replace('-','')
    df.loc[:, 'price'] = df.price.str.strip(' ')
    df.price.fillna(0,inplace=True)
    df.company.fillna("n/a",inplace=True)
    df.brand=df.brand.str.strip()
    df.loc[:, 'totalreviews'] = df.totalreviews.str.replace('customer reviews', '')
    df.loc[:, 'totalreviews'] = df.totalreviews.str.replace(',', '')
    df.loc[:, 'totalreviews'] = df.totalreviews.str.replace('customer review', '')
    df.totalreviews=df.totalreviews.str.strip()
    print(df.totalreviews)

    return df


def totalreviews(df, filename):
    print(df.totalreviews)
    df.totalreviews = df.totalreviews.astype(float, True)
    fig = plt.figure()
    df.sort_values('totalreviews').totalreviews.plot(kind='barh', figsize=(13, 10))
    return fig.savefig(filename, bbox_inches='tight')


def rating(df, filename):
    df.rating = df.rating.astype(float, True)
    fig = plt.figure()
    df.sort_values('rating').rating.plot(kind='barh', figsize=(13, 10))
    return fig.savefig(filename, bbox_inches='tight')


def price(df, filename):
    df.price = df.price.astype(float, True)
    fig = plt.figure()
    df.sort_values('price').price.plot(kind='barh', figsize=(13, 10))
    return fig.savefig(filename, bbox_inches='tight')


def pie_price(df, filename):
    df.price = df.price.astype(float, True)
    fig = plt.figure()
    df[['brand', 'price']].groupby('brand').max().sort_values(by='price').tail(10).plot(kind='pie', subplots=True,
                                                                                        legend=False, autopct='%.2f%%',
                                                                                        figsize=(13, 10))
    plt.title('Brand wise price analysis')
    return plt.savefig(filename, bbox_inches='tight')


def pie_rating(df, filename):
    df.rating = df.rating.astype(float, True)
    fig = plt.figure()
    df[['brand', 'rating']].groupby('brand').sum().sort_values(by='rating').tail(10).plot(kind='pie', subplots=True,
                                                                                          legend=False,
                                                                                          autopct='%.2f%%',
                                                                                          figsize=(13, 10))
    plt.title('Brand wise rating analysis')
    return plt.savefig(filename, bbox_inches='tight')


def pie_reviews(df, filename):
    df.totalreviews = df.totalreviews.astype(float, True)
    fig = plt.figure()
    df[['brand', 'totalreviews']].groupby('brand').sum().sort_values(by='totalreviews').tail(10).plot(kind='pie',
                                                                                                      subplots=True,
                                                                                                      legend=False,
                                                                                                      autopct='%.2f%%',
                                                                                                      figsize=(13, 10))
    plt.title('Brand wise review analysis')
    return plt.savefig(filename, bbox_inches='tight')


def recommend_on_prefs(df,prefers):
    if prefers =='price':
        return 'price',df.price.idxmin()
    else:
        brand=df.reset_index()[['title','rating','brand']].dropna(axis=0).groupby('rating').max().iloc[-1][1]
        product=df.reset_index()[['title','rating','brand']].dropna(axis=0).groupby('rating').max().iloc[-2][0]
        if len(brand)<=1:
            brand=df.reset_index()[['title','rating','brand']].dropna(axis=0).groupby('rating').max().iloc[-2][1]
        else:
            brand=df.reset_index()[['title','rating','brand']].dropna(axis=0).groupby('rating').max().iloc[-3][1]
        return 'brand',product 

def recommend_on_reviews(df,reviews):
    return 'reviews',df.reviews.dropna(axis=0).idxmax()
def recommend_on_rating(df,rating):
    return 'ratings',df.rating.dropna(axis=0).sort_values().idxmax()