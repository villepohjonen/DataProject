from myconnection import connect_to_mysql

config = {
    "host": "localhost",
    "user": "DESKTOP-OPATNA9\admin",
    "password": "",
    "database": "PL2018-2019",
}

cnx = connect_to_mysql(config, attempts=3)

if cnx and cnx.is_connected():

    with cnx.cursor() as cursor:

        result = cursor.execute("SELECT * FROM PL2018-2019")

        rows = cursor.fetchall()

        for rows in rows:

            print(rows)

    cnx.close()

else:

    print("Could not connect")