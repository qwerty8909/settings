#!/usr/bin/python3

import openai
from flask import Flask, request, render_template
from deep_translator import GoogleTranslator

app = Flask(__name__, template_folder=r'C:\Users\vitalii\IdeaProjects\settings\vilomov\article_writer')
# app = Flask(__name__, template_folder='/home/project')


@app.route('/', methods=['GET', 'POST'])
def index():
    output_text = ''
    input_text = ''
    if request.method == 'POST':
        user_input = request.form['user_input']

        option1 = request.form.get('option1')
        option2 = request.form.get('option2')
        option3 = request.form.get('option3')
        option4 = request.form.get('option4')
        option5 = request.form.get('option5')

        openai.api_key = ("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")

        for item in user_input.split('\n'):
            translated_en = GoogleTranslator(source='ru', target='en').translate(item)
            input_text += translated_en

        prompt = 'Please ignore all previous instructions. I want you to respond only in language English. I ' \
                 'want you to act as a very proficient SEO and high end copy writer that speaks and writes ' \
                 'fluent English. Write the text as long as possible, the article must be 100 to 300 words. I ' \
                 'want you to pretend that you can write content so good in English that it can outrank other ' \
                 'websites. Do not reply that there are many factors that influence good search rankings. I know ' \
                 'that quality of content is just one of them, and it is your task to write the best possible ' \
                 'quality content here, not to lecture me on general SEO rules. Then I want you to write an ' \
                 'article in a formal that helps me outrank the article in Google. Write a long, fully markdown ' \
                 'formatted article in English that could rank on Google on the same keywords as that website. ' \
                 'Do not echo my prompt. Do not remind me what I asked you for. Do not apologize. Do not ' \
                 'self-reference. Do now use generic filler phrases. Get to the point precisely and accurate. Do ' \
                 'not explain what and why, just give me your best possible article. All output shall be in ' \
                 'English. Write the article as long as possible, the article must be 100 to 300 words. The ' \
                 'article must be on the following topic: '

        if option1:
            prompt = prompt + '\n- sports and everything related to sports. '
        if option2:
            prompt = prompt + '\n- football and all topics related to football. '
        if option3:
            prompt = prompt + '\n- hockey and all topics related to hockey. '
        if option4:
            prompt = prompt + '\n- forecasts and predictions and all topics related to forecasting and ' \
                              'predicting events. '
        if option5:
            prompt = prompt + '\n- news and all topics related to news. '

        content = input_text.replace('\n', ' ').replace('\t', '').replace('"', '').replace("'", "") \
            .replace('(', '').replace(')', '').replace('  ', ' ').replace('   ', ' ').replace(' .', '.')

        if len(content) > 1:
            prompt = prompt + '\nAnd most importantly, this article should be on the topic: ' + content
            prompt = prompt + '\nBut if the topics of the article cannot exist together and the article cannot ' \
                              'consider these topics together, then write "Indicate relevant topics"! \n'

            results = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                temperature=0.7,
                max_tokens=500,
                top_p=1,
                best_of=1,
                frequency_penalty=0.5,
                presence_penalty=0,
                stop=["//#"]
            )
            response = dict(results)
            openai_response = response['choices']
            eng_text = openai_response[-1]['text']

            output_text = GoogleTranslator(source='en', target='ru').translate(eng_text)

        else:
            output_text = 'Введите текст'

    else:
        user_input = None

    return render_template('article_generator.html', user_input=user_input, output=output_text)


if __name__ == '__main__':
    app.run(debug=True)
    # from waitress import serve
    # serve(app, host="88.218.169.217", port=8099)
