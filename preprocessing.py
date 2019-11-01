import pandas as pd
from janome.tokenizer import Tokenizer
from collections import Counter, defaultdict


def read_txt_data():
    csv = "./csv/txt_data.csv"
    df = pd.read_csv(csv)

    ids = df['id']
    dates = df['date']
    texts = df['text']

    return ids, dates, texts


def read_exclude_words():  # 除外するワード
    csv = "./csv/exclude_words.csv"
    df = pd.read_csv(csv)

    exclude_words = df['exclude_words'].reset_index()['index'].tolist()
    return exclude_words


def do_exclude(texts, exclude_words):
    print("Starting exclude specific keywords...")
    articles = []
    for article in texts:
        for exclude in exclude_words:
            article = article.replace(exclude, '')
        article.strip()
        articles.append(article)
    return articles


def counter(article):
    print("Starting explode to vocabulary...")
    t = Tokenizer()
    words_count = defaultdict(int)
    words = ""
    tokens = t.tokenize(article)
    for token in tokens:
        pos = token.part_of_speech.split(',')[0]
        if pos == '名詞':
            words_count[token.base_form] += 1
            words += token.base_form
            words += ","
    return words_count, words


# 出てきた単語を記事ごとに保存
def write_words(_id, date, words):
    csv_file = 'csv/words.csv'
    df = pd.read_csv(csv_file)

    storaged_article_id = df['id'].reset_index()['index'].tolist()
    # print(storaged_article_id)
    if _id in storaged_article_id:
        print("This article has storaged(id: %d)" % _id)
    else:
        results = pd.DataFrame([[_id, date, words]], columns=[
            'id', 'date', 'words'])

        df = pd.concat([df, results])
        df.to_csv(csv_file, index=False)
        print("success writing to %s" % csv_file)


def write_words_count(_id, date, voc_arr, count_arr):
    csv_file = 'csv/words_count.csv'
    df = pd.read_csv(csv_file)

    storaged_article_id = df['id'].reset_index()['index'].tolist()
    # print(storaged_article_id)
    if _id in storaged_article_id:
        print("This article has storaged(id: %d)" % _id)
    else:
        for i in range(len(voc_arr)):
            results = pd.DataFrame([[_id, date, voc_arr[i], count_arr[i]]], columns=[
                'id', 'date', 'word', 'count'])

        df = pd.concat([df, results])
        df.to_csv(csv_file, index=False)
        print("success writing to %s" % csv_file)


def create_array(_id, dates, articles):
    for i, article in enumerate(articles):
        words_count, words = counter(article)
        voc_arr = list(words_count.keys())
        count_arr = list(words_count.values())
        # csv書き出し
        write_words(_id[i], dates[i], words)
        write_words_count(_id[i], dates[i], voc_arr, count_arr)


def start():
    print("Preprocessing process start")
    ids, dates, texts = read_txt_data()
    exclude_words = read_exclude_words()
    articles = do_exclude(texts, exclude_words)
    create_array(ids, dates, articles)


start()


# texts = ' '.join(words)
# fpath = "./font/NotoSansCJKjp-Regular.otf"
# wordcloud = WordCloud(font_path=fpath, width=480, height=320)

# print("Generating wordcloud...")
# wordcloud.generate(texts)
# wordcloud.to_file('./img/wordcloud.png')
# print("Successfully generate wordcloud png image!")
