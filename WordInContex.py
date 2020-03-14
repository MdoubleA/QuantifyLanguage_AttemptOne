import nltk
from collections import Counter
import matplotlib.pyplot as plt


# Category short hands.
REF = "Reference"
NON = "Nonsarcastic"
SAR = "Sarcastic"
SHA = "Shared"

# Map category short hands to numbers and vice versa; a form of enumeration, I don't like the built in enum support.
type_to_number = {REF: 0, NON: 1, SAR: 2, SHA: 3}
number_to_type = {0: REF, 1: NON, 2: SAR, SHA: 3}

# The various data source files.
# All results, even some intermittent results stored in file for documentation.
# Path names are absolute.
src_file = "UniqueWordsAndSharedWords.txt"
sarc_file_name = "C:\\Users\\Michael\\PycharmProjects\\QuantfyLanguage_AttemptOne\\SarcCommentsClean\\SarcComments.csv"
non_sarc_file_name = "C:\\Users\\Michael\\PycharmProjects\\QuantfyLanguage_AttemptOne\\NonSarcCommentsClean\\" \
                     "NonSarcComments.csv"


# Pull from file unique words and organize by category.
# Ex return: {"Shared":[str]}
def get_unique_words(file=src_file):
    to_ret = dict()
    with open(file, "r") as file_handle:
        curr_line = file_handle.readline().strip()
        while curr_line:
            curr_line = curr_line[0:-1]
            to_ret[curr_line] = file_handle.readline().strip().replace(" ", "").split(",")
            curr_line = file_handle.readline().strip()

    return to_ret


# From file pull the corpus. Expects a CSV file with tokenized comments in first column followed by metadata.
def get_corpus(file_name):
    with open(file_name, "r") as file_handle:
        #  For each line in the file remove white space, get first column, convert it to list and add it to "the_text".
        #  The csv header file will be in the 0th position, remove it.
        #  Return the comments corpus as nltk Text object.
        the_text = [line.strip().split("\t")[0].split(" ") for line in file_handle.readlines()][1:]

    return nltk.Text([token.lower() for post in the_text for token in post])


#  Get clean tokenized comment data as nltk Text object.
sarc_text = get_corpus(sarc_file_name)
non_sarc_text = get_corpus(non_sarc_file_name)
# There is no single repository of both sarcastic and nonsarcastic data.
# A Text object of the two categories created below.
all_words_text = nltk.Text(list(sarc_text) + list(non_sarc_text))
unique_words = get_unique_words()  # {str:[str]}

# Map tokenized data to category shorthands.
type_to_corpus = {
    REF: all_words_text,
    NON: non_sarc_text,
    SAR: sarc_text,
    SHA: all_words_text,
}


# Get the context specified by orientation of concordance_list_reference.
# Return type: [str]
def get_context(concordance_list_reference, orientation):
    orientation_mapping = {
        "right": concordance_list_reference.right,
        "left": concordance_list_reference.left,
        "center": concordance_list_reference.line.split(" "),  # The line field is not a list; left and right are.
    }

    return orientation_mapping.get(orientation, concordance_list_reference.right)


# Save to file the specified context of the key words by category.
def get_key_word_context_to_file(orientation, window_size=15, max_num_lines_returned=500):
    for key in type_to_number.keys():
        with open(key + ".txt", "w") as file_handle:
            for token in unique_words[key]:
                file_handle.write("*" + token + "\n")
                context = type_to_corpus[key].concordance_list(token, width=window_size, lines=max_num_lines_returned)
                for a in context:
                    file_handle.write(", ".join(get_context(a, orientation)) + "\n")


# If desire to make new context files, comment out flag = False below; a short term fix.
flag = True
flag = False

if flag:
    user_input = input("Specify: window orientation, window size, and number of context lines. Space delineated. ")
    if user_input[0] == "d":
        user_input = ["right", "15", "20"]
    else:
        user_input = user_input.strip().split()
    get_key_word_context_to_file(orientation=user_input[0], window_size=int(user_input[1]), max_num_lines_returned=int(user_input[2]))


# NEED to get probabilities for each phrase
def get_context_frequency_distro():
    for classification in type_to_number.keys():
        with open(classification + "Context" + "Freq" + ".txt", "w") as freq_data_handle:
            with open(classification + ".txt", "r") as raw_context_handle:
                key_word = raw_context_handle.readline()  # Get the keyword, ex: *oh
                while True:
                    line = raw_context_handle.readline()  # Read first line of context, processing happens in loop.
                    context = list()
                    while line and line[0] != "*":  # Get the context for just one key word.
                        context += line.strip().split(", ")  # Processing, turn string into list of individual words.
                        line = raw_context_handle.readline()  # Get raw string.

                    # Make frequency distribution.
                    word_counts = Counter(context)  # The count of each word in the key words context.
                    tot_num_word = len(context)  # Total number of words in a context.
                    freq_distro = {key: (value/tot_num_word) * 100 for key, value in word_counts.items()}  # Count to Frequency.
                    freq_distro = [(k, v) for k, v in sorted(freq_distro.items(), key=lambda item: item[1])]  # Sort by Frequency.
                    freq_distro.reverse()  # Most frequent to front of list.

                    freq_data_handle.write(key_word)
                    freq_data_handle.write("Total number of words in context: " + str(tot_num_word) + "\n")
                    freq_data_handle.write(" ".join([data[0] + ":" + str(data[1]) for data in freq_distro]) + "\n")

                    if not line:
                        break
                    key_word = line

# get_context_frequency_distro()


def plot_bar_graph(words, probs, title):
    x_axis = [x for x in range(len(words))]
    plt.bar(x_axis, probs)
    plt.xlabel('Words', fontsize=12)
    plt.ylabel('Frequencies', fontsize=12)
    plt.xticks(x_axis, words, fontsize=11, rotation=35)
    plt.title(title)
    plt.show()


def graph_contextual_frequencies(amt_context):
    suffix = "ContextFreq.txt"
    for key in type_to_number.keys():
        file_name = key + suffix
        with open(file_name, "r") as file_handle:
            key_word = file_handle.readline().strip()[1:]
            context_word_count = file_handle.readline().strip().split(" ")[-1:]
            frequencies = file_handle.readline().strip().split(" ")

            frequencies = [x.split(":") for x in frequencies[:amt_context]]
            words = [x[0] for x in frequencies]
            frequencies = [float(x[1]) for x in frequencies]

            plot_bar_graph(words, frequencies, key_word)


graph_contextual_frequencies(5)
