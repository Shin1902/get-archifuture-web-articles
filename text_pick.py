import pandas as pd

<<<<<<< HEAD
csv = '../csv/txt_data.csv'
=======
csv = 'csv/txt_data.csv'
>>>>>>> origin/master
df = pd.read_csv(csv)

# print(df['text'])
text = df['text']

string = ""
for article in text:
  string += article
  
print(string)
