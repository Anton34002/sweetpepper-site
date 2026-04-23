#!/usr/bin/env python3
import psycopg2
import os
import json
import ssl

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:vFRwTXvxZWlPlriIkChyNDnbgNxpsRSD@interchange.proxy.rlwy.net:24304/railway")

print("Trying different connection options...")

options_to_try = [
    DATABASE_URL + "?sslmode=require",
    DATABASE_URL + "?sslmode=verify-full",
    DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://") + "?sslmode=require",
]

for url in options_to_try:
    print(f"\nTrying: {url[:50]}...")
    try:
        conn = psycopg2.connect(url, connect_timeout=10)
        print("Connected!")
        
        cur = conn.cursor()
        cur.execute("SELECT key, value FROM settings")
        rows = cur.fetchall()
        
        print(f"Found {len(rows)} settings")
        for key, value in rows:
            print(f"  - {key}")
            try:
                data = json.loads(value)
                with open(f"{key}.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            except:
                pass
        
        conn.close()
        print("Done!")
        break
    except Exception as e:
        print(f"  Failed: {e}")