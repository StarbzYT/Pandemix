from flask import Flask, render_template, request, redirect
from flask.helpers import url_for
import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator
from datetime import timedelta

# helper class with helper methods
class Helper:
   def get_vaccinated(self):
      vaccination_url = "https://news.google.com/covid19/map?hl=en-CA&state=7&mid=%2Fm%2F02j71&gl=CA&ceid=CA%3Aen"
      response = requests.get(vaccination_url)
      html_page = response.content
      soup = BeautifulSoup(html_page, 'html.parser')
      soup.prettify()
      # get vaccinated
      vaccinated = soup.findAll("div", {"class": "UvMayb"})[-1].get_text()
      return vaccinated

   def get_global(self):
      summary_data = requests.get('https://api.covid19api.com/summary').json()
      # grab global data (rest is not what we want)
      global_data = summary_data["Global"]
      # grab values of keys inside "Global"
      confirmed_cases = global_data["TotalConfirmed"]
      total_deaths = global_data["TotalDeaths"]
      total_recovered = global_data["TotalRecovered"]
      return tuple([confirmed_cases, total_deaths, total_recovered])

   def country_data(self):
      country = request.form.get("myCountry")
      # get current date (when this script is run)
      get_date = str(datetime.datetime.now())
      current_date = get_date.split()[0]
      url = f"https://api.covid19api.com/country/{country}?from={current_date}T00:00:00Z&to={current_date}T00:00:00Z"
      # grab last index of json dict to get most recent data
      country_data = requests.get(url).json()[-1]
      confirmed_cases = "{:,}".format(country_data["Confirmed"])
      deaths = "{:,}".format(country_data["Deaths"])
      recovered = "{:,}".format(country_data["Recovered"])
      return tuple([confirmed_cases, deaths, recovered])

   def display_graph(self):
      # load data
      # df = data frame
      df = pd.read_csv(
      'https://covid.ourworldindata.org/data/owid-covid-data.csv', 
      usecols=['date', 'location', 'total_vaccinations_per_hundred'], 
      parse_dates=['date'])

      countries = ['United States', 'Canada', 'United Kingdom', 'China']
       # make sure our data frame only includes the countries we specified
      df = df[df['location'].isin(countries)]
      pivot = pd.pivot_table(
      data=df,                                    # What dataframe to use
      index='date',                               # The "rows" of your dataframe
      columns='location',                         # What values to show as columns
      values='total_vaccinations_per_hundred',    # What values to aggregate
      aggfunc='mean',                             # How to aggregate data
      )
      pivot = pivot.fillna(method='ffill')
      # set colors
      main_country = 'Canada'
      colors = {country:('grey' if country!= main_country else '#129583') for country in countries}
      alphas = {country:(0.75 if country!= main_country else 1.0) for country in countries}
      fig, ax = plt.subplots(figsize=(12,8))
      fig.patch.set_facecolor('#F5F5F5')    # Change background color to a light grey
      ax.patch.set_facecolor('#F5F5F5')     # Change background color to a light grey

      for country in countries:
         ax.plot(
               pivot.index,              # What to use as your x-values
               pivot[country],           # What to use as your y-values
               color=colors[country],    # How to color your line
               alpha=alphas[country]     # What transparency to use for your line
            )
         ax.text(
            x = pivot.index[-1] + timedelta(days=2),    # Where to position your text relative to the x-axis
            y = pivot[country].max(),                   # How high to position your text
            color = colors[country],                    # What color to give your text
            s = country,                                # What to write
            alpha=alphas[country])                   # What transparency to use
      date_form = DateFormatter("%Y-%m-%d")
      ax.xaxis.set_major_locator(WeekdayLocator(byweekday=(0), interval=1))
      ax.xaxis.set_major_formatter(date_form)
      plt.xticks(rotation=45)
      plt.ylim(0,100)
      ax.spines['top'].set_visible(False)
      ax.spines['right'].set_visible(False)
      ax.spines['bottom'].set_color('#3f3f3f')
      ax.spines['left'].set_color('#3f3f3f')
      ax.tick_params(colors='#3f3f3f')
      ax.grid(alpha=0.1)
      # Adding a title and axis labels
      plt.ylabel('Total Vaccinations per 100 People', fontsize=12, alpha=0.9)
      plt.xlabel('Date', fontsize=12, alpha=0.9)
      plt.title('COVID-19 Vaccinations over Time', fontsize=18, weight='bold', alpha=0.9)
      # plot graph
      display = plt.show()
      return display

# instantiate app
app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def home():
   helper = Helper()  # instantiate helper class
   # add commas and helper class method
   confirmed_cases = "{:,}".format(helper.get_global()[0])
   total_deaths = "{:,}".format(helper.get_global()[1])
   total_recovered = "{:,}".format(helper.get_global()[2])
   global_vaccinated = helper.get_vaccinated()
   return render_template("home.html",
    vaccinated=global_vaccinated,
      cases=confirmed_cases,
      deaths=total_deaths,
      recovered=total_recovered)

@app.route('/search/', methods=["POST", "GET"])
def search():
   if request.method == 'POST':
      new_country = request.form.get("myCountry")
      helper = Helper()  # instantiate helper class
      confirmed_cases = helper.country_data()[0]
      deaths = helper.country_data()[1]
      recovered = helper.country_data()[2]
      return render_template("search.html", country=new_country, cases=confirmed_cases, deaths=deaths, recovered=recovered)
   return render_template("search.html", country="Select a Country", cases="Select a Country", deaths="Select a Country", recovered="Select a Country")

@app.route('/graph', methods=["GET", "POST"])
def graph():
   helper = Helper()
   graph = helper.display_graph()
   return render_template("graph.html", graph=graph)

# only run if this file is called
if __name__ == '__main__':
   app.run(debug=True)

