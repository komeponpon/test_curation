from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

# データベースから記事を取得する関数
def get_articles():
    conn = sqlite3.connect('data/articles.db')
    cursor = conn.cursor()
    cursor.execute('SELECT title, link, thumbnail, source FROM articles')
    articles = cursor.fetchall()
    conn.close()
    return articles

# 記事一覧ページ
@app.route('/')
def index():
    articles = get_articles()
    return render_template('index.html', articles=articles)

# サーバー起動
if __name__ == '__main__':
    app.run(debug=True)
