import folium
import pandas
from flask import Flask, render_template

corona_df = pandas.read_csv(
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/08-13-2020.csv")
# now we have to remove NaN values from latitude and longitude cloumn(if there are any)
# because if there are then program will give error, as marker can not be place for NaN value
corona_df = corona_df.dropna(subset=['Lat'])
corona_df = corona_df.dropna(subset=['Long_'])


def find_top_confirmed(n=20):

    by_country = corona_df.groupby('Country_Region').sum()[
        ['Confirmed', 'Active', 'Deaths', 'Recovered']]
    confirmed_df = by_country.nlargest(n, 'Confirmed')[['Confirmed']]
    return confirmed_df


cdf = find_top_confirmed()  # .to_html()
data_pairs = [(country, confirmed)
              for country, confirmed in zip(cdf.index, cdf['Confirmed'])]

map1 = folium.Map(location=[28.644800, 77.216721],
                  zoom_start=3, tiles="Stamen toner")


def marker_placer(x):
    folium.Circle(location=[x[0], x[1]], radius=float(x[2]*0.6),
                  popup='{}\n Confrimed Cases: {}\nTotal Deaths: {}\nRecovered Cases: {}\nActive Cases: {}' .format(x[3], x[2], x[4], x[5], x[6]), color='red', fill=True).add_to(map1)


corona_df[['Lat', 'Long_', 'Confirmed', 'Combined_Key', 'Deaths', 'Recovered', 'Active']].apply(
    lambda x: marker_placer(x), axis=1)


html_map = map1._repr_html_()

app = Flask(__name__)


@ app.route('/')
def home():
    return render_template("home.html", table=cdf, covid_map=html_map, pairs=data_pairs)


if __name__ == '__main__':
    app.run(debug=True)
