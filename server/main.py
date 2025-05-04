from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from model import (
    transliterate,
    transliterate_top_k,
    load_alignment_data,
    build_lex_table,
    build_translit_dict,
    load_language_model,  # Add this if mapping is loaded from a function
)
from CSM import mapping
from tokenizer import tokenize_word_to_consonants_vowels
from fastapi.middleware.cors import CORSMiddleware
from dev_pra_map import cross_map

# Load the alignment data and build the transliteration dictionary
aligned_data = load_alignment_data()
lex_table = build_lex_table(aligned_data)
translit_dict = build_translit_dict(lex_table)
lm_model = load_language_model()
  # Load your char type mapping

app = FastAPI(title="Transliteration API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # or ["*"] to allow all (not recommended in prod)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InputText(BaseModel):
    word: str  # Can be single word or multi-word string
    k: int = 1



@app.post("/transliterate_statistical")
def get_transliteration(data: InputText):
    words = data.word.strip().split()

    if data.k == 1:
        results = [transliterate(w, translit_dict, lm_model, mapping) for w in words]
        return {
            "input": data.word,
            "result": " ".join(results),
            "tokens": results
        }
    else:
        top_k_results = [
            transliterate_top_k(w, data.k, translit_dict, lm_model, mapping)
            for w in words
        ]
        return {
            "input": data.word,
            "top_k": top_k_results
        }



class TransliterateReq(BaseModel):
    text: str

@app.post('/transliterate_rule')
async def transliterate_rule(text: TransliterateReq):
    words = text.text.split()
    transliterated_words = []
    all_independent_vowels = []
    all_consonants = []
    all_dependent_vowels = []
    all_digits = []
    all_spaces = []
    all_symbols = []
    all_punctuation = []

    for word in words:
        independent_vowels, consonants, dependent_vowels, digits, spaces, symbols, punctuation = tokenize_word_to_consonants_vowels(word)

        all_independent_vowels.extend(independent_vowels)
        all_consonants.extend(consonants)
        all_dependent_vowels.extend(dependent_vowels)
        all_digits.extend(digits)
        all_spaces.extend(spaces)
        all_symbols.extend(symbols)
        all_punctuation.extend(punctuation)

        # Transliterate the word
        transliterated_chars = []



        for i in range(len(word) - 1):
            # print(word[i])
            char = cross_map.get(word[i],"")
            next_char = cross_map.get(word[i + 1],"")

            if char in mapping:
                char_type = mapping[char]["type"]
                transliterated_chars.append(mapping[char]["char"])

                # print(f'{mapping[char]["char"]}')

                if(char_type=='dependent_vowel' or (mapping[next_char]["type"] == "independent_vowel") or (mapping[next_char]["type"] == "dependent_vowel")):
                    # print(f"{char} {mapping[char]['char']}")
                    continue
                
               
                if char_type == "consonant" and next_char in mapping and mapping[next_char]["type"] == "consonant" and (mapping[next_char]["char"]!='virama'):
                    transliterated_chars.append("a")

                if(mapping[next_char]["char"]=='nukta'):
                    if((mapping[char]['char']!='a')) :
                        if(transliterated_chars[-1]=='a'):
                            transliterated_chars[-1]==''

            

        # Handle the last character in the word
        if cross_map.get(word[-1],"") in mapping:
            if(mapping[cross_map.get(word[-1],"")]["type"]!='dependent_vowel'):
                transliterated_chars.append(mapping[cross_map.get(word[-1],"")]["char"])
            elif(len(word)==1):
                if mapping[cross_map.get(word[-1],"")]['type'] == "consonant":
                    transliterated_chars.append("a")
            else:
                transliterated_chars.append(mapping[cross_map.get(word[-1],"")]["char"])



        transliterated_word = "".join(transliterated_chars)
        transliterated_words.append(transliterated_word)

    transliterated_text = " ".join(transliterated_words)

    return {
        'ans': transliterated_text,
        'independent_vowels': list(set(all_independent_vowels)),
        'consonants': list(set(all_consonants)),
        'dependent_vowels': list(set(all_dependent_vowels)),
        'digits': list(set(all_digits)),
        'spaces': list(set(all_spaces)),
        'symbols': list(set(all_symbols)),
        'punctuation': list(set(all_punctuation))
    }



@app.get("/")
def root():
    return {"message": "Welcome to the Transliteration API"}
