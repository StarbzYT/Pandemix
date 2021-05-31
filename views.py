from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

# helper class with helper methods
class Helper:
   def get_vaccinated(self):
      vaccination_url = "https://covidvax.live/"
      response = requests.get(vaccination_url)
      html_page = response.content
      soup = BeautifulSoup(html_page, 'html.parser')
      # get vaccinated
      vaccinated = soup.find(id="tilePeopleVaccinated").get_text()
      return vaccinated

   def get_global(self):
      summary_data = requests.get('https://api.covid19api.com/summary').json()
      global_data = summary_data["Global"]
      confirmed_cases = global_data["TotalConfirmed"]
      total_deaths = global_data["TotalDeaths"]
      total_recovered = global_data["TotalRecovered"]
      return tuple([confirmed_cases, total_deaths, total_recovered])

# instantiate app
app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def home():
   helper = Helper()
   confirmed_cases = "{:,}".format(helper.get_global()[0])
   total_deaths = "{:,}".format(helper.get_global()[1])
   total_recovered = "{:,}".format(helper.get_global()[2])
   global_vaccinated = helper.get_vaccinated()
   return render_template("home.html",
    vaccinated=global_vaccinated,
      cases=confirmed_cases,
      deaths=total_deaths,
      recovered=total_recovered)

# only run if this file is called
if __name__ == '__main__':
    app.run()
    home()
