#!/usr/bin/env python3
import psycopg2
import json

OLD_DB = "postgresql://postgres:vFRwTXvxZWlPlriIkChyNDnbgNxpsRSD@interchange.proxy.rlwy.net:24304/railway"

print("Connecting to old DB...")
try:
    conn = psycopg2.connect(OLD_DB)
    cur = conn.cursor()
    cur.execute("SELECT key, value FROM settings")
    rows = cur.fetchall()
    
    for key, value in rows:
        try:
            data = json.loads(value)
            with open(f"{key}.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Exported: {key}")
        except Exception as e:
            print(f"Skip {key}: {e}")
    
    conn.close()
    print("DONE!")
except Exception as e:
    print(f"Error: {e}")