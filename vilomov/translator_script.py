from deep_translator import (GoogleTranslator)

with open('translator_in.txt', 'r') as file:
       file_contents = file.read()

translated = GoogleTranslator(source='en', target='ru').translate(file_contents)

with open('translator_out.txt', 'w') as file:
       file.write(translated)