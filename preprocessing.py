import pandas as pd
from janome.tokenizer import Tokenizer
from collections import Counter, defaultdict
from wordcloud import WordCloud
import matplotlib.pyplot as plt


csv = "./csv/txt_data.csv"
df = pd.read_csv(csv)

# print(df.tail())

text = df['text']
# print(text[447])

# 除外するワード
exclude_words = [
    '#',
    '\!',
    '\(.*',
    '.*\)',
    '\*',
    '\n',
    '\$.*',
    '`.*`',
    'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+',
    '@.* ',
    '@さんから',
    '【',
    '】',
    '『',
    '』',
    '「',
    '」',
    '（',
    '）',
    '〜',
    '-',
    '>',
    '|',
    ' |',
    '[a-zA-Z]',
    '\d',
    '&',
    ';',
    '/',
    '"',
    '“',
    '”',
    '\.',
    'や',
    'などの',
    '^・$',
]


def do_exclude(text):
  print("Starting exclude specific keywords...")
  articles = []
  for article in text:
      for exclude in exclude_words:
          article = article.replace(exclude, '')
      article.strip()
      articles.append(article)
  return articles

articles = do_exclude(text)
# print(len(articles))


def counter(articles):
  print("Starting explode to vocabulary...")
  t = Tokenizer()
  words_count = defaultdict(int)
  words = []
  for article in articles:
    tokens = t.tokenize(article)
    for token in tokens:
      pos = token.part_of_speech.split(',')[0]
      if pos == '名詞':
        words_count[token.base_form] += 1
        words.append(token.base_form)
  return words_count, words




words_count, words = counter(articles)
print(len(words_count))
print(words)

# print(text)
text = ' '.join(words)
fpath = "./font/NotoSansCJKjp-Regular.otf"
wordcloud = WordCloud(font_path=fpath, width=480, height=320)

print("Generating wordcloud...")
wordcloud.generate(text)
wordcloud.to_file('./img/wordcloud.png')
print("Successfully generate wordcloud png image!")
