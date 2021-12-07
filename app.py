from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def getconn():
    conn = sqlite3.connect('./memberdb.db')
    return conn

@app.route('/')
def index():
    return render_template('index.html')
    # return"<h1>Welcome~ 방문을 환영합니다.</h1>"

@app.route('/memberlist/')
def memberlist():
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM member"
    cur.execute(sql)
    rs = cur.fetchall() #db에서 검색한 테이터
    conn.close()
    return render_template('memberlist.html', rs=rs)

@app.route('/member_view/<string:id>/')
def member_view(id):    #mid를 경로로 설정하고 매개변수로 넘겨준다.
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM member WHERE mid='%s'" % (id)
    cur.execute(sql)
    rs = cur.fetchall()     #해당 1개의 자료를 반환받음
    #목록을 불러올때는 fetchall()을 사용한다.
    #목록을 1개씩 받아올때는 fetchone()을 사용한다.
    conn.close()
    return render_template('member_view.html', rs=rs)

app.run(debug=True)
