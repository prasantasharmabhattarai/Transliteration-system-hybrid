from collections import defaultdict

aligned_pairs = []

# Step 1: Read aligned character pairs
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

# Step 2: Count frequencies of aligned pairs
freq = defaultdict(lambda: defaultdict(int))
total = defaultdict(int)

for sentence in aligned_pairs:
    for src_char, tgt_char in sentence:
        freq[src_char][tgt_char] += 1
        total[src_char] += 1

# Step 3: Compute probabilities
lex_table = []
for src in freq:
    for tgt in freq[src]:
        prob = freq[src][tgt] / total[src]
        lex_table.append((src, tgt, prob))

# Step 4: Output the top alignments
print("\nTop probabilistic character alignments:")
for entry in sorted(lex_table, key=lambda x: -x[2])[:150]:
    print(f"{entry[0]} ||| {entry[1]} ||| {entry[2]:.4f}")
