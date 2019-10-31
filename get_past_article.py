from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import datetime

# ArchiFutureのページをスクレイピング

# initial_scraping()


def scraping_archifuture_news(url):
    r = requests.get(url)  # archifutreのページを開く
    soup = bs(r.text, 'html.parser')  # beautifulsoupでhtmlを取得
    ptags = soup.select('p')
    if len(ptags) > 2:
        print("scraping start on url: %s" % url)
        date = soup.select('.page-data')[0].string
        text = ptags[2].get_text()
        lines = [line.strip() for line in text.splitlines()]  # タグを排して文字だけ取得
        ten_lines_news = lines[0:10]  # 不要部分の削除

        # 1行のテキストに変換
        ten_lines_news_text = ""
        for line in ten_lines_news:
            ten_lines_news_text += line

        return date, ten_lines_news_text
    else:
        return "page not found"


# csvファイルに追加
def write_data(id, value):
    csv_file = 'csv/txt_data.csv'
    df = pd.read_csv(csv_file)

    date = value[0]
    text = value[1]
    results = pd.DataFrame([[id, date, text]], columns=['id', 'date', 'text'])

    df = pd.concat([df, results])
    df.to_csv(csv_file, index=False)
    print("success writing to %s" % csv_file)


def start_scraping(id, first_scraping=False):
    # 実行開始時のメッセージ
    now = datetime.datetime.now()
    print("scraping start at %d:%d:%d" % (now.hour, now.minute, now.second))

    article_num = 0 # 記事に振られている番号
    scraping_iteration = 0  # 繰り返し処理の回数
    added_article = 0 # 追加された記事の数
    
    if first_scraping == True:
        scraping_iteration = id + 1
    else:
        article_num = id + 1
        scraping_iteration = 10
        
    for i in range(scraping_iteration):
        url = "http://www.archifuture-web.jp/headline/%d.html" % article_num
        return_value = scraping_archifuture_news(url)
        if(return_value != "page not found"):
            write_data(id, return_value)
            added_article += 1
        article_num += 1

    # 実行終了時のメッセージ
    now = datetime.datetime.now()
    print("scraping end at %d:%d:%d" % (now.hour, now.minute, now.second))
    if(added_article < 2):
        print("RESULT: this time added %d article" % added_article)
    else:
        print("RESULT: this time added %d articles" % added_article)
        

def check_data():
    csv_file = 'csv/txt_data.csv'
    df = pd.read_csv(csv_file)
    if len(df) < 1:
        latest_post_id = 458    # 最新の記事のURLから記事番号を確認して入力
        start_scraping(latest_post_id, True)
    else:
        last_article = df.tail(1)
        last_article_id = last_article['id']
        start_scraping(last_article_id)
        


# if __name__ = "__main__":
check_data()
# initial_scraping()
