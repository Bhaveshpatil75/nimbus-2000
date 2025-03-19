import speech_recognition as sr
import pyttsx3
import pywhatkit
import os
import datetime
import pvporcupine
import pyaudio
import numpy as np
import private

engine = pyttsx3.init()
engine.setProperty('rate', 170)  
engine.setProperty('volume', 1.0)

def speak(text):
    """Convert text to speech"""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen for user command after wake word"""
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True 

    with sr.Microphone() as source:
        print("Listening for command...")
        try:
            audio = recognizer.listen(source, timeout=5) 
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.WaitTimeoutError:
            print("No command detected. Returning to wake word detection...")
            return "error1"  
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand.")
            return "error2"
        except sr.RequestError:
            print("Speech recognition service is unavailable.")
            return ""
        except:
            return ""


def execute_command(command):
    """Process the voice command"""
    
    if "open youtube" in command:
        speak("Opening YouTube")
        pywhatkit.playonyt("trending videos")
    elif "play" in command:
        song = command.replace("play", "").strip()
        speak(f"Playing {song}")
        pywhatkit.playonyt(song)
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {current_time}")
    elif "open chrome" in command:
        speak("Opening Google Chrome")
        os.system("start chrome")
    elif "shutdown" in command:
        speak("Shutting down your computer")
        os.system("shutdown /s /t 5")
    elif "exit" in command:
        speak("Goodbye!")
        exit()
    elif command=='error1':
        speak('say something')
    elif command=='error2':
        speak("I didn't understand. Please repeat.")
    else:
        speak('Sorry, I am not feeling well now')

def detect_wake_word():
    """Continuously listen for the wake word and respond"""
    porcupine = pvporcupine.create(
        access_key=private.access_key,
          keyword_paths=["Hey-Nimbus.ppn"])
    pa = pyaudio.PyAudio()

    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=porcupine.sample_rate, 
                 input=True, frames_per_buffer=porcupine.frame_length)

    print("Say 'Hey Nimbus' to activate...")

    while True:
        pcm = np.frombuffer(stream.read(porcupine.frame_length), dtype=np.int16)
        keyword_index = porcupine.process(pcm)
        if keyword_index >= 0:
            print("Wake word detected!")
            speak("Hello bhavesh, how can I help you?")
            command = listen()
            if command:
                execute_command(command)
            else:
                print("Waiting for next wake word...")

if __name__ == "__main__":
    detect_wake_word()
