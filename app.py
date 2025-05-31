from flask import Flask, render_template, request, redirect, url_for, session
import os
import requests

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "cokGizliBirAnahtar")

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
        token = request.form.get("token", "").strip()
        supplier_id = request.form.get("supplier_id", "").strip()
        access_token = None

        if token:  # Eğer elle token girilmişse onu kullan
            access_token = token
        else:
            # Client ID/Secret ile token almaya çalış
            client_id = request.form.get("client_id", "").strip()
            client_secret = request.form.get("client_secret", "").strip()
            token_url = "https://api.trendyol.com/sapigw/token"
            payload = {
                "client_id": client_id,
                "client_secret": client_secret,
                "grant_type": "client_credentials"
            }
            headers = {
                "Content-Type": "application/x-www-form-urlencoded"
            }
            try:
                token_response = requests.post(token_url, data=payload, headers=headers, timeout=20)
                if token_response.status_code == 200:
                    access_token = token_response.json().get("access_token")
                    if not access_token:
                        error = "Token alınamadı. Yanıt: " + str(token_response.json())
                        return render_template("panel.html", orders=orders, error=error)
                else:
                    error = f"Token alınamadı: {token_response.status_code} - {token_response.text}"
                    return render_template("panel.html", orders=orders, error=error)
            except Exception as e:
                error = f"Token isteğinde hata oluştu: {e}"
                return render_template("panel.html", orders=orders, error=error)

        # Token ile sipariş çek
        try:
            orders_url = f"https://api.trendyol.com/sapigw/suppliers/{supplier_id}/orders"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            params = {"size": 5}
            orders_response = requests.get(orders_url, headers=headers, params=params, timeout=20)
            if orders_response.status_code == 200:
                orders = orders_response.json().get("content", [])
            else:
                error = f"Sipariş çekilemedi: {orders_response.status_code} - {orders_response.text}"
        except Exception as e:
            error = f"Hata: {e}"
    return render_template("panel.html", orders=orders, error=error)

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
