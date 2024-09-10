import os
from flask import Flask, render_template
import dialogflow_api
from flask import Flask, request, jsonify
import translate


app = Flask(__name__)


@app.route("/")
def index(): 
    return render_template('index.html')



# Define a route for handling chatbot responses
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    print(user_input)
    res = translate.detect_and_translate(user_input)
    print(res)
    bot_response = dialogflow_api.run_sample([res])
    print(bot_response)
    final_return = translate.translate_to_english(bot_response)
    print(final_return)
    return jsonify({"response": final_return})



@app.route("/home")
def home():
    result = dialogflow_api.run_sample(["hi"])
    print (result)
    return result
    

@app.route('/get-last-4-digits', methods=['GET'])
def get_last_4_digits():
    print (request)
    print( type(request))
    phone_number = request.args.get('phone_number')
    
    if not phone_number:
        return jsonify({'error': 'Phone number is required'}), 400

    # Extract the last 4 digits
    last_4_digits = phone_number[-4:]

    # Convert last 4 digits to an integer for modulo operations
    last_4_digits_int = int(last_4_digits)

    # Initialize the message
    message = "Number is not divisible by 7 or 4"

    if last_4_digits_int % 7 == 0:
        message = "Number is divisible by 7"
    elif last_4_digits_int % 4 == 0:
        message = "Number is divisible by 4"

    # Return the last 4 digits and the message
    return jsonify({'last_4_digits': last_4_digits, 'message': message}), 200


@app.route("/api")
def display():
    result = [ {
    "name": "Adeel Solangi",
    "language": "Sindhi",
    "id": "V59OF92YF627HFY0",
    "bio": "Donec lobortis eleifend condimentum. Cras dictum dolor lacinia lectus vehicula rutrum. Maecenas quis nisi nunc. Nam tristique feugiat est vitae mollis. Maecenas quis nisi nunc.",
    "version": 6.1
  },
  {
    "name": "Afzal Ghaffar",
    "language": "Sindhi",
    "id": "ENTOCR13RSCLZ6KU",
    "bio": "Aliquam sollicitudin ante ligula, eget malesuada nibh efficitur et. Pellentesque massa sem, scelerisque sit amet odio id, cursus tempor urna. Etiam congue dignissim volutpat. Vestibulum pharetra libero et velit gravida euismod.",
    "version": 1.88
  }]
    return result



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))