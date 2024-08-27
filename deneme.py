import sqlite3
import pandas as pd

con = sqlite3.connect("./giris_tablo.db")
df = pd.read_sql_query(f"SELECT * FROM tablo_verileri", con)
df.to_csv("./tablo_to_csv4.csv", index=False)
