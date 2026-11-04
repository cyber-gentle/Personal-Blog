import flask, datetime, os
import storage.storage as storage

app = flask.Flask(__name__)
app.secret_key = 'Hello'
articles, errors = storage.load_articles()

@app.route("/", methods=["GET"])
def home():
    return flask.render_template("index.html", articles=articles)



@app.route("/article/<article_id>", methods=["GET"])
def article_detail(article_id: str):
    return flask.render_template('article.html', article=articles.get(int(article_id), ""))


@app.route('/admin', methods=["GET", "POST"])
def admin():
    auth = flask.request.authorization
    if auth and auth.username == "Admin" and auth.password == "Login":
        return flask.render_template("admin.html", articles=articles)
    
    if flask.request.method == "GET":
        return flask.make_response("<h1>ACCESS DENIED</h1>", 401, {'WWW-Authenticate': 'Basic realm="Admin Login required"'})


@app.route("/new", methods=["GET", "POST"])
def new_article():
    new_article = {}
    if flask.request.method == "GET":
        return flask.render_template("new_article.html")
    if flask.request.method == "POST":
        new_article['title'] = flask.request.form["article_title"]
        new_article['date_posted'] = flask.request.form["publish_date"]
        new_article['content'] = flask.request.form["article_content"]
        articles[len(articles) + 1] = new_article
        storage.save_articles(articles)
        return flask.redirect(flask.url_for('admin')) 
        
@app.route("/edit/<article_id>", methods=["GET", "POST"])
def edit_article(article_id: str):
    updated = articles.get(int(article_id), "")
    if flask.request.method == "GET":
        return flask.render_template('edit_article.html', article_details=articles.get(int(article_id), ""))
    if flask.request.method == "POST":
        updated['title'] = flask.request.form.get("article_title", updated.get('title', ''))
        updated['last_update_date'] = flask.request.form.get("updated_date", updated.get('date_posted', ''))
        updated['content'] = flask.request.form.get("article_content", updated.get('content', ''))
        storage.save_articles(articles)
        return flask.redirect(flask.url_for('admin'))

@app.route("/delete/<article_id>", methods=["GET"])
def delete_article(article_id: str):
    article_key = int(article_id)
    if article_key in articles:
        file_path = os.path.join(os.path.dirname(__file__), "storage", "data", f"article_{article_key:03d}.json")
        if os.path.exists(file_path):
            os.remove(file_path)
        del articles[article_key]
        storage.save_articles(articles)
    return flask.redirect(flask.url_for('admin'))


if __name__ == "__main__":
    app.run(debug=True)
