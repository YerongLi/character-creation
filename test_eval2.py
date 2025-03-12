from pycocoevalcap.cider.cider import Cider
from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer

# Define your persona and sentence in the expected format
persona = {
    'persona1': [{'caption': 'I enjoy poetry.'}]
}
sentence = {
    'sentence1': [{'caption': 'I love writing poems.'}]
}

# Tokenize the sentences
tokenizer = PTBTokenizer()
tokenized_persona = tokenizer.tokenize(persona)
tokenized_sentence = tokenizer.tokenize(sentence)

# Initialize the CIDEr scorer
cider_scorer = Cider()

# Compute the CIDEr score with idf set to "coco-val-df"
score, scores = cider_scorer.compute_score(tokenized_persona, tokenized_sentence, df="coco-val-df")

print("CIDEr Score:", score)
