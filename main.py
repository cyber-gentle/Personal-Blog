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
        storage.save_article(new_article, len(articles))
        return flask.redirect(flask.url_for('admin'))
        

        


if __name__ == "__main__":
    app.run(debug=True)
