import pyttsx3

def talk(text):

    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Speed of speech (words per minute)
    engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)

    text1 = ' '.join(word.capitalize() for word in text.split())

    engine.say(text)
    engine.runAndWait()
