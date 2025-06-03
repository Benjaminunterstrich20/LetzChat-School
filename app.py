from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# In-Memory-Speicher für Nachrichten pro Raum
chat_rooms = {}

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        room_code = request.form.get("room")
        return redirect(url_for("chat_room", room_code=room_code))
    return render_template("home.html")

@app.route("/chat/<room_code>", methods=["GET", "POST"])
def chat_room(room_code):
    if room_code not in chat_rooms:
        chat_rooms[room_code] = []

    if request.method == "POST":
        name = request.form.get("name") or "Ghost"
        message = request.form.get("message")
        if message:
            chat_rooms[room_code].append({
                "name": name,
                "message": message,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        return redirect(url_for("chat_room", room_code=room_code))

    messages = chat_rooms[room_code]
    return render_template("chat.html", messages=messages, room_code=room_code)

if __name__ == "__main__":
    app.run(debug=True)
