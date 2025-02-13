import os
import logging
from typing import Dict, Any
from flask import Flask, render_template, request, jsonify
from werkzeug.exceptions import BadRequest
import dialogflow_api
import translate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Configuration
class Config:
    PORT = int(os.environ.get("PORT", 8080))
    HOST = os.environ.get("HOST", "0.0.0.0")
    DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"

@app.route("/")
def index() -> str:
    """Render the main index page."""
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat() -> Dict[str, Any]:
    """
    Handle chat interactions with the bot.
    
    Returns:
        JSON response containing bot's reply
    """
    try:
        if not request.is_json:
            raise BadRequest("Content-Type must be application/json")

        user_input = request.json.get('message')
        if not user_input:
            raise BadRequest("Message field is required")

        logger.info(f"Received user input: {user_input}")
        
        # Process the message through translation and dialogflow
        translated_input = translate.detect_and_translate(user_input)
        logger.debug(f"Translated input: {translated_input}")
        
        bot_response = dialogflow_api.run_sample([translated_input])
        logger.debug(f"Bot response: {bot_response}")
        
        final_response = translate.translate_to_english(bot_response)
        logger.info(f"Final response: {final_response}")
        
        return jsonify({"response": final_response}), 200

    except BadRequest as e:
        logger.error(f"Bad request error: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

@app.route("/home")
def home() -> str:
    """Test endpoint for dialogflow."""
    try:
        result = dialogflow_api.run_sample(["hi"])
        logger.info(f"Home endpoint response: {result}")
        return result, 200
    except Exception as e:
        logger.error(f"Error in home endpoint: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

@app.route('/get-last-4-digits', methods=['GET'])
def get_last_4_digits() -> Dict[str, Any]:
    """
    Extract and analyze the last 4 digits of a phone number.
    
    Returns:
        JSON response with last 4 digits and divisibility message
    """
    try:
        phone_number = request.args.get('phone_number')
        
        if not phone_number:
            raise BadRequest("Phone number is required")
        
        if not phone_number.isdigit():
            raise BadRequest("Phone number must contain only digits")

        if len(phone_number) < 4:
            raise BadRequest("Phone number must be at least 4 digits long")

        last_4_digits = phone_number[-4:]
        last_4_digits_int = int(last_4_digits)

        message = "Number is not divisible by 7 or 4"
        if last_4_digits_int % 7 == 0:
            message = "Number is divisible by 7"
        elif last_4_digits_int % 4 == 0:
            message = "Number is divisible by 4"

        return jsonify({
            'last_4_digits': last_4_digits,
            'message': message
        }), 200

    except BadRequest as e:
        logger.error(f"Bad request error: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error processing phone number: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

@app.route("/api")
def display() -> Dict[str, Any]:
    """Return sample API data."""
    try:
        result = [
            {
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
            }
        ]
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error in display endpoint: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors."""
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {error}", exc_info=True)
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    logger.info(f"Starting application on {Config.HOST}:{Config.PORT}")
    app.run(
        debug=Config.DEBUG,
        host=Config.HOST,
        port=Config.PORT
    )