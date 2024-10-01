import speech_recognition as sr
def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print(text)
        return text
    except sr.UnknownValueError:
        return "R"
    except sr.RequestError:
        return "E"


