import os
from pathlib import Path
import nltk
import string


src_dir = input("\nEnter Directory Name: ").strip()
header = "post\tlabel\tauthor\tsubreddit\tscore\tups\tdowns\tdate\tcreated_utc\tparent_comment\tpost_id\tparent_id\n"
dst_dir = src_dir + "Clean"
dst_file = dst_dir + "\\" + src_dir + ".csv"
Path(dst_dir).mkdir(parents=True, exist_ok=True)  # Make destination file if it doesn't exist.

clean_post = lambda x: ' '.join(nltk.word_tokenize(x.lower().translate(str.maketrans('', '', string.punctuation))))

with open(dst_file, "+w") as dst_handle:
    dst_handle.write(header)

    for filename in os.listdir(src_dir):  # For every dirty csv file in src, do the following . . .
        with open(src_dir + "\\" + filename, "r") as src_handle:
            row = src_handle.readline()

            while row != '':
                row = row.strip().split("\t")
                post = clean_post(row[1]) + "\t"
                parent_post = clean_post(row[9]) + "\t"
                row = post + row[0] + "\t" + '\t'.join(row[2:9]) + "\t" + parent_post + "\t".join(row[10:]) + "\n"
                dst_handle.write(row)
                row = src_handle.readline()
