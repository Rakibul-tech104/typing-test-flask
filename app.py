from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users
                 (name TEXT, email TEXT, phone TEXT, wpm INTEGER, accuracy REAL, submitted_at TEXT)""")
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    return render_template('test.html', name=name, email=email, phone=phone)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    wpm = int(request.form['wpm'])
    accuracy = float(request.form['accuracy'])
    now = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", (name, email, phone, wpm, accuracy, now))
    conn.commit()
    conn.close()

    return render_template('result.html', name=name, wpm=wpm, accuracy=accuracy)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8080)