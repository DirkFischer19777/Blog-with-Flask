from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# File with blog posts
DATA_FILE = "posts.json"

def load_posts():
    """
    Load all blog posts from the JSON file.

    Returns:
        list: A list of blog post dictionaries.
              Returns an empty list if the file is missing or invalid.
    """
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # If the file doesn't exist, return an empty list
        return []
    except json.JSONDecodeError:
        # If the file is corrupted or empty, also return an empty list
        return []
    except Exception as e:
        # Catch-all for unexpected errors (logging would be better in production)
        print(f"Error loading posts: {e}")
        return []


def save_posts(posts):
    """
    Save a list of blog posts to the JSON file.

    Args:
        posts (list): List of dictionaries containing blog post data.
    """
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(posts, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving posts: {e}")


@app.route('/')
def index():
    """
    Home page: Display all blog posts.

    Returns:
        Rendered HTML page with all existing blog posts.
    """
    posts = load_posts()
    return render_template("index.html", posts=posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Route for adding a new blog post.

    GET:
        Render a form for entering a new blog post.
    POST:
        Read form data (author, title, content),
        create a new blog post, save it to the JSON file,
        and redirect to the home page.

    Returns:
        Rendered HTML form (GET) or redirect to home page (POST).
    """
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        posts = load_posts()
        new_id = max([post["id"] for post in posts], default=0) + 1

        new_post = {
            "id": new_id,
            "author": author,
            "title": title,
            "content": content
        }
        posts.append(new_post)
        save_posts(posts)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """
    Route for deleting a blog post.

    Args:
        post_id (int): The ID of the blog post to delete.

    Returns:
        Redirect to the home page after deletion.
    """
    posts = load_posts()
    posts = [post for post in posts if post["id"] != post_id]
    save_posts(posts)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    Route for updating an existing blog post.

    Args:
        post_id (int): The ID of the blog post to update.

    GET:
        Render a form pre-filled with the current blog post data.
    POST:
        Update the blog post with new form data and save it.

    Returns:
        Rendered HTML form (GET) or redirect to home page (POST).
    """
    posts = load_posts()
    post = next((p for p in posts if p["id"] == post_id), None)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        post['author'] = request.form.get('author')
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')

        save_posts(posts)
        return redirect(url_for('index'))

    return render_template('update.html', post=post)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

