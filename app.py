from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "cokGizliBirAnahtar")  # Değiştir!

# Giriş için kullanıcı adı ve şifre
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "123456"

@app.route("/", methods=["GET", "POST"])
def login():
    if session.get("logged_in"):
        return redirect(url_for("panel"))
    message = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("panel"))
        else:
            message = "Kullanıcı adı veya şifre hatalı!"
    return render_template("login.html", message=message)

@app.route("/panel")
def panel():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("panel.html")

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
