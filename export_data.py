#!/usr/bin/env python3
"""
Export data from Railway PostgreSQL to local JSON files
Run this once on Railway deployment, then use JSON files locally
"""
import os
import json
import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL")

def export_data():
    if not DATABASE_URL:
        print("No DATABASE_URL found!")
        return
    
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    # Export settings
    cur.execute("SELECT key, value FROM settings")
    rows = cur.fetchall()
    
    data = {}
    for key, value in rows:
        try:
            data[key] = json.loads(value)
        except:
            data[key] = value
    
    # Save each key as separate JSON file
    for key, value in data.items():
        filename = f"{key}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(value, f, ensure_ascii=False, indent=2)
        print(f"Exported: {filename}")
    
    conn.close()
    print("Done!")

if __name__ == "__main__":
    export_data()
