import csv


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
num_all = len(all_words)
nonsarcastic_words = [word[0] for word in get_csv(all_files[nonsarcastic])]
num_non = len(nonsarcastic_words)
sarcastic_words = [word[0] for word in get_csv(all_files[sarcastic])]
num_sarc = len(sarcastic_words)

words_shared = lambda x, y: [z for z in x if z in y]
words_not_shared = lambda x, y: [z for z in x if z not in y]

print("Number of words in set: " + str(len(all_words)))
print("Number of words shared between subsets: " + str(len(words_shared(sarcastic_words, nonsarcastic_words))))
print("Number of words not shared between subsets: " + str(len((words_not_shared(sarcastic_words, nonsarcastic_words)))))
print("\n")
print("Number of words shared between set and nonsarcastic set: " + str(len(words_shared(all_words, nonsarcastic_words))))
print("Number of words not shared between set and nonsarcastic set: " + str(len(words_not_shared(all_words, nonsarcastic_words))))
print("\n")
print("Number of words shared between set and sarcastic set: " + str(len(words_shared(all_words, sarcastic_words))))
print("Number of words not shared between set and sarcastic set: " + str(len(words_not_shared(all_words, sarcastic_words))))
print("\n")

def print_shared_words(a, b):
    max_line = 15
    temp = words_shared(a, b)
    for x in [temp[y:y+max_line] for y in range(0, len(temp), max_line)]:
        print(', '.join(x))

def print_not_shared_words(a, b):
    max_line = 15
    temp = words_not_shared(a, b)
    for x in [temp[y:y+max_line] for y in range(0, len(temp), max_line)]:
        print(', '.join(x))

print("The words shared between subsets: ")
print_shared_words(nonsarcastic_words, sarcastic_words)
print("\n")

print("The words not shared between subsets: ")
print_not_shared_words(nonsarcastic_words, sarcastic_words)
print("\n")

print("The words shared between set and nonsarcastic set: ")
print_shared_words(all_words, nonsarcastic_words)
print("\n")

print("The words not shared between set and nonsarcastic set: ")
print_not_shared_words(all_words, nonsarcastic_words)
print("\n")

print("The words shared between set and sarcastic set: ")
print_shared_words(all_words, sarcastic_words)
print("\n")

print("The words not shared between set and sarcastic set: ")
print_not_shared_words(all_words, sarcastic_words)
print("\n")
