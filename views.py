from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

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

@app.route('/search', methods=["GET", "POST"])
def search():
   if request.method == "POST":
      country = request.form.get("myCountry")
   return render_template("search.html")

# only run if this file is called
if __name__ == '__main__':
   app.run(debug=True)

