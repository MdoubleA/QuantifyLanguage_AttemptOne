import os
from pathlib import Path
import nltk
import shutil
import csv
from nltk.corpus import stopwords


the_file = 'most_freq_words.csv'

with open(the_file, newline='') as the_csv_file:
    the_csv_file = list(csv.reader(the_csv_file, delimiter=','))[1:]  # Remove header.
    raw_count = sum([1 for row in the_csv_file])
    stop_words = set(stopwords.words('english'))
    stop_word_count = sum([1 for row in the_csv_file if row[0] not in stop_words])
    print("Raw count: " + str(raw_count))
    print("stop word count: " + str(stop_word_count))
