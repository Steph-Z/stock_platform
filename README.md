# 📊 Stock-Projekt

In this project I want to **learn how to develop and deploy a Data App / Dashboard** using Python and related libraries.  
The goal is to build a small but scalable financial dashboard that fetches real-time data, provides interactive charts, and calculates useful stock metrics.

---

## 🚀 Tech Stack

For this project I am using:

- **Python 3.10+**
- **FastAPI** – backend API
- **Plotly / Dash (or React)** – interactive charts & UI
- **pandas** – data wrangling
- **yfinance** – real-time stock/financial data
- **pytest, black, flake8, mypy** – testing & code quality
- **Docker** – containerization & deployment

---

## 🌍 Deployment

The app is hosted under:  
👉 [https://your-app-url-here.com](https://your-app-url-here.com)  

*(replace with your actual deployment link once live)*

---

## 📈 Using the App

- Search for stocks via **WKN** (or ticker symbol).  
- Visualize price history with different **chart types** (line, candlestick, etc.).  
- Access **metrics** like volatility and returns.  
- Choose from **predefined timeframes** (7d, 30d, 1y) or set a **custom date range**.  

---

## 🔧 Setup (Local Development)

Clone the repo and install dependencies:

```bash
git clone https://github.com/your-username/stock-projekt.git
cd stock-projekt
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
