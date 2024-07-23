import json
import requests
from datetime import datetime
import sqlite3

def create_record(data: dict, date) -> None:
    record = (
        data['id'],
        data['name'],
        data['dateEnd'],        
        data['status'],
        data['lastTradePrice'],
        data['bestBuyYesCost'],
        data['bestBuyNoCost'],
        data['bestSellYesCost'],
        data['bestSellNoCost'],
        data['lastClosePrice'],
        data['displayOrder'],
        date
    )
    cursor.execute('INSERT INTO main VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', record)
    conn.commit()

if __name__ == "__main__":

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS main (
        id INTEGER PRIMARY KEY,
        name TEXT,
        dateEnd TEXT,        
        status TEXT,
        lastTradePrice REAL,
        bestBuyYesCost REAL,
        bestBuyNoCost REAL,
        bestSellYesCost REAL,
        bestSellNoCost REAL,
        lastClosePrice REAL,
        displayOrder INTEGER,
        lastUpdated TEXT
    )
''')

    
    with requests.Session() as s:
        r = s.get("https://www.predictit.org/api/marketdata/all/")
        data = json.loads(r.content)
        print(data)

        for x in data['markets']:
            date = datetime.fromisoformat(x['timeStamp']).strftime('%m-%d-%Y')
            for y in x['contracts']:
                create_record(y, date)
