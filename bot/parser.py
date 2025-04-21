import re
import requests
from lxml import etree
import pandas as pd


def parse_price(text: str) -> float | None:
    cleaned = re.sub(r'[^\d,\.]', '', text)
    if cleaned.count(',') == 1 and cleaned.count('.') == 0:
        cleaned = cleaned.replace(',', '.')
    cleaned = cleaned.replace(' ', '')
    try:
        return float(cleaned)
    except ValueError:
        return None


def compute_average_prices(df: pd.DataFrame) -> pd.DataFrame:
    results = []
    for url, group in df.groupby('url'):
        prices = []
        for _, row in group.iterrows():
            try:
                resp = requests.get(url, timeout=10)
                tree = etree.HTML(resp.text)
                elems = tree.xpath(row['xpath'])
                if not elems:
                    continue
                raw = elems[0].text_content()
                price = parse_price(raw)
                if price is not None:
                    prices.append(price)
            except Exception:
                continue
        avg = sum(prices) / len(prices) if prices else None
        results.append({'url': url, 'average_price': avg})
    return pd.DataFrame(results)
