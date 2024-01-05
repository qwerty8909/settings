#!/usr/bin/python3

import openai
from flask import Flask, request, render_template
from deep_translator import GoogleTranslator

from predict_parser import championat, ironbets, liveresult, stavkionline
from predict_parser import sportsru, soccer365, bookmakerratings
from predict_parser import stavkiprognozy, vseprosport, odds, metaratings

# app = Flask(__name__, template_folder=r'C:\Users\vitalii\IdeaProjects\settings\vilomov\article_writer')
app = Flask(__name__, template_folder='/home/project')


@app.route('/', methods=['GET', 'POST'])
def index():
    output_text = ''
    input_text = ''
    links = []
    if request.method == 'POST':
        user_input = request.form['user_input']
        user_input += '\n'

        option1 = request.form.get('option1')
        option2 = request.form.get('option2')
        option3 = request.form.get('option3')
        option4 = request.form.get('option4')
        option5 = request.form.get('option5')

        openai.api_key = ("key")

        if option1:
            links.append(option1)
        if option2:
            links.append(option2)
        if option3:
            links.append(option3)
        if option4:
            links.append(option4)
        if option5:
            links.append(option5)

        for link in links:
            if 'championat.com' in link:
                user_input += championat.site_parser(link)
            if 'ironbets.ru' in link:
                user_input += ironbets.site_parser(link)
            if 'liveresult.ru' in link:
                user_input += liveresult.site_parser(link)
            if 'stavki-online.info' in link:
                user_input += stavkionline.site_parser(link)
            if 'stavkiprognozy.ru' in link:
                user_input += stavkiprognozy.site_parser(link)
            if 'vseprosport.ru' in link:
                user_input += vseprosport.site_parser(link)
            if 'odds.ru' in link:
                user_input += odds.site_parser(link)
            if 'metaratings.ru' in link:
                user_input += metaratings.site_parser(link)
            if 'sports.ru' in link:
                user_input += sportsru.site_parser(link)
            if 'soccer365.ru' in link:
                user_input += soccer365.site_parser(link)
            if 'bookmaker-ratings.ru' in link:
                user_input += bookmakerratings.site_parser(link)

        for item in user_input.split('\n'):
            translated_en = GoogleTranslator(source='ru', target='en').translate(item)
            input_text += translated_en

        content = input_text.replace('\n', ' ').replace('\t', '').replace('"', '').replace("'", "") \
            .replace('(', '').replace(')', '').replace('  ', ' ').replace('   ', ' ').replace(' .', '.')

        # with open(r'/vilomov/article_writer/gpt_rewrite_prompt.txt', 'r', encoding="utf-8") as file:
        with open('/home/project/gpt_rewrite_prompt.txt', 'r', encoding="utf-8") as file:
            prompt = file.read()

        if len(content) > 1:

            results = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt + content + '.\n',
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

            output_text = GoogleTranslator(source='en', target='ru').translate(eng_text)

        else:
            output_text = 'Введите текст или вставьте ссылку'

    else:
        user_input = None

    return render_template('news_maker.html', user_input=user_input, output=output_text)


if __name__ == '__main__':
    # app.run(debug=True)
    from waitress import serve
    serve(app, host="0.0.0.0", port=0000)
