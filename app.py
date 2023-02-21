from waitress import serve
from flask import Flask, render_template, request, jsonify
from chat import get_response
from googletrans import Translator
import json

app= Flask(__name__)



# @app.route("/",method=["GET"])
@app.get("/")
def index_get():
    return render_template("base.html")


class Translated:
    def __init__(self, text, language):
        translator= Translator()
        try:
          ott =translator.translate(text ,dest=language)
          self.text = ott.text
          self.language = language
          
        except:
            self.text = "Sorry, translation failed."
            self.language = "en"
            
    def to_dict(self):
        return {"text":self.text, "language": self.language}


              
@app.post("/predict")
def predict():
   
    # lang = input("Enter your convenient language code: eg(hindi=hi or english=en)")
   
    # text = request.form.get("message")
    
    
    # text = request.get_json().get("message")
    # lang = request.form.get("language")
    data = request.get_json()
    text = data['message']
    lang = data['lang']
    
    
    response = get_response(text)
    

    output = Translated(response, lang)
    translated_dict = output.to_dict()
    
    # convert dictionary to json
    json_output = json.dumps(translated_dict)
    
    # convert json back to a dictionary
    dict_output = json.loads(json_output)
    
    # extract the translated text from the dictionary
    translated_text = dict_output["text"]
    
    message = {"answer": translated_text}
    return jsonify(message)



if __name__=="__main__":
    
    serve(app, host='0.0.0.0', port=5000)
    app.run(debug=True)
    
    
    
    