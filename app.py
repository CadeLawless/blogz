from flask import Flask, request, redirect, render_template, session
import mysql.connector
import secrets
from passlib.hash import pbkdf2_sha256

conn = mysql.connector.connect(
    host="localhost",
    database="blogz",
    user="root",
    password="millieBean0414" )

app = Flask("app")
app.config['DEBUG'] = True
app.secret_key = secrets.token_hex(16)

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'index', 'blog', 'singleUser', 'post']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/')
def index():
    users = []
    conn.reconnect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    for user in result:
        users.append(user)
    conn.close()
    return render_template('index.html', users=users)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        usernameError = ""
        passwordError = ""
        errorCount = 0
        bloggers = []
        conn.reconnect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = '{}'".format(username))
        result = cursor.fetchall()
        for user in result:
            bloggers.append(user)
        if username == "":
            usernameError = "This field needs to be filled out"
            errorCount += 1
        else:
            if len(bloggers) == 0:
                    usernameError = "Username does not exist"
                    errorCount += 1
            else:
                if password == "":
                    passwordError = "This field needs to be filled out"
                    errorCount += 1
                else:
                    for user in bloggers:
                        if pbkdf2_sha256.verify(password, user[2]) == False:
                            passwordError = "Incorrect password"
                            errorCount += 1
        if errorCount > 0:
            return render_template("login.html", username=username, password=password, usernameError=usernameError, passwordError=passwordError)
        else:
            session['username'] = username
            return redirect("/newpost")
            conn.close()
    return render_template('login.html')

@app.route('/blog')
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

@app.route('/post', methods=['GET'])
def post():
    id = request.args.get("id")
    conn.reconnect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts WHERE id = '{}'".format(id))
    result = cursor.fetchall()
    for post in result:
        entry = post
    conn.close()
    return render_template('post.html', entry=entry)

@app.route("/singleUser/",  methods=['GET'])
def singleUser():
    posts = []
    user = request.args.get("user")
    conn.reconnect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts WHERE user = '{}'".format(user))
    result = cursor.fetchall()
    for post in result:
        posts.append(post)
    conn.close()
    return render_template('singleUser.html', posts=posts, user= user)

@app.route("/newpost/",  methods=['POST', 'GET'])
def newpost():
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
            title, content, user)
            VALUES ("{}", "{}", "{}")""".format(title, post, session['username'])
            conn.reconnect()
            cursor = conn.cursor()
            cursor.execute(sql)

            conn.commit()
            
            return redirect("/post?id={}".format(cursor.lastrowid))
            conn.close()
    return render_template('newpost.html')

@app.route("/signup",  methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        passwordConfirm = request.form['passwordConfirm']
        usernameError = ""
        passwordError = ""
        passwordConfirmError = ""
        errorCount = 0
        bloggers = []
        conn.reconnect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        result = cursor.fetchall()
        for user in result:
            bloggers.append(user)
        if username == "":
            usernameError = "This field needs to be filled out"
            errorCount += 1
        else:
            if len(username) < 3:
                usernameError = "Username needs to be at least 3 characters long"
                errorCount += 1
            else:
                for user in bloggers:
                    if user[1] == username:
                        usernameError = "The username already exists. Pick another one."
                        errorCount += 1
        if password == "":
            passwordError = "This field needs to be filled out"
            errorCount += 1
        else:
            if len(password) < 3:
                passwordError = "Password needs to be at least 3 characters long"
                errorCount += 1
            else:
                if password != passwordConfirm:
                    passwordError = "Passwords do not match"
                    errorCount += 1
        if passwordConfirm == "":
            passwordConfirmError = "This field needs to be filled out"
            errorCount += 1          
        if errorCount > 0:
            return render_template("signup.html", username=username, password=password, passwordConfirm=passwordConfirm, usernameError=usernameError, passwordError=passwordError, passwordConfirmError=passwordConfirmError)
        else:
            password = pbkdf2_sha256.hash(password)
            sql = """INSERT INTO users(
            username, pass)
            VALUES ('{}', '{}')""".format(username, password)
            conn.reconnect()
            cursor = conn.cursor()
            cursor.execute(sql)

            conn.commit()
            
            session["username"] = username
            return redirect("/newpost")
            conn.close()
    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')
