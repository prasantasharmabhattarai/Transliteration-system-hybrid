def tokenize_words_to_characters(line):
    """Split words and return list of space-separated characters."""
    words = line.strip().split()
    return [' '.join(list(word)) for word in words]

def process_file(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as infile, \
         open(output_file, "w", encoding="utf-8") as outfile:
        
        for line in infile:
            tokenized_words = tokenize_words_to_characters(line)
            for token in tokenized_words:
                outfile.write(token + '\n')

    print(f"✅ Successfully saved to '{output_file}'")

# Change these paths as needed
input_path = "corpus.tgt"
output_path = "_corpus.tgt"

process_file(input_path, output_path)
