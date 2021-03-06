import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "kimjinhe" #암호키 설정

def getconn():
    conn = sqlite3.connect('./memberdb.db')
    return conn

@app.route('/') #url경로
def index():
    return render_template('index.html')

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
    rs = cur.fetchone()     #해당 1개의 자료를 반환받음
    #목록을 불러올때는 fetchall()을 사용한다.
    #목록을 1개씩 받아올때는 fetchone()을 사용한다.
    conn.close()
    return render_template('member_view.html', rs=rs)

@app.route('/register/', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        #자료 수집
        id = request.form['mid']
        pwd = request.form['passwd']
        name = request.form['name']
        age = request.form['age']

        # 회원 가입
        conn = getconn()
        cur = conn.cursor()
        sql = "INSERT INTO member(mid, passwd, name, age) VALUES ('%s','%s','%s', %s)"\
            % (id, pwd, name, age)  # 문자 = '%s', 숫자 = %s
        cur.execute(sql)    # 실행 함수
        conn.commit()       # 커밋 완료
        # 가입 후 자동 로그인
        sql = "SELECT * FROM member WHERE mid='%s'" % (id)
        cur.execute(sql)
        rs=cur.fetchone()
        conn.close()
        if rs:
            session['userID'] = rs[0] # 자동 로그인 - session 필수, session - 가입,로그인시 만듦
            session['userName'] = rs[2] # 자동 로그인 - session 필수, session - 가입,로그인시 만듦
        return redirect(url_for('memberlist'))
    else:
        return render_template('register.html')

@app.route('/login/', methods=['GET','POST'])
def login():
    if request.method == 'POST':    #POST는 반드시 대문자로!!
        #자료 전달 받음
        id = request.form['mid']
        pwd = request.form['passwd']

        conn = getconn()
        cur = conn.cursor()
        sql = "SELECT * FROM member WHERE mid = '%s' AND passwd ='%s'"%(id, pwd)
        cur.execute(sql)
        rs = cur.fetchone()     # db에서 찾은 데이터 가져옴
        conn.close()
        if rs:
            session['userID'] = rs[0]
            session['userName'] = rs[2]
            return redirect(url_for('index'))
        else:
            error = "아이디나 비밀번호가 일치하지 않습니다."
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')

@app.route('/logout/')
def logout():
    # session.pop("userID")   #id 세션 삭제
    session.clear()     # 전체 세션 삭제
    return redirect(url_for('index'))

@app.route('/member_del/<string:id>/')   #삭제 url 생성
def member_del(id):   #mid를 매개변수로 넘겨줌
    conn = getconn()
    cur = conn.cursor()
    sql = "DELETE FROM member WHERE mid='%s'" % (id)
    cur.execute(sql)    # 삭제 실행
    conn.commit()
    conn.close()
    return redirect(url_for('memberlist'))

@app.route('/member_edit/<string:id>/', methods=['GET','POST'])  # 삭제 url 생성
def member_edit(id):
    if request.method == "POST":
        # 회원 자료 가져오기
        # 자료 수집
        id = request.form['mid']
        pwd = request.form['passwd']
        name = request.form['name']
        age = request.form['age']

        #db 연결
        conn = getconn()
        cur = conn.cursor()
        sql = "UPDATE member SET passwd='%s', name='%s', age='%s'"\
            "WHERE mid= '%s'" % (pwd, name, age, id)
        cur.execute(sql)  # 실행 함수
        conn.commit()   # 커밋 완료
        conn.close()
        return redirect(url_for('member_view', id=id))
    else:
        conn = getconn()
        cur = conn.cursor()
        sql = "SELECT * FROM member WHERE mid = '%s'" % (id)
        cur.execute(sql)
        rs = cur.fetchone()  # db에서 찾은 데이터 가져옴
        conn.close()
        return render_template('member_edit.html', rs=rs)

@app.route('/boardlist/')
def boardlist():
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM board ORDER BY bno DESC"
    cur.execute(sql)
    rs = cur.fetchall()
    conn.close()
    return render_template('boardlist.html', rs=rs)

@app.route('/writing/', methods = ['GET','POST'])
def writing():
    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        hit = 0
        mid = session.get('userName')
        conn = getconn()
        cur = conn.cursor()
        sql = "INSERT INTO board(title, content, hit, mid) VALUES ('%s','%s','%s','%s')" \
              % (title, content, hit, mid)
        cur.execute(sql)
        conn.commit()
        conn.close()
        return redirect(url_for('boardlist'))
    else:
        return render_template('writing.html')

# 게시글 보기
@app.route('/board_view/<int:bno>/')
def board_view(bno):
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM board WHERE bno = %s" % (bno)
    cur.execute(sql)
    rs = cur.fetchone()
    # 조회수 1 증가
    hit = rs[4] #hit = 0
    hit = hit + 1
    sql = "UPDATE board SET hit = %s WHERE bno = %s" % (hit, bno)
    cur.execute(sql)
    conn.commit()
    conn.close()
    return render_template('board_view.html', rs=rs)

# 게시글 삭제
@app.route('/board_del/<int:bno>')
def board_del(bno):
    conn = getconn()
    cur = conn.cursor()
    sql = "DELETE FROM board WHERE bno = %s" % (bno)
    cur.execute(sql)
    conn.commit()
    conn.close()
    return redirect(url_for('boardlist'))

#게시글 수정
@app.route('/board_edit/<int:bno>/', methods=['GET','POST'])
def board_edit(bno):
    if request.method == 'POST':
        #자료 전달
        title = request.form['title']
        content = request.form['content']
        mid = session.get('userNamw') #자동으로 session입력
        #db update
        conn = getconn()
        cur = conn.cursor()
        sql = "UPDATE board SET title='%s', content='%s', mid='%s' WHERE bno= %s" % (title, content, mid, bno)
        cur.execute(sql)  # 실행 함수
        conn.commit()  # 커밋 완료
        conn.close()
        return redirect(url_for('board_view', bno=bno))
    else:
        conn = getconn()
        cur = conn.cursor()
        sql = "SELECT * FROM board WHERE bno = %s" % (bno)
        cur.execute(sql)
        rs = cur.fetchone()
        conn.close()
    return render_template('board_edit.html', rs=rs)

app.run(debug=True)
