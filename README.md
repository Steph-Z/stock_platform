#  Stock-Learning-Projekt: https://stephs-plotpoint.onrender.com/

In this project I want to **learn how to develop and deploy a Data App / Dashboard** using Python and related libraries.  
The inital loading time of the Dashboard might take up to a minute, as a result from renders **free** hosting service

The goal is to build a small but scalable financial dashboard that fetches real-time data, provides interactive charts, and calculates useful stock metrics. I focus on learning classical software engineering skills required in DS or AI engineering roles. This includes thinking about **Testing, CI/CD, robustness, readability**. Additionally, this is a **learning project**, so next to standard comments in the code, I highlight things I learned on the way and found interesting and noteworthy.

---

Since writing near-production level code and tests, even for a small dashboard, can quickly become overwhelming without relying on LLM help (and I do not want to use that too much in a learning project), please refer to special sections where I focus on specific tasks.

---

For **Testing**, please refer to `testing_learnings.ipynb` and `tests/test_user_input.py` to see how I check the functions that handle the initial user input for a Stock (ISIN or Ticker). If you have any suggestions, feel free to contact me about it.


##  Tech Stack

For this project I am using:

- **Python 3.13.7**
- **Plotly / Dash** – interactive charts & UI
- **pandas** – data wrangling
- **yfinance** – real-time stock/financial data
- **pytest** - for unit and integration tests
- **Github Actions** -for automating Tests
- **pipreqs** - to manage the requirements.txt
- **gunicorn** - as a HTTP server
- **Render** - to host the dashboard
- **cachetools** - for caching some data of a session
---

##  Deployment

The app is hosted under:
- https://stephs-plotpoint.onrender.com/
- The dashboard is hosted through render. 
- A big thank you goes to https://github.com/thusharabandara/dash-app-render-deployment for helping with a steep learning curve

---

##  Using the App

- Search for stocks via **ISIN or Tracker** (or ticker symbol).  
- Visualize price history with different **chart types** (line, candlestick, etc.).  
- Choose from **predefined timeframes** or interact with the charts

---

##  Setup (Local Development)

To set up the project locally, follow these steps:

1. **Clone the repository**  
   Download the project to your machine:

2. **Create and activate a virtual environment**  
Set up a Python virtual environment to isolate dependencies:


3. **Install required libraries**  
Use the `requirements.txt` file to install dependencies:

4. **Install the project in editable mode**  
This allows you to make changes to the source code without reinstalling:
pip install -e "root_of_project"
