import text_speech as ts
import datetime
import indents
import random
import webbrowser
import re
import json
import os
import subprocess
import requests
import sys

def is_network_available():
    try:
        response = requests.get('https://www.google.com', timeout=10)
        return True if response.status_code == 200 else False
    except requests.ConnectionError:
        return False

def import_pywhatkit():
    if is_network_available():
        import pywhatkit
    else:
        ts.talk("No Internet Connection. Cannot Import PyWhatKit. Connect to the Internet")
        sys.exit(1)

def is_website_link(url):
    return url.startswith(("http://www.", "https://www."))

def load_custom_commands():
    global custom_commands_file
    custom_commands_file = "custom_commands.json"
    global custom_commands
    custom_commands = []
    if os.path.exists(custom_commands_file):
        with open(custom_commands_file, "r") as file:
            custom_commands = [json.loads(line)['name'].lower() for line in file]
            print(custom_commands)

def load_custom_commands_urls():
    global commands_urls
    if os.path.exists(custom_commands_file):
        with open(custom_commands_file, "r") as file:
            commands_urls = [json.loads(line)['url'] for line in file]
            print(commands_urls)


def ai(command):
    try:
        import_pywhatkit()
    except SystemExit:
        return
    command = command.lower()
    load_custom_commands()
    load_custom_commands_urls()
    if any(neg_word in command for neg_word in indents.negative):
        ts.talk("Okay. Tell Me Another Command")
        return
    else:
        if any(intent in command for intent in custom_commands):
            ccommand = indents.find(command, custom_commands)
            action = commands_urls[custom_commands.index(ccommand)]
            print(action)
            print(is_website_link(action))
            if is_website_link(action):
                try:
                    ts.talk("Opening" + ccommand)
                    webbrowser.open(action)
                except:
                    print("Invalid Link. Enter A Valid Link")
                    ts.talk("Invalid Link. Enter A Valid Link")
                return


            elif (".exe" in action or ".msi" in action or ".bat" in action):
                ts.talk("Opening App")
                cmd = f'"{action}"'
                result = subprocess.run(f'"{cmd}"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if result.returncode != 0:
                    stderr_output = result.stderr.decode().lower()
                    print(stderr_output)
                    ts.talk("Cannot Open This File")
                    return
                return
            elif ".ps1" in action:
                ts.talk("Opening App")
                cmd = f'powershell -Command "& ""{action}"""'
                result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if result.returncode != 0:
                    stderr_output = result.stderr.decode().lower()
                    print(stderr_output)
                    ts.talk("Cannot Open This File")
                    return
                return
            else:
                ts.talk("Proceeding with the Command")
                cmd = f'"{action}"'
                result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print(result)
                stderr_output = result.stderr.decode().lower()
                if "not recognized as an internal or external command" in result.stderr.decode():
                    cmd = f'powershell -Command "& ""{action}"""'
                    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    print(result)
                    if "not recognized as the name of a cmdlet, function, script file, or operable program" in result.stderr.decode():
                        print("Enter a Valid CMD or Powershell Command")
                        ts.talk("Enter a Valid CMD or Powershell Command")
                        return
                    return
                return
            return

        elif ("your name" in command or ("introduc" in command and "yourself" in command) or ("who" in command and "you" in command)):
            ts.talk("My name is Aurora")
            return
        elif "your creator" in command or "made you" in command:
            creator = ["Michelle", "Phantom", "Aurora", "Systemmaniac", "Xyrin"]
            ts.talk("My Creator Is" + random.choice(creator))
            return
        elif any(intent in command for intent in indents.song):
            word = indents.find(command,indents.song)
            song = command[command.index(word) + len(word):].strip()
            ts.talk('playing ' + song)
            pywhatkit.playonyt(song)
            return
        elif 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            ts.talk('Current time is ' + time)
            return
        elif any(intent in command for intent in indents.search):
            if any(intent in command for intent in indents.rsearch):
                word = indents.find(command, indents.rsearch)
                search_query = command[command.index(word) + len(word):].strip()
            else:
                search_query = command
            ts.talk(f'Browsing for {search_query}')
            webbrowser.open(f"https://www.google.com/search?q={search_query}")
            return
        elif any(intent in command for intent in indents.invoke):
            word = indents.find(command, indents.invoke)
            if any(intent in command for intent in indents.websites):
                website = indents.find(command, indents.websites)
                if website in indents.websites:
                    link = indents.weblinks[indents.websites.index(website)]
                    ts.talk("Opening " + website)
                    webbrowser.open(link)
            elif any(intent in command for intent in indents.apps):
                app = indents.find(command, indents.apps)
                if app in indents.apps:
                    cmd = indents.appcommand[indents.apps.index(app)]
                    ts.talk("Opening " + app)
                    os.system(f'cmd /c "{cmd}"')
            else:
                websearch = command[command.index(word) + len(word):].strip()
                ts.talk("Opening " + websearch)
                webbrowser.open(f"https://www.google.com/search?q={websearch}")
                return
        elif 'troubleshooter' in command or 'troubleshoot' in command:
            if any(intent in command for intent in indents.troubleshooters):
                troubleshooter = indents.find(command, indents.troubleshooters)
                if troubleshooter in indents.troubleshooters:
                    cmd = indents.tcommands[indents.troubleshooters.index(troubleshooter)]
                    ts.talk("Opening" + troubleshooter + "Troubleshooter")
                    os.system(f'cmd /c "{cmd}"')
            else:
                ts.talk('Cannot Open The Specified Troubleshooter. Opening Settings')
                os.system('cmd /c "start ms-settings:"')
            return
        elif 'shut down' in command or 'terminate' in command:
            if any(intent in command for intent in indents.devices):
                ts.talk("Shutting Down System")
                os.system('cmd /c "shutdown /s /f /t 0"')
            return
        elif 'restart' in command:
            if any(intent in command for intent in indents.devices):
                ts.talk("Restarting System")
                os.system('cmd /c "shutdown /r /f /t 0"')
            return
        elif 'sleep' in command:
            if any(intent in command for intent in indents.devices):
                ts.talk("Putting System to Sleep")
                os.system('cmd /c "rundll32.exe powrprof.dll,SetSuspendState 0,1,0"')
            return
        elif 'log out' in command or 'sign out' in command or 'log off' in command:
            ts.talk('Logging Out')
            os.system('cmd /c "shutdown /l"')
            return
        elif 'update' in command:
            if any(intent in command for intent in indents.devices):
                ts.talk("Updating System")
                os.system('cmd /c "UsoClient ScanInstallWait"')
            elif "app" in command:
                ts.talk("Updating All Apps")
                os.system('cmd /c "winget upgrade -h -all"')
            return
        elif 'enable' in command or 'turn on' in command:
            if any(intent in command for intent in indents.edparams):
                param = indents.find(command, indents.edparams)
                if param in indents.edparams:
                    cmd = indents.enablecommands[indents.edparams.index(param)]
                    ts.talk(param + " Enabled Successfully")
                    os.system(f'cmd /c "{cmd}"')
            return
        elif 'disable' in command or 'turn off' in command:
            if any(intent in command for intent in indents.edparams):
                param = indents.find(command, indents.edparams)
                if param in indents.edparams:
                        cmd = indents.disablecommands[indents.edparams.index(param)]
                        ts.talk(param + " Disabled Successfully")
                        os.system(f'cmd /c "{cmd}"')
            return
        elif 'desktop background' in command or 'desktop wallpaper' in command:
            ts.talk("Set the Desktop Wallpaper Manually")
            os.system(f'cmd /c "start ms-settings:personalization-background"')
            return
        elif 'login background' in command or 'login wallpaper' in command:
            ts.talk("Set the Login Wallpaper Manually")
            os.system(f'cmd /c "start ms-settings:lockscreen"')
            return
        elif ('apply' in command or 'set' in command) and 'theme' in command:
            ts.talk("Set the Theme Manually")
            os.system(f'cmd /c "start ms-settings:personalization"')
            return
        else:
            ts.talk(random.choice(indents.ucr))
