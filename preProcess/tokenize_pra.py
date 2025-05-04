devanagari_core_chars = [

    'अ', 'आ  ', 'इ', 'ई', 'उ', 'ऊ',
    'ऋ', 'ॠ', 'ऌ', 'ॡ',
    'ए', 'ऐ', 'ओ', 'औ',
    'ऑ', 'ऒ', 'ऍ', 'ॲ', 'ॳ', 'ॴ', 'ॵ',

    'क', 'ख', 'ग', 'घ', 'ङ',
    'च', 'छ', 'ज', 'झ', 'ञ',
    'ट', 'ठ', 'ड', 'ढ', 'ण',
    'त', 'थ', 'द', 'ध', 'न',
    'प', 'फ', 'ब', 'भ', 'म',
    'य', 'र', 'ल', 'व',
    'श', 'ष', 'स', 'ह',
    'ळ', 'क्ष', 'ज्ञ',


    '।', '॥'
]


def custom_join(l1):
    res = ""
    for i,char in enumerate(l1):
        if i!=0:
            if l1[i] not in devanagari_core_chars:
                res+=" "
        
        res=res+char+" "

    if res[-1]==" " and res[-2]==" ":
        res=res[:-1]
            

    return res.strip()

def prepare_char_level_data(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as infile, \
         open(output_path, 'w', encoding='utf-8') as outfile:

        for line in infile:
            words = line.strip().split()
            for word in words:
                char_list = list(word)
                char_spaced = custom_join(char_list)
                outfile.write(char_spaced + '\n')

    print(f"✅ Character-level data saved to: {output_path}")

prepare_char_level_data('corpus.src','_corpus.src')
