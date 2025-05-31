from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "<h2>Hoş geldin! Trendyol Satıcı Paneline Başlangıç</h2><p>Başarıyla deploy edildi 🎉</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
