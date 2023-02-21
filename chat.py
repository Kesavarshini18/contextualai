import random
import json
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
import torch
import pyttsx3
import speech_recognition as sr
from googletrans import Translator


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "kv"

def get_response(msg):
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]
   
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                if intent["tag"]=="location":
                    # g = geocoder.ip('me')
                    # return (g.latlng)
                    
                    from selenium import webdriver
                    from selenium import webdriver
                    from selenium.webdriver.chrome.options import Options
                    from selenium.webdriver.support.ui import WebDriverWait


                    def getLocation():
                      chrome_options = Options()
                      chrome_options.add_argument("--use-fake-ui-for-media-stream")
                      timeout = 5
                      driver = webdriver.Chrome(chrome_options=chrome_options)
                      driver.get("https://maps.google.com/")
                      wait = WebDriverWait(driver, timeout)
                      longitude = driver.find_elements_by_xpath('//*[@id="longitude"]')
                      longitude = [x.text for x in longitude]
                      longitude = str(longitude[0])
                      latitude = driver.find_elements_by_xpath('//*[@id="latitude"]')
                      latitude = [x.text for x in latitude]
                      latitude = str(latitude[0])
                      driver.quit()
                      return (latitude,longitude)
                    print(getLocation())
                    return "my location has been shared through google map live location"          
                return random.choice(intent['responses'])
            
               
    print(1)       
     
    if(1):
        engine = pyttsx3.init()
        n=engine.say(msg)
        engine.runAndWait()
        engine = None
        r = sr.Recognizer()
        while(1):
            try:
              with sr.Microphone() as source2:
                   r.adjust_for_ambient_noise(source2, duration=0.2)
                   audio2 = r.listen(source2)
                   MyText = r.recognize_google(audio2)
                   MyText = MyText.lower()
                  
                   return MyText
            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))
         
            except sr.UnknownValueError:
                print("unknown error occurred")

# def trans_resp(msg,lang):
#     translator= Translator()
#     output = translator.translate(msg ,dest=lang)
#     return output  



if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    lang=input("enter the lang code:")
    while True:
        # sentence = "do you use credit cards?"
        sentence = input("You: ")
        
        if sentence == "quit":
            break
        
        resp = get_response(sentence)
        # translator = Translator()
        # output = translator.translate(resp, dest=lang)
        # print(output)
        
        # translator= Translator()
        # output = translator.translate(resp, dest=lang)
        # print(output)  
        # ln= trans_resp(resp,lang)
        # print(ln)
        

