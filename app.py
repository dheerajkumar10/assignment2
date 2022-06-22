import json
import redis
from unittest import result
import pyodbc
from flask import Flask, render_template, request
import math
import time

app = Flask(__name__)


myHostname = "dxt3485.redis.cache.windows.net"
myPassword = "Q0OXaGyAsts64gD44uEG1zBg29yqHmKIAAzCaB0midM="

r = redis.StrictRedis(host=myHostname, port=6380,
                      password=myPassword, ssl=True)

result = r.ping()

server = 'dheeraj1045.database.windows.net'
database = 'dheerajdb'
username = 'dheeraj'
password = 'Dheer@jkumar1045'
driver = '{ODBC Driver 17 for SQL Server}'

cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server +
                      ';PORT=1443;DATABASE='+database+';UID='+username+';PWD=' + password)
cursor = cnxn.cursor()


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/random2', methods=['GET', 'POST'])
def random2():
    number = int(request.form["rnumber"])
    start = time.time()
    for i in range(0, number):
        query = "SELECT * FROM[dbo].[earthquake]"
        if(r.exists("task1")):
            r.get("task1")
            res = json.loads(r.get("task1"))
        else:
            data = list()
            cursor.execute(query)
            res = cursor.fetchall()
            for row in res:
                data.append([x for x in row])
            result1 = json.dumps(data)
            r.set("task1", result1)
    end = time.time()
    return render_template('random.html', num=res, data=end-start)


@app.route('/random1', methods=['GET', 'POST'])
def random1():
    number = int(request.form["rnumber"])
    city = request.form["city"]
    city = city.upper()
    start = time.time()
    for i in range(0, number):
        query = "SELECT TOP 5 * FROM [dbo].[earthquake] WHERE place  LIKE '%" + \
            city+"' ORDER BY NEWID() "
        print(query)
        result = cursor.execute(query)
    end = time.time()
    return render_template('random.html', num=result, data=end-start)


@app.route('/random', methods=['GET', 'POST'])
def random():
    number = int(request.form["rnumber"])
    start = time.time()
    for i in range(0, number):
        query = "SELECT * FROM[dbo].[earthquake]"
        result = cursor.execute(query)
    end = time.time()
    return render_template('random.html', num=result, data=end-start)


if __name__ == "__main__":
    app.run(debug=True)
