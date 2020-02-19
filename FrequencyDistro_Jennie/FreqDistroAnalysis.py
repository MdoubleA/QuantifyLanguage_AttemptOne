import os
from pathlib import Path
import nltk
import shutil
import csv
from nltk.corpus import stopwords
from enum import Enum


all_files = [
    'most_freq_words.csv',
    'most_freq_words_non_sarc.csv',
    'most_freq_words_sarc.csv',
]

both = 0
nonsarcastic = 1
sarcastic = 2


def get_csv(the_file):
    with open(the_file, newline='') as the_csv_file:
        the_csv_file = list(csv.reader(the_csv_file, delimiter=','))[1:]  # Remove header.
    return the_csv_file


all_words = [word[0] for word in get_csv(all_files[both])]
nonsarcastic_words = [word[0] for word in get_csv(all_files[nonsarcastic])]
sarcastic_words = [word[0] for word in get_csv(all_files[sarcastic])]

common_words = [x for x in nonsarcastic_words if x in sarcastic_words]
not_common_words = [x for x in nonsarcastic_words if x not in sarcastic_words]

print("Total number of words: " + str(len(all_words)))
print("Number of words shared between subsets: " + str(len(common_words)))
print("Number of words not shared between subsets: " + str(len(not_common_words)))
print("\n")
print("Number of words shared between set and nonsarcastic set: " + str(len([x for x in all_words if x in nonsarcastic_words])))
print("Number of words not shared between set and nonsarcastic set: " + str(len([x for x in all_words if x not in nonsarcastic_words])))
print("\n")
print("Number of words shared between set and sarcastic set: " + str(len([x for x in all_words if x in sarcastic_words])))
print("Number of words not shared between set and sarcastic set: " + str(len([x for x in all_words if x not in sarcastic_words])))
