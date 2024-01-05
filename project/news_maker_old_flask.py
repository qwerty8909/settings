#!/usr/bin/python3

import openai
from flask import Flask, request, render_template
from deep_translator import GoogleTranslator

app = Flask(__name__, template_folder='/home/project')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        with open('/home/project/gpt_rewrite_out.txt', 'w', encoding="utf-8") as file:
            file.write(' ')

        key_words = user_input
        openai.api_key = ("key")

        with open('/home/project/gpt_rewrite_in.txt', 'w', encoding="utf-8") as file:
            for item in key_words.split('\n'):
                translated_en = GoogleTranslator(source='ru', target='en').translate(item)
                file.write(translated_en + '\n')

        with open('/home/project/gpt_rewrite_in.txt', 'r', encoding="utf-8") as file:
            file_contents = file.read()
        with open('/home/project/gpt_rewrite_prompt.txt', 'r', encoding="utf-8") as file:
            file_prompt = file.read()

        content = file_contents.replace('\n', ' ').replace('\t', '').replace('"', '').replace("'", "") \
            .replace('(', '').replace(')', '').replace('  ', ' ').replace('   ', ' ').replace(' .', '.')
        results = openai.Completion.create(
            model="text-davinci-003",
            prompt=file_prompt + content + '.\n',
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

        translated_ru = GoogleTranslator(source='en', target='ru').translate(eng_text)
        with open('/home/project/gpt_rewrite_out.txt', 'w', encoding="utf-8") as file:
            file.write(translated_ru)
    else:
        user_input = None

    with open('/home/project/gpt_rewrite_out.txt', 'r', encoding="utf-8") as f:
        output = f.read()

    return render_template('article_generator.html', user_input=user_input, output=output)


if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=0000)
