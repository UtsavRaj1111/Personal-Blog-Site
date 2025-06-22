from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

# In-memory storage for blog posts
posts = []

# HTML Template (single file)
template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Blog</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #FFDAB9; font-family: 'Segoe UI', sans-serif; }
        .navbar { background-color: #1f2937; }
        .navbar-brand, .nav-link, .btn { color: white !important; }
        .card { margin-bottom: 20px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .btn-primary { background-color: #2563eb; border-color: #2563eb; }
        .btn-primary:hover { background-color: #1d4ed8; border-color: #1d4ed8; }
    </style>
</head>
<body>
<nav class="navbar navbar-expand-lg">
    <div class="container">
        <a class="navbar-brand" href="/">My Blog</a>
        <a href="/new" class="btn btn-success">+ New Post</a>
    </div>
</nav>

<div class="container mt-4">
    {% if page == 'index' %}
        <h2 class="mb-4">Recent Posts</h2>
        {% for post in posts %}
            <div class="card p-3">
                <h5>{{ post['title'] }}</h5>
                <p>{{ post['content'][:150] }}...</p>
                <a href="/post/{{ loop.index0 }}" class="btn btn-primary">Read More</a>
            </div>
        {% else %}
            <p>No posts yet.</p>
        {% endfor %}

    {% elif page == 'new' or page == 'edit' %}
        <h2>{{ 'Edit Post' if page == 'edit' else 'New Post' }}</h2>
        <form method="POST">
            <div class="mb-3">
                <input type="text" name="title" class="form-control" placeholder="Post Title" value="{{ post.title if post else '' }}" required>
            </div>
            <div class="mb-3">
                <textarea name="content" rows="8" class="form-control" placeholder="Post Content" required>{{ post.content if post else '' }}</textarea>
            </div>
            <button type="submit" class="btn btn-primary">Save Post</button>
            <a href="/" class="btn btn-secondary">Cancel</a>
        </form>

    {% elif page == 'post' %}
        <div class="card p-4">
            <h2>{{ post['title'] }}</h2>
            <p>{{ post['content'] }}</p>
            <a href="/edit/{{ post_id }}" class="btn btn-warning">Edit</a>
            <a href="/delete/{{ post_id }}" class="btn btn-danger" onclick="return confirm('Are you sure you want to delete this post?');">Delete</a>
            <a href="/" class="btn btn-secondary">Back</a>
        </div>
    {% endif %}
</div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(template, page='index', posts=posts)

@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        posts.append({'title': title, 'content': content})
        return redirect(url_for('index'))
    return render_template_string(template, page='new', post=None)

@app.route('/post/<int:post_id>')
def post_detail(post_id):
    if 0 <= post_id < len(posts):
        return render_template_string(template, page='post', post=posts[post_id], post_id=post_id)
    return "Post not found", 404

@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit(post_id):
    if 0 <= post_id < len(posts):
        if request.method == 'POST':
            posts[post_id]['title'] = request.form['title']
            posts[post_id]['content'] = request.form['content']
            return redirect(url_for('post_detail', post_id=post_id))
        return render_template_string(template, page='edit', post=posts[post_id])
    return "Post not found", 404

@app.route('/delete/<int:post_id>')
def delete(post_id):
    if 0 <= post_id < len(posts):
        posts.pop(post_id)
        return redirect(url_for('index'))
    return "Post not found", 404

if __name__ == '__main__':
    app.run(debug=True)
