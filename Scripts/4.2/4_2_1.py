import os

usc_lexicon = os.path.expanduser("~/usc/lexicon.txt")
kaldi_data = os.path.expanduser("~/kaldi/egs/usc/data")
dict_dir = os.path.join(kaldi_data, "local/dict")

phonemes = set()

# Extract phonemes from USC lexicon
with open(usc_lexicon) as f:
    for line in f:
        parts = line.strip().split()
        for p in parts[1:]:
            if p != "<oov>": #<oov> (out of vocabulary) is not phoneme but it appears at usc/lexicon.txt
                phonemes.add(p)

phonemes = sorted(phonemes)

sil = "sil" #Silence phone

with open(os.path.join(dict_dir, "silence_phones.txt"), "w") as f: #creation of silence_phones.txt
    f.write(sil + "\n")

with open(os.path.join(dict_dir, "optional_silence.txt"), "w") as f: #creation of optional_silence.txt
    f.write(sil + "\n")

with open(os.path.join(dict_dir, "nonsilence_phones.txt"), "w") as f: #creation of nonsilence_phones.txt
    for p in phonemes:
        if p != sil:
            f.write(p + "\n")

with open(os.path.join(dict_dir, "lexicon.txt"), "w") as f:  #creation of lexicon.txt
    for p in phonemes:
        f.write(f"{p} {p}\n")

#creation of lm_train.text files

def create_lm(split):

    text_file = os.path.join(kaldi_data, split, "text")
    lm_file = os.path.join(kaldi_data, split, "lm_train.text")

    with open(text_file) as inp, open(lm_file, "w") as out:
        for line in inp:
            parts = line.strip().split()

            # remove utterance id
            sentence = " ".join(parts[1:])

            out.write(f"<s> {sentence} </s>\n")


create_lm("train")
create_lm("dev")
create_lm("test")

open(os.path.join(dict_dir, "extra_questions.txt"), "w").close() #creation of extra_questions.txt

