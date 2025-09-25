from flask import Flask, render_template
import json

app = Flask(__name__)

# Datei mit den Blogposts
DATA_FILE = "posts.json"

# Hilfsfunktion: JSON-Datei laden
def load_posts():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# Hilfsfunktion: JSON-Datei speichern
def save_posts(posts):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=4, ensure_ascii=False)

@app.route('/')
def index():
    posts = load_posts()  # Beiträge laden
    return render_template("index.html", posts=posts)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
