import nltk
from nltk.corpus import stopwords
import string
from collections import Counter
import matplotlib.pyplot as plt

# Category short hands.
REF = "Reference"
NON = "Nonsarcastic"
SAR = "Sarcastic"
SHA = "Shared"

# Map category short hands to numbers and vice versa; a form of enumeration, I don't like the built in enum support.
cate_to_numb = {REF: 0, NON: 1, SAR: 2, SHA: 3}
numb_to_cate = {0: REF, 1: NON, 2: SAR, SHA: 3}

sarc_file_name = "C:\\Users\\Michael\\PycharmProjects\\QuantfyLanguage_AttemptOne\\SarcCommentsClean\\SarcComments.csv"
nonsarc_file_name = "C:\\Users\\Michael\\PycharmProjects\\QuantfyLanguage_AttemptOne\\NonSarcCommentsClean\\" \
                     "NonSarcComments.csv"
key_word_file_name = "UniqueWordsAndSharedWords.txt"


# From file pull the corpus. Expects a CSV file with tokenized comments in first column followed by metadata.
# [str] where each string is a post made of only lower case letters.
def get_corpus(file_name):
    with open(file_name, "r") as file_handle:
        #  For each line in the file remove white space, get first column, convert it to list and add it to "the_text".
        #  The csv header file will be in the 0th position, remove it.
        the_text = [line.strip().split("\t")[0].lower() for line in file_handle.readlines()][1:]

    return the_text


# Pull from file unique words and organize by category.
# Ex return: {"Shared":[str]}
def get_key_words(file_name):
    to_ret = dict()
    with open(file_name, "r") as file_handle:
        curr_line = file_handle.readline().strip()
        while curr_line:
            curr_line = curr_line[0:-1]
            to_ret[curr_line] = file_handle.readline().strip().replace(" ", "").split(",")
            curr_line = file_handle.readline().strip()

    return to_ret


# Get the corpus for later processing. Important that these data go unchanged and are copied rather than altered.
sarc_corpus = get_corpus(sarc_file_name)  # [str]
nonsarc_corpus = get_corpus(nonsarc_file_name)
reference_corpus = sarc_corpus + nonsarc_corpus
shared_corpus = reference_corpus
key_words = get_key_words(key_word_file_name)  # {"Shared":[str]}
stop_words = set([word.translate(str.maketrans('', '', string.punctuation)) for word in stopwords.words('english')])

cate_to_corpus = {
    SAR: sarc_corpus,
    SHA: shared_corpus,
    NON: nonsarc_corpus,
    REF: reference_corpus,
}


# Return the corpus without stop words
def remove_stop_words(the_corpus):
    # [[str]]
    return [[a_word for a_word in a_post.split(" ") if a_word not in stop_words] for a_post in the_corpus]


# Return tagged corpus.
# Expects corpus as a list of lists of str's, [[str]].
def get_tagged_corpus(the_corpus):
    return [nltk.pos_tag(a_post) for a_post in the_corpus]  # [(str, str)], (word, part-of-speech)


# [[str]]
stopwordless_sarc = remove_stop_words(sarc_corpus)
stopwordless_nonsarc = remove_stop_words(nonsarc_corpus)
stopwordless_reference = remove_stop_words(reference_corpus)
stopwordless_shared = stopwordless_reference

# [[(str, str)]]
# [[(key_word, tag)]]
tagged_sarc = get_tagged_corpus(stopwordless_sarc)
tagged_nonsarc = get_tagged_corpus(stopwordless_nonsarc)
tagged_reference = get_tagged_corpus(stopwordless_reference)
tagged_shared = tagged_reference

# Map category short hands to tagged corpora.
# {str: [[(key_word, tag)]]}
cate_to_tagged_key_words = {
    SAR: tagged_sarc,
    NON: tagged_nonsarc,
    REF: tagged_reference,
    SHA: tagged_shared,
}


# Parameters: tagged_corpora -> {str: [[(key_word, tag)]]}, key_words -> {"Shared":[str]}
# {str: [(str, str)]} -> {'category': [('key_word', 'tag')]}
def filter_for_tagged_key_words(tagged_corpora, key_words):
    to_ret = {k: [a_word for a_post in tagged_corpora[k] for a_word in a_post if a_word[0] in v]
              for k, v in key_words.items()
              }  # for a_word in a_post } # if a_word[0] in v}
    return to_ret


def send_tag_words_to_file(tagged_words):
    with open("TaggedKeyWords.txt", "w") as file_handle:
        for k, v in tagged_words.items():
            file_handle.write(k + ":\n")
            file_handle.write(" ".join([":".join(x) for x in v]) + "\n")


tagged_key_words = filter_for_tagged_key_words(cate_to_tagged_key_words, key_words)
# send_tag_words_to_file(tagged_key_words)


cate_stopwordless_corpus = {
    SAR: stopwordless_sarc,
    NON: stopwordless_nonsarc,
    REF: stopwordless_reference,
    SHA: stopwordless_shared,
}


# Always and only pass "cate_to_stopwordless_corpus".
# {str: {str: [[str]]}}
def sort_corpus_by_key_word(a_corpus):
    return {category: {a_word: [a_post for a_post in a_corpus[category] if a_word in a_post]
                       for a_word in key_words[category]} for category, key_words_ in key_words.items()}


# Orientation is your right or left, not the posts's.
# [str]
# Returns up to length number of elements to the right or left of key_word as a list; plus key_word,
# for a total of up to length + 1 elements.
def get_window(key_word, the_post, orientation, window_size):
    to_return = []
    locus = the_post.index(key_word)

    if orientation == 'right':
        to_return = the_post[locus:locus+window_size+1]
        if window_size == 0:
            to_return = [the_post[locus]]
    if orientation == 'left':
        start = locus - window_size
        if start < 0:
            start = 0
        to_return = the_post[start: locus + 1]

    return to_return


# Always and only pass "cate_to_stopwordless_corpus".
# {str: {str: [[str]]}}
def get_keyword_context(a_corpus, window_size, orientation):
    return {category: {a_word: [a_post for a_post in a_corpus[category] if a_word in a_post]
                       for a_word in key_words[category]} for category, key_word_mapping in key_words.items()}



'''

print(sarc_corpus[0])
print(stopwordless_sarc[0])
i need a girlfriend omg i am insulted and the code is wrongfun anyway idiots
['need', 'girlfriend', 'omg', 'insulted', 'code', 'wrong', 'anyway', 'idiots']

'''



# Be sure to satisfy PEP 8.
