# загружаем необходимые модули и библиотеки
import openai
from deep_translator import GoogleTranslator

openai.api_key = ("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")
with open('gpt_rewrite_in.txt', 'r') as file:
    file_contents = file.read()

with open('gpt_rewrite_prompt.txt', 'r') as file:
    file_prompt = file.read()

content = file_contents.replace('\'', '').replace('\n', ' ').replace('"', ' ').replace("'", " ")\
                        .replace('(', '').replace(')', '').replace('  ', ' ').replace(' .', '.')
results = openai.Completion.create(
    model="text-davinci-003",               # "text-davinci-003" "text-curie-001"
    prompt=file_prompt + content + '.\n',   # make the article in 650 words as sport news:
                                            # make the advertising in 150 words for sporting event:
                                            # summarize text in 600 words:
                                            # shorten the article in 650 words:
    temperature=0.7,
    max_tokens=1500,
    top_p=1,
    best_of=1,
    frequency_penalty=0.5,
    presence_penalty=0,
    stop=["//#"]
)
response = dict(results)
openai_response = response['choices']
eng_text = openai_response[-1]['text']

translated = GoogleTranslator(source='en', target='ru').translate(eng_text)
with open('gpt_rewrite_out.txt', 'w') as file:
    file.write(translated)
