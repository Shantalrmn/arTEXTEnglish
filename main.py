"""
Created on Mon Mar 10 22:03:23 2025

@author: Shantal Robles Román
"""
# ======================== IMPORTS ========================
import nltk
nltk.download('wordnet')
import pandas as pd
import pyphen
#from nltk.corpus import wordnet as wn
# ======================== IMPORTS ========================

pyphen_dic = pyphen.Pyphen(lang='en_US')

def count_syllables(word):
   
    syllables = pyphen_dic.inserted(word).split('-')
    return len(syllables)

def identify_words_by_syllables_and_match(lemmas, prefix):
   
    filtered_lemmas = [lemma for lemma in lemmas if prefix.lower() in lemma.lower()]
  
    if len(filtered_lemmas) < 2:
        return []

    sorted_words = sorted(filtered_lemmas, key=count_syllables)

    
    short_word = sorted_words[0]
    long_word = sorted_words[-1]

    return [{'short word': short_word, 'long word': long_word}]

def process_all_synsets(output_excel='filtered_synsets.xlsx'):
    results = []
    processed = set()

    for synset in wn.all_synsets():
        if synset.name() in processed:
            continue
        processed.add(synset.name())

        main_name = synset.name().split('.')[0]  
        prefix = main_name[:3]  

      
        lemmas = {lemma.name() for lemma in synset.lemmas()}

       
        pairs = identify_words_by_syllables_and_match(lemmas, prefix)
        results.extend(pairs)

  
    df = pd.DataFrame(results)
    df.to_excel(output_excel, index=False)
    print(f"Excel file saved as '{output_excel}'")

process_all_synsets()
