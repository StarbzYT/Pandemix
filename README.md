# COVID-Tracer

---

## **About**

This website was made with **Python** (_flask framework_), **HTML**, **CSS**, **BootStrap**, and the [PostMan COVID-19 API](https://documenter.getpostman.com/view/10808728/SzS8rjbc#00030720-fae3-4c72-8aea-ad01ba17adf8 "COVID API"). The user can:

> - View _**global**_ COVID _cases_, _deaths_, _recovered_, and _fully vaccinated_ (2 doses).
> - _**Search**_ any country's COVID _cases_, _deaths_, and _recovered_.
> - Analyze top-country's _**vaccination**_ projections (US, UK, Canada, China).

---

## **Wireframe**

![covid tracer wireframe](https://user-images.githubusercontent.com/57025422/120940805-ea864800-c6d3-11eb-8469-175013ccb571.PNG)

I decided to change the "history" endpoint to "Vaccination Graph". As a result, the last endpoint only shows one graph instead of three shown in the wireframe above.

---

## **The Result**

### 'Home' Endpoint

![home covid tracer](https://user-images.githubusercontent.com/57025422/120943735-a0a65d80-c6e5-11eb-8ee4-57004940fc1e.PNG)

The data used in the table was grabbed from the _COVID-API_.

### 'Search' Endpoint

![search covid tracer](https://user-images.githubusercontent.com/57025422/120943778-e6fbbc80-c6e5-11eb-8f09-7db3486f823c.PNG)

I used a script tag that auto-generates countries based on what the user types in the search bar.

### 'Vaccination Chart' Endpoint

![vaccination chart covid tracer](https://user-images.githubusercontent.com/57025422/120943806-0c88c600-c6e6-11eb-97cf-18de51898a09.PNG)

The pop-up graph was plotted using _matplotlib_. Once the user clicks 'see graph' it will generate.

---

## Potential Improvements

Using _matplotlib_ for this website sometimes caused a 'RuntimeError'. Instead, using **chart.js** would have just displayed the graph on the website itself rather than a pop-up. Hence, the error would have been, for the most part, avoided.

After making this website, I realized it would have been easier to use 'Flask-Bootstrap', which would have taken care of the _links_ and _jquery_ scripts for me.

If you use the website, you will notice that, at times, the website is quite slow. I believe that my HTML templates are waiting for the API calls to display the information. Simplifying the number of operations on some of the backend endpoints would decrease loading times.

---

## Install

```bash
pip install flask
pip install pandas
pip install bs4
pip install requests
pip install matplotlib
```

---

## **Import**

```python
from flask import Flask, render_template, request, redirect
from flask.helpers import url_for
import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator
from datetime import timedelta
```

---

## **Run**

```bash
python views.py
```

---

### **Inspiration**

Last year (just after the pandemic began), I made a simple **web scraper** that scraped the cases, deaths, and recovered off [WorldoMeters](https://www.worldometers.info/coronavirus/?utm_campaign=homeAdvegas1 "The website I scraped"), and inserted them into a _SQLite3_ database. Since then, I wanted to create a new version of the app, but with a **frontend** and **backend**. You can view my first/original version of this project [here](https://github.com/StarbzYT/Covid-App "Simple Covid Scraper").