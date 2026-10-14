import ollama
import pyttsx3
import webbrowser
import urllib.parse
import subprocess



# ARIS MODEL


MODEL_NAME = "phi3.5:latest"

MAX_HISTORY = 10

USER_NAME = "Aayush"


# ARIS SPEAK


engine = pyttsx3.init()

engine.setProperty("rate", 170)
engine.setProperty("volume", 1.0)


def speak(text):

    print("ARIS:", text)

    try:

        engine.say(text)
        engine.runAndWait()

    except Exception as e:

        print(f"[Voice error: {e}]")





# ARIS COMMANDS


def handle_command(user_input):

    command = user_input.lower().strip()


    
    # OPEN YOUTUBE
    

    if command in [
        "open youtube",
        "youtube",
        "open youtube.com"
    ]:

        webbrowser.open("https://www.youtube.com")

        speak("Opening YouTube.")

        return True


    
    # OPEN GOOGLE
    

    if command in [
        "open google",
        "google",
        "open google.com"
    ]:

        webbrowser.open("https://www.google.com")

        speak("Opening Google.")

        return True


    
    # OPEN CALCULATOR
    

    if command in [
        "open calculator",
        "calculator",
        "open calc"
    ]:

        subprocess.Popen("calc.exe")

        speak("Opening Calculator.")

        return True


    
    # SEARCH YOUTUBE
    

    if command.startswith("search youtube for "):

        query = user_input[len("search youtube for "):].strip()

        if query:

            encoded_query = urllib.parse.quote_plus(query)

            url = (
                "https://www.youtube.com/results?search_query="
                + encoded_query
            )

            webbrowser.open(url)

            speak(f"Searching YouTube for {query}.")

            return True


    
    # SEARCH GOOGLE
    

    if command.startswith("search google for "):

        query = user_input[len("search google for "):].strip()

        if query:

            encoded_query = urllib.parse.quote_plus(query)

            url = (
                "https://www.google.com/search?q="
                + encoded_query
            )

            webbrowser.open(url)

            speak(f"Searching Google for {query}.")

            return True


    
    # COMMAND NOT FOUND
    

    return False



# OLLAMA CONVERSATION MEMORY


conversation = [

    {
        "role": "system",

        "content":
        "You are ARIS, a helpful lightweight desktop AI assistant. "
        "Keep responses simple, short and natural. "
        "Do not pretend to perform computer actions."
    }

]



# ASK OLLAMA


def ask_ai(user_input):

    conversation.append({

        "role": "user",

        "content": user_input

    })


    
    # KEEP MEMORY SMALL
    

    if len(conversation) > MAX_HISTORY + 1:

        conversation.pop(1)


    
    # ASK OLLAMA
    

    try:

        response = ollama.chat(

            model=MODEL_NAME,

            messages=conversation

        )

        answer = response["message"]["content"].strip()


        
        # SAVE AI RESPONSE
        

        conversation.append({

            "role": "assistant",

            "content": answer

        })


        return answer


    except Exception as e:

        print(f"[Ollama error: {e}]")

        return "I couldn't connect to my AI model."



# ARIS STARTUP


print()
print("==========================================")
print("           ARIS AI ASSISTANT")
print("==========================================")
print()

print("Model:", MODEL_NAME)
print("Status: Ready")

print()

print("Commands:")
print("  open YouTube")
print("  open Google")
print("  open Calculator")
print("  search YouTube for Minecraft")
print("  search Google for Python")
print("  exit")

print()



# MAIN LOOP


while True:

    try:

        user_input = input("YOU: ").strip()

    except (KeyboardInterrupt, EOFError):

        print()

        speak("Goodbye.")

        break


    
    # EMPTY INPUT
    

    if not user_input:

        continue


    
    # EXIT
    

    if user_input.lower() in [
        "exit",
        "quit",
        "goodbye"
    ]:

        speak("Goodbye.")

        break


    
    # DIRECT COMMAND ROUTER
    

    if handle_command(user_input):

        continue


    
    # OLLAMA AI FALLBACK
    

    print("ARIS is thinking...")

    answer = ask_ai(user_input)

    speak(answer)
    
    