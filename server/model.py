import math
from collections import defaultdict
from typing import List
import kenlm
from dev_pra_map import cross_map

# Load aligned pairs and build transliteration dictionary
def load_alignment_data():
    aligned_pairs = []

    with open("char_corpus.txt", "r") as corpus_file, open("symmetrized.txt", "r") as align_file:
        for sent_line, align_line in zip(corpus_file, align_file):
            src_sent, tgt_sent = sent_line.strip().split("|||")
            src_words = src_sent.strip().split()
            tgt_words = tgt_sent.strip().split()

            alignment_indices = align_line.strip().split()
            pairs = []
            for a in alignment_indices:
                src_idx, tgt_idx = map(int, a.split('-'))
                if src_idx < len(src_words) and tgt_idx < len(tgt_words):
                    pairs.append((src_words[src_idx], tgt_words[tgt_idx]))
            aligned_pairs.append(pairs)
    return aligned_pairs

def build_lex_table(aligned_pairs):
    freq = defaultdict(lambda: defaultdict(int))
    total = defaultdict(int)

    for sentence in aligned_pairs:
        for src_char, tgt_char in sentence:
            freq[src_char][tgt_char] += 1
            total[src_char] += 1

    lex_table = []
    for src in freq:
        for tgt in freq[src]:
            prob = freq[src][tgt] / total[src]
            lex_table.append((src, tgt, prob))

    return lex_table

def build_translit_dict(lex_table):
    translit_dict = defaultdict(list)
    for src, tgt, prob in lex_table:
        translit_dict[src].append((tgt, prob))
    for src in translit_dict:
        translit_dict[src].sort(key=lambda x: -x[1])
    return translit_dict

# Load KenLM model
def load_language_model():
    # Load the KenLM language model
    model = kenlm.Model("target.arpa")
    return model

# Get the language model probability for a sequence
def get_lm_score(model, sentence: str) -> float:
    return model.score(sentence, bos=False, eos=False)


#correct transliteration
def correct_transliteration(word, translit_dict, mapping):
    final_word = ""
    corresponding_map = [
        (char, translit_dict[char][0][0]) if char in translit_dict else (char, char)
        for char in word
    ]
    

    for i in range(len(corresponding_map) - 1):
        char = cross_map.get(corresponding_map[i][0],None)
        next_char = cross_map.get(corresponding_map[i + 1][0],None)
        
        final_word += corresponding_map[i][1]


        if char and char in mapping:
            char_type = mapping[char]["type"]
            
            

            if (
                char_type == "dependent_vowel"
                or (next_char in mapping and mapping[next_char]["type"] in ["independent_vowel", "dependent_vowel"])
            ):
                continue

            if (
                char_type == "consonant"
                and next_char in mapping
                and mapping[next_char]["type"] == "consonant"
                and mapping[next_char].get("char") != "virama"
                and not corresponding_map[i][1].endswith("a")
            ):
                final_word += "a"

            if next_char in mapping and mapping[next_char].get("char") == "nukta":
                if mapping[char]["char"] != "a" and final_word.endswith("a"):
                    final_word = final_word[:-1]  # remove trailing 'a'

    # Final character processing
    last_char = corresponding_map[-1][0]
    mapped_char = cross_map.get(last_char, None)
    

    if mapped_char and mapped_char in mapping:
        if mapping[mapped_char]["type"] != "dependent_vowel":
            final_word += translit_dict.get(last_char, [(last_char,)])[0][0]
        elif len(word) == 1 and mapping[mapped_char]["type"] == "consonant":
            final_word += "a"
        else:
            final_word+=translit_dict.get(last_char, [(last_char,)])[0][0]
    else:
            final_word += corresponding_map[-1][1]

    return final_word


# Transliteration functions
def transliterate(word: str, translit_dict, lm_model, mapping) -> str:
    corrected = correct_transliteration(word, translit_dict, mapping)

    lm_score = get_lm_score(lm_model, corrected)
    print(f"LM score for corrected transliteration '{corrected}': {lm_score}")

    return corrected

def transliterate_top_k(
    word: str,
    k: int = 3,
    translit_dict=None,
    lm_model=None,
    mapping=None,
) -> List[str]:
    import math

    # Each path = ([(src_char, tgt_char), ...], cumulative_log_prob)
    paths = [([], 0)]

    for char in word:
        options = translit_dict.get(char, [(char, 1.0)])[:k]
        new_paths = []

        for corr_map, logp in paths:
            for tgt_char, prob in options:
                new_corr_map = corr_map + [(char, tgt_char)]
                new_logp = logp + math.log(prob)
                new_paths.append((new_corr_map, new_logp))

        new_paths.sort(key=lambda x: -x[1])
        paths = new_paths[:k]

    scored_corrections = []

    for corr_map, base_score in paths:
        final_word = ""
        for i in range(len(corr_map) - 1):
            char, mapped = corr_map[i]
            next_char, _ = corr_map[i + 1]

            final_word += mapped

            mapped_char = cross_map.get(char, char)
            mapped_next = cross_map.get(next_char, next_char)

            if mapped_char in mapping:
                char_type = mapping[mapped_char]["type"]

                if (
                    char_type == "dependent_vowel"
                    or (mapped_next in mapping and mapping[mapped_next]["type"] in ["independent_vowel", "dependent_vowel"])
                ):
                    continue

                if (
                    char_type == "consonant"
                    and mapped_next in mapping
                    and mapping[mapped_next]["type"] == "consonant"
                    and mapping[mapped_next].get("char") != "virama"
                    and not mapped.endswith("a")
                ):
                    final_word += "a"

                if (
                    mapped_next in mapping
                    and mapping[mapped_next].get("char") == "nukta"
                    and mapping[mapped_char]["char"] != "a"
                    and final_word.endswith("a")
                ):
                    final_word = final_word[:-1]

        # Final character correction
        last_char, last_mapped = corr_map[-1]
        mapped_last_char = cross_map.get(last_char, last_char)
        # print(mapped_last_char in mapping)

        if mapped_last_char in mapping:
            if mapping[mapped_last_char]["type"] != "dependent_vowel":
                final_word += last_mapped
            elif len(word) == 1 and mapping[mapped_last_char]["type"] == "consonant":
                final_word += "a"
            else:
                final_word+=last_mapped
        else:
            final_word += last_mapped

        lm_score = get_lm_score(lm_model, final_word)
        total_score = base_score + lm_score
        scored_corrections.append((total_score, final_word))

    scored_corrections.sort(reverse=True)
    return [final for _, final in scored_corrections[:k]]



# Main setup
aligned_data = load_alignment_data()
lex_table = build_lex_table(aligned_data)
translit_dict = build_translit_dict(lex_table)
lm_model = load_language_model()

# Example usage of transliteration with LM:
if __name__ == "__main__":
    word = "example"  # Replace with any word you want to test
    top_k = 3
    print(f"Best transliteration: {transliterate(word, translit_dict, lm_model)}")
    print(f"Top {top_k} transliterations: {transliterate_top_k(word, top_k, translit_dict, lm_model)}")
