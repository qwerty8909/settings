#!/usr/bin/python3

import os
import glob
import pandas as pd
import openai
import random
from flask import Flask, request, render_template
from deep_translator import GoogleTranslator

from predict_parser import championat, ironbets, liveresult, stavkionline
from predict_parser import sportsru, soccer365, bookmakerratings
from predict_parser import stavkiprognozy, vseprosport, odds, metaratings

app = Flask(__name__, template_folder=r'C:\Users\vitalii\IdeaProjects\settings\parser\test\\') #

@app.route('/', methods=['GET', 'POST'])
def index():
    output_text = ''
    if request.method == 'POST':
        user_input = request.form['user_input']

        key_words = user_input.split()
        openai.api_key = ("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")

        path = r'/parser/test/data\\'  #
        csv_files = glob.glob(os.path.join(path, "*.csv"))
        df1 = pd.DataFrame()
        df2 = pd.DataFrame()
        for f in csv_files:
            df = pd.read_csv(f, sep=';')
            df1 = pd.concat([df1, df], ignore_index=True)

        df1.drop_duplicates(inplace = True)
        key_words = [item.lower() for item in key_words]
        df1.text = [item.lower() for item in df1.text]
        for line in df1.text:
            if all(word in line for word in key_words):
                df0 = df1[df1.text.str.contains(line)]
                df2 = pd.concat([df2, df0], axis=0).drop_duplicates()

        news = ''
        for link in sorted(df2.link, key=lambda _: random.random()):
            if len(news) < 6000:
                if 'championat.com' in link:
                    news += championat.site_parser(link)
                if 'ironbets.ru' in link:
                    news += ironbets.site_parser(link)
                if 'liveresult.ru' in link:
                    news += liveresult.site_parser(link)
                if 'stavki-online.info' in link:
                    news += stavkionline.site_parser(link)
                if 'stavkiprognozy.ru' in link:
                    news += stavkiprognozy.site_parser(link)
                if 'vseprosport.ru' in link:
                    news += vseprosport.site_parser(link)
                if 'odds.ru' in link:
                    news += odds.site_parser(link)
                if 'metaratings.ru' in link:
                    news += metaratings.site_parser(link)
                if 'sports.ru' in link:
                    news += sportsru.site_parser(link)
                if 'soccer365.ru' in link:
                    news += soccer365.site_parser(link)
                if 'bookmaker-ratings.ru' in link:
                    news += bookmakerratings.site_parser(link)

        input_text = ''
        for item in news.split('\n'):
            translated_en = GoogleTranslator(source='ru', target='en').translate(item)
            input_text += translated_en

        with open(r'/vilomov/gpt_rewrite_prompt.txt', 'r', encoding="utf-8") as file:
            file_prompt = file.read()

        content = input_text.replace('\n', ' ').replace('\t', '').replace('"', '').replace("'", "") \
            .replace('(', '').replace(')', '').replace('  ', ' ').replace('   ', ' ').replace(' .', '.')

        results = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", # gpt-4, gpt-4-0314, gpt-4-32k, gpt-4-32k-0314, gpt-3.5-turbo, gpt-3.5-turbo-0301
            messages=[
                {"role": "system", "content": "You are a very proficient SEO and high end copy writer."},
                {"role": "user", "content": file_prompt + content + '.\n'}
            ],
            temperature=0.7,
            max_tokens=1500,
            top_p=1,
            frequency_penalty=0.5,
            presence_penalty=0,
            stop=["//#"]
        )

        # results = openai.Completion.create(
        #     model="text-davinci-003",
        #     prompt=file_prompt + content + '.\n',
        #     temperature=0.7,
        #     max_tokens=1500,
        #     top_p=1,
        #     best_of=1,
        #     frequency_penalty=0.5,
        #     presence_penalty=0,
        #     stop=["//#"]
        # )
        # response = dict(results)
        # openai_response = response['choices']
        eng_text = results.choices[0].message['content']


        for item in eng_text.split('\n'):
            translated_ru = GoogleTranslator(source='en', target='ru').translate(item)
            output_text += translated_ru + '\n'

    else:
        user_input = None

    return render_template('index.html', user_input=user_input, output=output_text)


if __name__ == '__main__':
    app.run()
    # from waitress import serve
    # serve(app, host="88.218.169.217", port=8098)
