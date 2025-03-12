from transformers import pipeline

# Load the NLI model
nli_model = pipeline("text-classification", model="facebook/bart-large-mnli")

# Define the persona and the sentence
persona = "I enjoy poetry."
sentence = "I love writing poems."

# Perform the entailment check
result = nli_model(f"{persona} [SEP] {sentence}")

# Print the result
print(result)

