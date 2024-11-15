import feedparser
import sqlite3

# RSSフィードから記事情報を取得する関数
def fetch_articles(feed_url):
    feed = feedparser.parse(feed_url)
    articles = []

    for entry in feed.entries:
        title = entry.title
        link = entry.link
        thumbnail = entry.media_thumbnail[0]['url'] if 'media_thumbnail' in entry else None
        source = feed.feed.title  # フィード元の名前

        articles.append({
            'title': title,
            'link': link,
            'thumbnail': thumbnail,
            'source': source
        })

    return articles

# 記事情報をデータベースに保存する関数
def save_articles(articles):
    conn = sqlite3.connect('data/articles.db')  # データベースファイルのパスを指定
    cursor = conn.cursor()

    # テーブルが存在しない場合は作成
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            link TEXT,
            thumbnail TEXT,
            source TEXT
        )
    ''')

    for article in articles:
        cursor.execute('''
            INSERT INTO articles (title, link, thumbnail, source)
            VALUES (?, ?, ?, ?)
        ''', (article['title'], article['link'], article['thumbnail'], article['source']))

    conn.commit()
    conn.close()

# RSSフィードURLのリスト
feed_urls = [
    "https://rss.itmedia.co.jp/rss/2.0/smartjapan.xml" # SmartJapan
    "https://xtech.nikkei.com/rss/xtech-ene.rdf",  # 日経クロステック(エネルギー)
]

# 各フィードURLから記事を取得し、データベースに保存
for feed_url in feed_urls:
    articles = fetch_articles(feed_url)
    save_articles(articles)
