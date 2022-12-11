from flask import Flask, request, redirect, render_template, url_for, session
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    database="blogz",
    user="root",
    password="millieBean0414" )

app = Flask("app")
app.config['DEBUG'] = True

@app.route('/')
def login():
    return render_template("login.html")

@app.route('/index/')
def index():
    users = []
    conn.reconnect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    for users in result:
        users.append(users)
    conn.close()
    return render_template('index.html', users=users)

@app.route('/blog/')
def blog():
    posts = []
    conn.reconnect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts")
    result = cursor.fetchall()
    for entry in result:
        posts.append(entry)
    conn.close()
    return render_template('blog.html', posts=posts)

@app.route("/post/",  methods=['GET'])
def post():
    id = request.args.get("id")
    conn.reconnect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts WHERE ID = '{}'".format(id))
    result = cursor.fetchall()
    for post in result:
        entry = post
    conn.close()
    return render_template('post.html', entry=entry)

@app.route("/singleUser/",  methods=['GET'])
def post():
    id = request.args.get("id")
    conn.reconnect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts WHERE user = '{}'".format(id))
    result = cursor.fetchall()
    for post in result:
        entry = post
    conn.close()
    return render_template('singleUser.html', entry=entry)

@app.route("/newpost/")
def newpost():
    return render_template("newpost.html")

@app.route("/newpost/",  methods=['POST', 'GET'])
def checkTitle():
    if request.method == 'POST':
        title = request.form['title']
        post = request.form['post']
        titleError = ""
        postError = ""
        errorCount = 0
        if title == "":
            titleError = "Your post needs to have a title"
            errorCount += 1
        elif post == "":
            postError = "Your post needs to have content"
            errorCount += 1
        if errorCount > 0:
            return render_template("newpost.html", post=post, title=title, titleError=titleError, postError=postError)
        else:
            posts = []
            sql = """INSERT INTO posts(
            title, post)
            VALUES ('{}', '{}')""".format(title, post)
            conn.reconnect()
            cursor = conn.cursor()
            cursor.execute(sql)

            conn.commit()
            
            return redirect("/post/?id={}".format(cursor.lastrowid))
            conn.close()

@app.route("/signup/",  methods=['POST', 'GET'])
def checkSignup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        usernameError = ""
        passwordError = ""
        errorCount = 0
        if username == "":
            titleError = "This field needs to be filled out"
            errorCount += 1
        elif password == "":
            postError = "This field needs to be filled out"
            errorCount += 1
        if errorCount > 0:
            return render_template("newpost.html", post=post, title=title, titleError=titleError, postError=postError)
        else:
            posts = []
            sql = """INSERT INTO posts(
            title, post)
            VALUES ('{}', '{}')""".format(title, post)
            conn.reconnect()
            cursor = conn.cursor()
            cursor.execute(sql)

            conn.commit()
            
            return redirect("/post/?id={}".format(cursor.lastrowid))
            conn.close()
