from langdetect import detect
from deep_translator import GoogleTranslator

def detect_and_translate(query):
    global detected_language 
    # Detect the language of the input query
    detected_language = detect(query)
    print(f"Detected language: {detected_language}")
    
    # If the detected language is not English, translate it to English
    if detected_language != 'en':
        translator = GoogleTranslator(source=detected_language, target='en')
        translated = translator.translate(query)
        print(f"Original: {query}")
        print(f"Translated to English: {translated}")
        return translated
    else:
        print("No translation needed, the text is already in English.")
        return query

def translate_to_english(text):
    print("transale to english")
    print(type(text))
    print(f"Detected language: {detected_language}")
    
    if detected_language =="en":
        return text
    else:
        translator = GoogleTranslator(source="en", target=detected_language)
        translated = translator.translate(text[0])
        return translated
# Example usage:
# user_query = "హలో, ఎలా ఉన్నారు?"  # Replace with user input
# language = detect_and_translate(user_query)

