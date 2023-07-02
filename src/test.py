from deep_translator import GoogleTranslator
import pyttsx3



def translate(data, language):
    translated = GoogleTranslator(source='auto', target=language).translate(data)
    return translated



print(translate('Hello world', 'uk'))




engine = pyttsx3.init()
engine.say('Привіт як справи?')
engine.runAndWait()