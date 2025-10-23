import yfinance as yf
import pandas as pd
from datetime import datetime, timezone



#old and unused for now
def calculate_volatility(timeframe:tuple, data:pd.DataFrame, ticker: str):
    '''This function calculates the volatility of a Stock for a given start and end date given by a tuple (start, end)
    in the format 'year-month-date', includes start state, omits end date '''
    
    data_adjusted = data['Close'].loc[(data['Date'] >= timeframe[0]) & (data['Date'] < timeframe[1])]
    
    vola_timeframe = data_adjusted.std() #already uses degrees of freedom
    
    return vola_timeframe, len(data_adjusted) #we could round but we can also have this as exact number and only round for the displayed output



#llm code, first explored and tested in a ipynb. 
#not blindly copied but was reviewd by me. 
#ask me for details on how i did this! 
#process: firs explored all key alue pairs of the metadata dict, then chose the important ones using my knowledge as a bank clerk.
#then looking at the fidderent formats i used a couple of long prompts to automatically build the dataframe as there are many preprocesisng/formatting steps needed

FORMAT_ORDER = [
    "currentPrice", "marketCap",
    "fiftyTwoWeekHigh", "52WeekChange", "allTimeHigh", "allTimeLow",
    "averageVolume10days", "averageVolume",
    "priceToBook", "enterpriseToRevenue", "enterpriseToEbitda",
    "dividendRate", "dividendYield", "lastDividendValue", "lastDividendDate", "fiveYearAvgDividendYield",
    "numberOfAnalystOpinions", "averageAnalystRating",
    "revenuePerShare", "grossProfits", "freeCashflow", "operatingCashflow", "netIncomeToCommon",
    "returnOnAssets", "returnOnEquity", "grossMargins", "ebitdaMargins", "operatingMargins",
    "earningsQuarterlyGrowth", "revenueGrowth",
]

FORMAT_LOOKUP = {
    "currentPrice": {"label":"Current price","type":"currency_price","group":"Price"},
    "marketCap": {"label":"Market cap","type":"currency_scaled","group":"Market & liquidity"},
    "fiftyTwoWeekHigh": {"label":"52‑week high","type":"currency_price","group":"Price"},
    "52WeekChange": {"label":"52‑week change","type":"percent_frac_or_str","group":"Performance"},
    "allTimeHigh": {"label":"All‑time high","type":"currency_price","group":"Price"},
    "allTimeLow": {"label":"All‑time low","type":"currency_price","group":"Price"},
    "averageVolume10days": {"label":"Avg volume (10d)","type":"integer","group":"Market & liquidity"},
    "averageVolume": {"label":"Avg volume","type":"integer","group":"Market & liquidity"},
    "priceToBook": {"label":"P/B ratio","type":"ratio","group":"Valuation & multiples"},
    "enterpriseToRevenue": {"label":"EV / Revenue","type":"ratio","group":"Valuation & multiples"},
    "enterpriseToEbitda": {"label":"EV / EBITDA","type":"ratio","group":"Valuation & multiples"},
    "dividendRate": {"label":"Dividend (annual)","type":"currency_price","group":"Dividend"},
    "dividendYield": {"label":"Dividend yield","type":"percent_raw","group":"Dividend"},
    "lastDividendValue": {"label":"Last dividend","type":"currency_price","group":"Dividend"},
    "lastDividendDate": {"label":"Last dividend date","type":"date_epoch_eu","group":"Dividend"},
    "fiveYearAvgDividendYield": {"label":"5y avg dividend yield","type":"percent_raw","group":"Dividend"},
    "numberOfAnalystOpinions": {"label":"Analyst count","type":"integer","group":"Analyst sentiment"},
    "averageAnalystRating": {"label":"Average analyst rating","type":"analyst_raw","group":"Analyst sentiment"},
    "revenuePerShare": {"label":"Revenue / share","type":"currency_price","group":"Profitability & margins"},
    "grossProfits": {"label":"Gross profit","type":"currency_scaled","group":"Profitability & margins"},
    "freeCashflow": {"label":"Free cash flow","type":"currency_scaled","group":"Cash flow"},
    "operatingCashflow": {"label":"Operating cash flow","type":"currency_scaled","group":"Cash flow"},
    "netIncomeToCommon": {"label":"Net income (to common)","type":"currency_scaled","group":"Profitability & margins"},
    "returnOnAssets": {"label":"ROA","type":"percent_frac_or_str","group":"Profitability & margins"},
    "returnOnEquity": {"label":"ROE","type":"percent_frac_or_str","group":"Profitability & margins"},
    "grossMargins": {"label":"Gross margin","type":"percent_frac_or_str","group":"Profitability & margins"},
    "ebitdaMargins": {"label":"EBITDA margin","type":"percent_frac_or_str","group":"Profitability & margins"},
    "operatingMargins": {"label":"Operating margin","type":"percent_frac_or_str","group":"Profitability & margins"},
    "earningsQuarterlyGrowth": {"label":"Earnings q/q growth","type":"percent_frac_or_str","group":"Growth"},
    "revenueGrowth": {"label":"Revenue growth","type":"percent_frac_or_str","group":"Growth"},
}

