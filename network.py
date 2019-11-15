import networkx as nx
import matplotlib.pyplot as plt
# import search_console_classifier_utils as utils
import pandas as pd


def read_words():
    csv = "./csv/words.csv"
    df = pd.read_csv(csv)

    words = df['words']

    return words


words = read_words()
print(words)
