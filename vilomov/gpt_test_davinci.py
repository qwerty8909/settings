import openai

# Load your API key from an environment variable or secret management service
openai.api_key = ("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")
question = str
answer = str

def gpt(question):
    text = openai.Completion.create(
        model="text-davinci-003",
        prompt=question,
        temperature=0.7,
        max_tokens=400,
        top_p=1,
        best_of=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["//#"]
    )
    global answer
    answer = text['choices'][0]['text'].strip()
    print(answer)


while question != 'print exit':
    question = input()
    gpt(question)
