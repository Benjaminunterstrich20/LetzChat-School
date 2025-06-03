from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Upload-Ordner konfigurieren
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
        image = request.files.get("image")

        image_url = None
        if image and image.filename:
            filename = secure_filename(image.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(filepath)
            image_url = url_for('uploaded_file', filename=filename)

        if message or image_url:
            chat_rooms[room_code].append({
                "name": name,
                "message": message,
                "image": image_url,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        return redirect(url_for("chat_room", room_code=room_code))

    messages = chat_rooms[room_code]
    return render_template("chat.html", messages=messages, room_code=room_code)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True)
    
