import openai

# Load your API key from an environment variable or secret management service
openai.api_key = ("key")

text = openai.Image.create(
    prompt="A cute baby sea otter",
    n=2,
    size="256x256"
)
print(text)