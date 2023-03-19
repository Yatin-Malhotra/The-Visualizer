import speech_recognition as sr

def speech_to_text():
    # create a recognizer object
    r = sr.Recognizer()


   
       # use the microphone as the audio source
       with sr.Microphone() as source:
           print("Speak now...")
           # adjust the ambient noise level to account for background noise
           r.adjust_for_ambient_noise(source)
           # listen for the user's voice input
           audio = r.listen(source)
           
       try:
           # recognize speech using Google Speech Recognition
           text = r.recognize_google(audio)
           print("You said: {}".format(text))
   
       except sr.UnknownValueError:
           print("Sorry, I didn't understand that.")
       except sr.RequestError:
           print("Sorry, could not request results from Google Speech Recognition.")

        
        return text