#helpers to build the df 

def _num(v):
    """Parse numeric-like input; returns float or None."""
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip()
    if s == "":
        return None
    s = s.replace("%", "").replace(" ", "")
    if "," in s and "." in s:
        s = s.replace(",", "")
    elif "," in s and "." not in s:
        s = s.replace(",", ".")
    try:
        return float(s)
    except Exception:
        return None

def _fmt_num(n, decimals=2):
    return f"{n:,.{decimals}f}"

def _fmt_currency_price(raw, symbol, eur_after):
    n = _num(raw)
    if n is None: return "N.A"
    s = _fmt_num(n, 2)
    return f"{s}€" if eur_after and symbol == "€" else (f"${s}" if symbol == "$" else f"{symbol}{s}")

def _fmt_currency_scaled(raw, symbol, eur_after):
    n = _num(raw)
    if n is None: return "N.A"
    if abs(n) >= 1_000_000_000:
        s = f"{n/1_000_000_000:,.2f} B"
    elif abs(n) >= 1_000_000:
        s = f"{n/1_000_000:,.2f} M"
    else:
        s = _fmt_num(n, 2)
    return f"{s}€" if eur_after and symbol == "€" else (f"${s}" if symbol == "$" else f"{symbol}{s}")

def _fmt_integer(raw):
    n = _num(raw)
    if n is None: return "N.A"
    return f"{int(round(n)):,}"

def _fmt_ratio(raw):
    n = _num(raw)
    return "N.A" if n is None else f"{n:.2f}"

def _fmt_date_eu(epoch):
    try:
        return datetime.fromtimestamp(int(epoch), tz=timezone.utc).strftime("%d.%m.%Y")
    except Exception:
        return "N.A"

def _fmt_percent_raw(raw):
    """Format raw numeric as 'xx.xx%' with no heuristics."""
    n = _num(raw)
    return "N.A" if n is None else f"{n:.2f}%"

def _fmt_percent_frac_or_str(raw):
    """If input is percent string keep it; else numeric fractions (<=1.5) -> *100."""
    if isinstance(raw, str) and "%" in raw:
        n = _num(raw)
        return "N.A" if n is None else f"{n:.2f}%"
    n = _num(raw)
    if n is None: return "N.A"
    return f"{(n*100):.2f}%" if abs(n) <= 1.5 else f"{n:.2f}%"

def _fmt_analyst_raw(raw):
    """Return analyst field as plain string, e.g. '1.8 - Buy' -> '1.8 - Buy' (cleaned)."""
    if raw is None:
        return "N.A"
    s = str(raw).strip()
    return s if s else "N.A"

# -------- main builder --------

def build_metrics_df(metadata: dict) -> pd.DataFrame:
    # currency selection: prefer financialCurrency then currency
    currency = metadata.get("financialCurrency") or metadata.get("currency")
    if currency == "USD":
        symbol, eur_after = "$", False
    elif currency in ("EUR", "€"):
        symbol, eur_after = "€", True
    elif isinstance(currency, str) and currency.strip():
        symbol, eur_after = currency.strip() + " ", False
    else:
        symbol, eur_after = "", False

    rows = []
    for key in FORMAT_ORDER:
        fmt = FORMAT_LOOKUP.get(key)
        if fmt is None:
            continue
        label = fmt["label"]
        group = fmt.get("group", "")
        ftype = fmt["type"]

        # direct lookup; keep known fallback for naming mismatch
        raw = metadata.get(key, None)

        if raw is None:
            value = "N.A"
        else:
            if ftype == "currency_price":
                value = _fmt_currency_price(raw, symbol, eur_after)
            elif ftype == "currency_scaled":
                value = _fmt_currency_scaled(raw, symbol, eur_after)
            elif ftype == "integer":
                value = _fmt_integer(raw)
            elif ftype == "ratio":
                value = _fmt_ratio(raw)
            elif ftype == "date_epoch_eu":
                value = _fmt_date_eu(raw)
            elif ftype == "percent_raw":
                value = _fmt_percent_raw(raw)
            elif ftype == "percent_frac_or_str":
                value = _fmt_percent_frac_or_str(raw)
            elif ftype == "analyst_raw":
                value = _fmt_analyst_raw(raw)
            else:
                value = str(raw)
        rows.append({"Label": label, "Value": value, "Group": group})

    return pd.DataFrame(rows)[["Label", "Value", "Group"]]