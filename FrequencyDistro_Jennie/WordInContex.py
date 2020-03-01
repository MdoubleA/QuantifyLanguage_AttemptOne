import nltk


REF = "Reference"
NON = "Nonsarcastic"
SAR = "Sarcastic"
SHA = "Shared"

type_to_number = {REF: 0, NON: 1, SAR: 2, SHA: 3}
number_to_type = {0: REF, 1: NON, 2: SAR, SHA: 3}

src_file = "UniqueWordsAndSharedWords.txt"


# Get the most common unique words by type.
def get_unique_words(file=src_file):
    to_ret = dict()
    with open(file, "r") as file_handle:
        curr_line = file_handle.readline().strip()
        while curr_line:
            curr_line = curr_line[0:-1]
            to_ret[curr_line] = file_handle.readline().strip().replace(" ", "").split(",")

            curr_line = file_handle.readline().strip()

    return to_ret


def get_corpus(file_name):
    with open(file_name, "r") as file_handle:
        the_text = [line.strip().split("\t")[0].split(" ") for line in file_handle.readlines()][1:]

    return nltk.Text([token.lower() for post in the_text for token in post])


sarc_file_name = "C:\\Users\\Michael\\PycharmProjects\\QuantfyLanguage_AttemptOne\\SarcCommentsClean\\SarcComments.csv"
non_sarc_file_name = "C:\\Users\\Michael\\PycharmProjects\\QuantfyLanguage_AttemptOne\\NonSarcCommentsClean\\" \
                     "NonSarcComments.csv"

sarc_text = get_corpus(sarc_file_name)
non_sarc_text = get_corpus(non_sarc_file_name)
all_words_text = nltk.Text(list(sarc_text) + list(non_sarc_text))
unique_words = get_unique_words()  # {str : [str]}
type_to_corpus = {
    REF: all_words_text,
    NON: non_sarc_text,
    SAR: sarc_text
}

for key in type_to_number.keys():
    if key != SHA:
        with open(key + ".txt", "w") as file_handle:
            for token in unique_words[key]:
                file_handle.write("*" + token + "\n")
                contex = type_to_corpus[key].concordance_list(token, width=15, lines=500)
                for a in contex:
                    #file_handle.write(", ".join(a.left) + "\n")
                    file_handle.write(", ".join(a.right) + "\n")

with open("Sarcastic.txt", "r") as file_handle:
    key_word = file_handle.readline().strip()[1:]
    line = file_handle.readline()
    context = list()
    while line[0] != "*":
        context += line.strip().split(", ")
        line = file_handle.readline()

result = sorted(context, key=context.count, reverse=True)
print(result)


