import os            
import subprocess
import math

def decompress_arpa_gz(gz_path, out_path):
    # Decompressing a .arpa.gz file to .arpa
    with open(out_path, 'w', encoding='utf-8') as out_f:
        subprocess.run(['gunzip', '-c', gz_path], stdout=out_f, check=True)

def parse_arpa(arpa_path):
    # Extracting probabilities from .arpa file
    unigrams = {}
    bigrams = {}
    backoff = {}
    ngram_section = None

    with open(arpa_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("\\data\\") or line.startswith("ngram"):
                continue
            if line.startswith("\\1-grams:"):
                ngram_section = 1
                continue
            elif line.startswith("\\2-grams:"):
                ngram_section = 2
                continue
            elif line.startswith("\\end\\"):
                break

            parts = line.split()
            if ngram_section == 1:
                log_prob = float(parts[0])
                word = parts[1]
                backoff_w = float(parts[2]) if len(parts) > 2 else 0.0
                unigrams[word] = log_prob
                backoff[word] = backoff_w
            elif ngram_section == 2:
                log_prob = float(parts[0])
                w1, w2 = parts[1], parts[2]
                bigrams[(w1, w2)] = log_prob

    return unigrams, bigrams, backoff

def compute_perplexity(text_path, unigrams, bigrams, model_type='bigram'):
    log2_prob_sum = 0.0
    M = 0

    with open(text_path, 'r', encoding='utf-8') as f:
        for line in f:
            words = line.strip().split()
            if not words:
                continue
            M += len(words) - 1 # Do not count as words <s> and </s>

            for i in range(1, len(words)):
                w2 = words[i]
                if model_type == 'bigram' and bigrams:
                    w1 = words[i-1]
                    log10p = bigrams.get((w1, w2), unigrams.get(w2, -10.0))
                else:
                    log10p = unigrams.get(w2, -10.0)
                log2_prob_sum += log10p * math.log2(10)  # convert log10 to log2

    H = -log2_prob_sum / M
    return 2 ** H

lm_gz_files = {
    "bg_bigram": os.path.expanduser("~/kaldi/egs/usc/data/local/nist_lm/lm_phone_bg.arpa.gz"),
    "ug_unigram": os.path.expanduser("~/kaldi/egs/usc/data/local/nist_lm/lm_phone_ug.arpa.gz")
}

texts = {
    "test": os.path.expanduser("~/kaldi/egs/usc/data/test/lm_train.text"),
    "validation": os.path.expanduser("~/kaldi/egs/usc/data/dev/lm_train.text")
}

models = {}
for name, gz_path in lm_gz_files.items():
    arpa_path = gz_path.replace(".gz", "")
    if not os.path.exists(arpa_path):
        decompress_arpa_gz(gz_path, arpa_path)
    models[name] = parse_arpa(arpa_path)

for model_name, (unigrams, bigrams, backoff) in models.items():
    for text_name, text_path in texts.items():
        if bigrams:
            pp = compute_perplexity(text_path, unigrams, bigrams, model_type='bigram')
            print(f"Text: {text_name}, Bigram perplexity: {pp:.3f}")
        else:
            pp = compute_perplexity(text_path, unigrams, bigrams, model_type='unigram')
            print(f"Text: {text_name}, Unigram perplexity: {pp:.3f}")