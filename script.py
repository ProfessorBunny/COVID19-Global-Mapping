import folium
import pandas

corona_df = pandas.read_csv(
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/08-10-2020.csv")
corona_df = corona_df.dropna(subset=['Lat'])
corona_df = corona_df.dropna(subset=['Long_'])


def find_top_confirmed(n=15):

    by_country = corona_df.groupby('Country_Region').sum()[
        ['Confirmed', 'Active', 'Deaths', 'Recovered']]
    confirmed_df = by_country.nlargest(n, 'Confirmed')[['Confirmed']]
    return confirmed_df
