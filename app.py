from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from logger import action, debug, critical
import data.SQLHandler as sql



action("SERVER", "Server session started.", True)


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
	return render_template("index.html",title = "Homepage")

recent_entries = [
]


@app.route("/inv")
def inventory():
	return render_template("inv.html", recent = recent_entries)

@app.route("/reg")
def reg():
	return render_template("cheapregister.html",title = "Reg!")


@app.route("/register", methods=["POST"])
def register():
	name = request.form.get("name")
	email = request.form.get("email")
	hash = request.form.get("hash")
	session['User'] = sql.User(email,hash)
	session['User'].register(str(name),str(email),str(hash))
	return redirect("/")

@app.route("/zuck")
def zuck():
	return render_template("zuck.html")

@app.route("/login", methods = ["POST"])
def login():
	email = request.form.get("email")
	hash = request.form.get("hash")
	session['User'] = sql.User(email,hash)
	session['User'].login()
	return redirect("/")

@app.route("/debug")
def debug():
	return render_template("debugUser.html", title="UserDebug", cls = session['User'])


@app.errorhandler(404)
def page_not_found(e):
	return render_template("error.html",error_code="404")

@app.errorhandler	(500)
def page_oop(e):
	return render_template("error.html", error_code="500")
