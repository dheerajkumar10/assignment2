from decimal import Decimal
from math import degrees
import re
from tkinter import Place
from turtle import distance
import pyodbc
import datetime as dt
from datetime import datetime
from pytz import timezone
import pytz
from flask import Flask, render_template, request
import pandas as pd
import math

app = Flask(__name__)

server = 'dheeraj1045.database.windows.net'
database = 'dheerajdb'
username = 'dheeraj'
password = 'Dheer@jkumar1045'
driver = '{ODBC Driver 17 for SQL Server}'

cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server +
                      ';PORT=1443;DATABASE='+database+';UID='+username+';PWD=' + password)
cursor = cnxn.cursor()


@app.route("/")
def hello_world():
    cursor.execute("SELECT * FROM [dbo].[earthquake]")
    num = cursor.fetchall()
    return render_template('index.html', num=num)


@app.route('/Filter', methods=['GET'])
def filter_magnitude():
    query = "SELECT * FROM [dbo].[earthquake]"
    if request.args.get('magnitude'):
        query += " and mag > "+request.args.get('magnitude')

    if request.args.get('distance'):
        current_longitude = request.args.get('longitude')
        current_latitude = request.args.get('latitude')
        degrees = 0.009 * float(request.args.get('distance'))
        query += " and Longitude >=" + current_latitude + '-' + str(degrees) + " and Longitude <=" + current_latitude + '+' + str(
            degrees) + 'and Latitude >=' + current_longitude + '-' + str(degrees) + 'and Latitude <=' + current_longitude + '+' + str(degrees)

    if request.args.get('lower_mag'):
        lower_limit = request.args.get('lower_mag')

        query += "and mag >= " + lower_limit

    if request.args.get('higher_mag'):
        higher_limit = request.args.get('higher_mag')
        query += "and mag  <=" + higher_limit

    if request.args.get('from_date'):
        initial_date = request.args.get('from_date')
        query += "and time >= " + "'" + initial_date + "'"

    if request.args.get('to_date'):
        final_date = request.args.get('to_date')
        query += "and time <= " + "'" + final_date + "'"

    if request.args.get('from_time'):
        start_time = request.args.get('from_time')
        query += "and CAST (time as time) >= " + "'" + start_time + "'"

    if request.args.get('to_time'):
        end_time = request.args.get('to_time')
        query += "or CAST (time as time) <= " + "'" + end_time + "'"

    # if (request.args.get('magnitude')) and (request.args.get('from_time') or request.args.get('to_time')):

    #     query="SELECT * FROM [dbo].[earthquake] where mag > 4.0"
    #     cursor.execute(query)
    #     total=cursor.fetchall()
    #     query_time="SELECT * FROM [dbo].[earthquake] WHERE time >= cast(DATEADD(DAY,-30,cast(GETDATE() as data)) as datetime"
    #     cursor.execute(query_time)
    #     in_time_interval = cursor.fetchall()
    #     probability=len(in_time_interval)/len(total)

    #     if probability >=0.75:
    #         likelihood ='Highly likely'
    #     elif probability >=0.5 and probability <0.75:
    #         likelihood ='Moderately likely'
    #     elif probability >=0.25 and probability <0.5:
    #         likelihood ='Less likely'
    #     else:
    #         likelihood = 'Unlikely'

    result = cursor.execute(query)

    # print(likelihood)
    return render_template('index.html', num=result)


def euclidean_distance(row1, row2):
    distance = 0.0
    for i in range(len(row1)-1):
        distance = distance + (row1[i] - row2[i])**2
        sqrtdistance = math.sqrt(distance)
    return sqrtdistance


@app.route("/Clusters", methods=['POST', 'GET'])
def Clusters():
    query = "SELECT latitude, longitude FROM [dbo].[earthquake] "
    df = pd.read_sql(query, cnxn)
    print(df.head(5))
    c1 = (33.288667, -115.991000)
    c2 = (62.056200, -150.887100)
    c3 = (19.698166, -155.176163)
    cluster1 = list()
    cluster2 = list()
    cluster3 = list()
    for index, row in df.iterrows():
        d = euclidean_distance((row['latitude'], row['longitude']), c1)
        e = euclidean_distance((row['latitude'], row['longitude']), c2)
        f = euclidean_distance((row['latitude'], row['longitude']), c3)
        if((d < e) and (d < f)):
            cluster1.append(row)
        elif((e < f) and (e < d)):
            cluster2.append(row)
        elif((f < d) and (f < e)):
            cluster3.append(row)
        else:
            print("")

    print(len(cluster1))
    return render_template('index.html', cluster=cluster1, cluster2=cluster2, cluster3=cluster3)


# @app.route('/Distance',methods=['GET'])
# def find_distance():
#     if request.args.get('search_action') == 'Search_Distance':
#         message = ''

#         if not request.args.get('latitude') or not request.args.get('longitude'):
#             message += 'Latitude and Longitude is not specified'


#         current_longitude= request.args.get('longitude')
#         current_latitude= request.args.get('latitude')
#         degrees = 0.009 * float(request.args.get('distance'))
#         distance_query = "SELECT * FROM [dbo].[earthquake] where Longitude >="+ current_latitude + '-'+ str(degrees) + " and Longitude <=" + current_latitude + '+' + str(degrees) + 'and Latitude >=' + current_longitude + '-' + str(degrees) + 'and Latitude <=' + current_longitude + '+' + str(degrees)
#         query = cursor.execute(distance_query)
#         print("SELECT * FROM [dbo].[earthquake] where Latitude >="+ current_latitude + '-'+ str(degrees) + " and Latitude <=" + current_latitude + '+' + str(degrees) + 'and longitude >=' + current_longitude + '-' + str(degrees) + 'and longitude <=' + current_longitude + '+' + str(degrees))
#     return render_template('index.html', num=query.fetchall())


# a="2.0"
# b="2.5"
# d="7"

# cursor.execute("SELECT count(*) FROM [dbo].[earthquake] where mag > " + a + "and mag  <" + b + "and DATEDIFF(DAY,time , GETDATE()) between 0 and 7 " )
# num1 =cursor.fetchall()
# print(" The earthquakes with magnitude between 2 and 2.5 are: " ,num1 )


# Greenwich = timezone('ETC/Greenwich')
# now = datetime.now()
# print(now)
# published_gmt = now.astimezone(Greenwich)
# actual_time_published = published_gmt.strftime('%a, %b %d %Y at %I:%M:%S %p %Z')

# print(actual_time_published)


# SELECT COUNT(*) ( 3959 * acos( cos( radians(37) ) * cos( radians( latitude ) ) * cos( radians( longitude ) - radians(-122) ) + sin( radians(37) ) * sin( radians( lat ) ) ) ) AS distance FROM [dbo].[earthquake] HAVING distance < 25 ORDER BY distance LIMIT 0 , 20;

if __name__ == "__main__":
    app.run(debug=True)
