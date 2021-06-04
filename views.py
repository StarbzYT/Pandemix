from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import datetime

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
      confirmed_cases = country_data["Confirmed"]
      deaths = country_data["Deaths"]
      recovered = country_data["Recovered"]
      return tuple([confirmed_cases, deaths, recovered])

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
   return render_template("search.html", country="Select a Country", cases="Select a Country", deaths="Select a Country", recovered="Select a Country" )

# only run if this file is called
if __name__ == '__main__':
   app.run(debug=True)

