import plotly as py
import plotly.graph_objs as go

import MySQLdb
import pandas as pd

conn = MySQLdb.connect(host="127.0.0.1", user="DESKTOP-OPATNA9\admin", passwd="", db="PL2018-2019")
cursor = conn.cursor()
cursor.execute('select HomeTeam, AwayTeam, FTHGM, FTAG, FTR, HTHG, HTAG, HTR, Referee, HS, AS, HST, AST, HF, AF, HC, AC, HY, AY, HR, AR');

rows = cursor.fetchall()
str(rows)[0:300]