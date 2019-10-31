from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import datetime

# ArchiFutureのページをスクレイピング
def scraping_archifuture_news(url):
  r = requests.get(url) # archifutreのページを開く
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
  else: return "page not found"
  
def write_data(value):
  csv_file = 'csv/txt_data.csv'
  df = pd.read_csv(csv_file)

  date = value[0]
  text = value[1]
  results = pd.DataFrame([[date, text]], columns=['date', 'text'])

  df = pd.concat([df, results])
  df.to_csv(csv_file, index=False)
  print("success writing to %s" % csv_file)
  

def start_scraping ():
  now = datetime.datetime.now()
  print("scraping start at %d:%d:%d" % (now.hour, now.minute, now.second))
  # url = "http://www.archifuture-web.jp/headline/301.html"
  # return_value = scraping_archifuture_news(url)
  # write_data(return_value)
  for i in range(458):
    url = "http://www.archifuture-web.jp/headline/%d.html" % i
    return_value = scraping_archifuture_news(url)
    if(return_value != "page not found"):
      write_data(return_value)
  now = datetime.datetime.now()
  print("scraping end at %d:%d:%d" % (now.hour, now.minute, now.second))
    
  
start_scraping()
  