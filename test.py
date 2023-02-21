from googletrans import Translator
translator= Translator()
output = translator.translate("iam a bad boy",dest='hi')
print(output)