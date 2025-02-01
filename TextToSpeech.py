import speech_recognition as sr

def speech_to_text():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening... Speak now:")
        recognizer.adjust_for_ambient_noise(source)  # Reduce background noise
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError:
        print("Could not request results. Check your internet connection.")

if __name__ == "__main__":
    speech_to_text()