def tokenize_and_save(input_file, output_file):
    try:
        # Open the input file to read the content
        with open(input_file, 'r', encoding='utf-8') as infile:
            text = infile.read()  # Read the entire content of the file
            
        # Tokenize by splitting the content based on spaces
        tokens = text.split()  # This splits by any whitespace, including spaces
        
        # Open the output file to save the tokenized words
        with open(output_file, 'w', encoding='utf-8') as outfile:
            # Write each token on a new line
            for token in tokens:
                outfile.write(token + '\n')
        
        print(f"Tokenization complete. The output is saved in {output_file}.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
input_file = 'corpus.tgt'  # Replace with your input file name
output_file = 'lang_model_train.txt'  # Replace with your desired output file name

tokenize_and_save(input_file, output_file)