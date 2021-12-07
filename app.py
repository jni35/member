from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    # return"<h1>Welcome~ 방문을 환영합니다.</h1>"

app.run(debug=True)
