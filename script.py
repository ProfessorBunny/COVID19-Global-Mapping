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


map = folium.Map(location=[28.644800, 77.216721],
                 zoom_start=4, tiles="Stamen toner")


def marker_placer(x):
    folium.Circle(location=[x[0], x[1]], radius=10000,
                  popup='{}\nConfrimed Cases: {}' .format(x[3], x[2]), fill=True).add_to(map)


corona_df[['Lat', 'Long_', 'Confirmed', 'Combined_Key']].apply(
    lambda x: marker_placer(x), axis=1)

map.save('map1.html')
