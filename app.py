from flask import Flask, render_template, request, redirect, url_for
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

# Neue Route zum Hinzufügen eines Posts
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Formular-Daten auslesen
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        # Neue ID generieren
        posts = load_posts()
        new_id = max([post["id"] for post in posts], default=0) + 1

        # Neuen Blogpost erstellen
        new_post = {
            "id": new_id,
            "author": author,
            "title": title,
            "content": content
        }
        posts.append(new_post)
        save_posts(posts)

        return redirect(url_for('index'))

    # GET-Anfrage -> Formular anzeigen
    return render_template('add.html')

# Neue Route zum Löschen eines Blogposts
@app.route('/delete/<int:post_id>')
def delete(post_id):
    posts = load_posts()
    # Blogpost mit gegebener ID entfernen
    posts = [post for post in posts if post["id"] != post_id]
    save_posts(posts)
    return redirect(url_for('index'))

# Neue Route zum updaten eines Blogposts
@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    posts = load_posts()
    # Post nach ID finden
    post = next((p for p in posts if p["id"] == post_id), None)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        # Formular-Daten auslesen
        post['author'] = request.form.get('author')
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')

        # Änderungen speichern
        save_posts(posts)
        return redirect(url_for('index'))

    # GET-Anfrage -> Formular mit aktuellen Daten anzeigen
    return render_template('update.html', post=post)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
