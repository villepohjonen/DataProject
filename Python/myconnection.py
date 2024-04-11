import plotly
plotly.__version__
import chart_studio.plotly as py
import plotly.graph_objs as go

import MySQLdb
import pandas as pd

conn = MySQLdb.connect(host="localhost", user="DESKTOP-OPATNA9\admin", passwd="", db="results.dbo")
cursor = conn.cursor()
cursor.execute('select date, home_team, away_team, home_score, away_score, tournament, city, country');

rows = cursor.fetchall()
str(rows)[0:300]
