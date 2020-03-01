import csv
from matplotlib import pyplot as plt
from matplotlib_venn import venn2, venn3


all_files = [
    'most_freq_words.csv',
    'most_freq_words_non_sarc.csv',
    'most_freq_words_sarc.csv',
]

both = 0
nonsarcastic = 1
sarcastic = 2

REF = "Reference"
NON = "Nonsarcastic"
SAR = "Sarcastic"


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


def set_overlap_2(set_a, set_b, group_names, title):
    Ab = [x for x in set_a if x not in set_b]
    aB = [x for x in set_b if x not in set_a]
    AB = [x for x in set_a if x in set_b]

    venn2(subsets=(len(Ab), len(aB), len(AB)), set_labels=(group_names[0], group_names[1]))
    plt.title(title)
    plt.savefig(title + ".png")
    #plt.show()
    plt.close()


def set_overlap_3(set_a, set_b, set_c, group_names, title):
    # ABC
    Abc = [x for x in set_a if x not in set_b + set_c]
    aBc = [x for x in set_b if x not in set_a + set_c]
    ABc = [x for x in set_a if x in set_b and x not in set_c]
    abC = [x for x in set_c if x not in set_a + set_b]
    AbC = [x for x in set_a if x in set_c and x not in set_b]
    aBC = [x for x in set_b if x in set_c and x not in set_a]
    ABC = [x for x in set_a if x in set_b and x in set_c]

    venn3(subsets=(len(Abc), len(aBc), len(ABc), len(abC), len(AbC), len(aBC), len(ABC)),
          set_labels=(group_names[0], group_names[1], group_names[2]))
    plt.title(title)
    plt.savefig(title + ".png")
    #plt.show()
    plt.close()

    print("The words unique to " + group_names[0] + ": ")
    print(Abc)
    print("\n")

    print("The words unique to " + group_names[1] + ": ")
    print(aBc)
    print("\n")

    print("The words unique to " + group_names[2] + ": ")
    print(abC)
    print("\n")

    print("The words shared by all of the sets: ")
    max_step = 5
    for x in range(0, len(ABC), max_step):
        print(", ".join(ABC[x:x+max_step]))
    print("\n")

    with open("UniqueWordsAndSharedWords.txt", "w") as file_handle:
        file_handle.write(group_names[0] + ": " + "\n")
        file_handle.write(", ".join(Abc) + "\n")

        file_handle.write(group_names[1] + ": " + "\n")
        file_handle.write(", ".join(aBc) + "\n")

        file_handle.write(group_names[2] + ": " + "\n")
        file_handle.write(", ".join(abC) + "\n")

        file_handle.write("Shared: \n")
        file_handle.write(", ".join(ABC) + "\n")


'''Ref & Non'''
title = REF + " vs " + NON
set_overlap_2(all_words, nonsarcastic_words, (REF, NON), title)

'''Non & Sar'''
title = NON + " vs " + SAR
set_overlap_2(nonsarcastic_words, sarcastic_words, (NON, SAR), title)

'''Sar & Ref'''
title = SAR + " vs " + REF
set_overlap_2(sarcastic_words, all_words, (SAR, NON), title)

'''Sar, Ref, and Non'''
title = SAR + " vs " + REF + " vs " + NON
set_overlap_3(sarcastic_words, all_words, nonsarcastic_words, (SAR, REF, NON), title)
