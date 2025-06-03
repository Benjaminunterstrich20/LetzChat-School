from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# In-Memory-Speicher für Nachrichten
messages = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name") or "Ghost"
        message = request.form.get("message")
        if message:
            messages.append({
                "name": name,
                "message": message,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        return redirect(url_for("index"))
    return render_template("chat.html", messages=messages)

if __name__ == "__main__":
    app.run(debug=True)
