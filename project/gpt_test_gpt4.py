import openai

# Load your API key from an environment variable or secret management service
openai.api_key = ("key")
question = str
answer = str

def gpt(question):
    completion = openai.ChatCompletion.create(
        model="gpt-4", # gpt-4, gpt-4-0314, gpt-4-32k, gpt-4-32k-0314, gpt-3.5-turbo, gpt-3.5-turbo-0301
        messages=[
            # {"role": "system", "content": "You are a very proficient SEO and high end copy writer."},
            {"role": "user", "content": question}
        ],
        temperature=0.7,
        # max_tokens=400,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["//#"]
    )
    global answer
    answer = completion.choices[0].message['content']
    print(answer)


while question != 'print exit':
    question = input()
    gpt(question)