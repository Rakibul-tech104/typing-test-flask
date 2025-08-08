from flask import Flask, render_template, request, redirect, session
import time
import difflib

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required to use sessions

TYPING_PROMPT = "The quick brown fox jumps over the lazy dog."

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['name'] = request.form['name']
        session['email'] = request.form['email']
        session['phone'] = request.form['phone']
        return redirect("/test")
    return render_template("index.html")

@app.route("/test", methods=['GET'])
def test():
    session['start_time'] = time.time()
    return render_template("test.html", prompt=TYPING_PROMPT, start_time=session['start_time'])

@app.route("/result", methods=['POST'])
def result():
    end_time = time.time()
    start_time = float(request.form['start_time'])
    typed_text = request.form['typed_text']
    original_text = request.form['prompt']
    time_taken = end_time - start_time

    # Calculate Words Per Minute (WPM)
    word_count = len(typed_text.split())
    minutes = time_taken / 60
    wpm = round(word_count / minutes, 2) if minutes > 0 else 0

    # Calculate accuracy
    matcher = difflib.SequenceMatcher(None, original_text, typed_text)
    accuracy = round(matcher.ratio() * 100, 2)

    return render_template("result.html", wpm=wpm, accuracy=accuracy,
                           name=session.get('name'),
                           email=session.get('email'),
                           phone=session.get('phone'))

if __name__ == '__main__':
    app.run(debug=True)
