from flask import Flask, render_template, request, redirect, url_for, session
import os
import requests

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "cokGizliBirAnahtar")  # Değiştir!

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

@app.route("/panel", methods=["GET", "POST"])
def panel():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    orders = None
    error = ""
    if request.method == "POST":
        client_id = request.form.get("client_id")
        client_secret = request.form.get("client_secret")
        supplier_id = request.form.get("supplier_id")
        try:
            url = f"https://api.trendyol.com/sapigw/suppliers/{supplier_id}/orders"
            headers = {
                "Authorization": f"Basic {client_id}:{client_secret}",
                "Content-Type": "application/json"
            }
            params = {"size": 5}  # Son 5 siparişi çekmek için
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                orders = response.json().get("content", [])
            else:
                error = f"API Hatası: {response.status_code} - {response.text}"
        except Exception as e:
            error = f"Hata: {e}"
    return render_template("panel.html", orders=orders, error=error)

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
