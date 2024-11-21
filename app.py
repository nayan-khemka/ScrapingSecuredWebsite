from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
from datetime import datetime
import os
import pytz

app = Flask(__name__)

username = "user"
password = "password"

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    if request.form['username'] == username and request.form['password'] == password:
        return redirect(url_for('data_page'))
    else:
        return "Login Failed"

@app.route('/data')
def data_page():
    now_utc = datetime.now(pytz.utc)
    cities = {
        "New York": now_utc.astimezone(pytz.timezone('America/New_York')).strftime("%Y-%m-%d %H:%M:%S"),
        "London": now_utc.astimezone(pytz.timezone('Europe/London')).strftime("%Y-%m-%d %H:%M:%S"),
        "Tokyo": now_utc.astimezone(pytz.timezone('Asia/Tokyo')).strftime("%Y-%m-%d %H:%M:%S")
    }

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {
        "Timestamp": [now],
        "Value": [42]
    }
    df = pd.DataFrame(data)
    df.to_csv('data.csv', index=False, mode='a', header=not os.path.exists('data.csv'))

    return render_template('data.html', tables=[df.to_html(classes='data')], titles=df.columns.values, cities=cities)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
