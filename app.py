from flask import Flask, request, redirect, render_template, url_for
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    database="blogs",
    user="root",
    password="millieBean0414" )

app = Flask("app")
app.config['DEBUG'] = True

@app.route('/')
def blog():
    posts = []
    titles = []
    conn.reconnect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM blogs")
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
    cursor.execute("SELECT * FROM blogs WHERE ID = '{}'".format(id))
    result = cursor.fetchall()
    for post in result:
        entry = post
    conn.close()
    return render_template('post.html', entry=entry)

@app.route("/newpost/")
def newpost():
    return render_template("newpost.html")

@app.route("/",  methods=['POST', 'GET'])
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
            sql = """INSERT INTO blogs(
            title, post)
            VALUES ('{}', '{}')""".format(title, post)
            conn.reconnect()
            cursor = conn.cursor()
            cursor.execute(sql)

            conn.commit()
            
            return redirect("/post/?id={}".format(cursor.lastrowid))
            conn.close()
