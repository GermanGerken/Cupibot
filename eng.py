from pygtrans import Translate

client = Translate()
text = client.translate('hello' , target='ru')
print(text.translatedText)