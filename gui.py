import customtkinter
import psutil
import GPUtil
import wmi
import platform
import tkinter as tk
from psutil import virtual_memory
from PIL import Image
import json
import os
import random
import speech_text
import ai

# Global variables for StringVars
theme_var = None
appearance_var = None
commands = []

custom_commands_file = "custom_commands.json"
mode_file = "mode.json"


# Function to load custom commands from the JSON file
def load_custom_commands():
    if os.path.exists(custom_commands_file):
        with open(custom_commands_file, "r") as file:
            for line in file:
                try:
                    command = json.loads(line.strip())
                    commands.append(command)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON from line: {line}, error: {e}")


# Function to save custom commands to the JSON file
def save_custom_commands():
    with open(custom_commands_file, "w") as file:
        for command in commands:
            file.write(json.dumps(command) + "\n")


# Function to load the saved theme preference
def load_theme_preference():
    if os.path.exists("theme_preference.json"):
        with open("theme_preference.json", "r") as file:
            return json.load(file).get("theme")
    return None


# Function to save the theme preference
def save_theme_preference(theme):
    with open("theme_preference.json", "w") as file:
        json.dump({"theme": theme}, file)


# Function to load the saved appearance mode preference
def load_mode_preference():
    if os.path.exists(mode_file):
        with open(mode_file, "r") as file:
            return json.load(file).get("mode", "System")
    else:
        save_mode_preference("System")
        return "System"


# Function to save the appearance mode preference
def save_mode_preference(mode):
    with open(mode_file, "w") as file:
        json.dump({"mode": mode}, file)


# Function to get system information
def get_system_info():
    info = {
        "cpu": {},
        "ram": {},
        "gpu": [],
        "others": {}
    }

    # Get CPU information
    cpu_info = wmi.WMI().Win32_Processor()[0]
    info["cpu"]["name"] = cpu_info.Name
    info["cpu"]["cores"] = cpu_info.NumberOfCores
    info["cpu"]["threads"] = psutil.cpu_count(logical=True)
    info["cpu"]["current_speed"] = cpu_info.CurrentClockSpeed / 1000  # Convert MHz to GHz
    info["cpu"]["architecture"] = platform.architecture()[0]

    # Get RAM information
    sys_info = wmi.WMI().Win32_ComputerSystem()[0]
    mem_info = virtual_memory()
    # info["ram"]["type"] = wmi.WMI().Win32_PhysicalMemory()[0].MemoryType
    info["ram"]["speed"] = wmi.WMI().Win32_PhysicalMemory()[0].Speed
    info["ram"]["total"] = mem_info.total

    # Get GPU information
    gpus = GPUtil.getGPUs()
    for gpu in gpus:
        info["gpu"].append({
            "name": gpu.name,
            "total_memory": gpu.memoryTotal,
            "load": gpu.load * 100,
        })

    # DirectX information
    info["directx_version"] = "DirectX 12"  # Assuming DirectX 12 for modern systems, customize as needed

    return info


# Function to create a frame displaying system information
def create_info_frame(root):
    info_frame = customtkinter.CTkFrame(master=root, border_width=2)
    info_frame.pack(side="right", padx=10, pady=10, fill="y")

    info = get_system_info()

    # Center-align and set font size
    label_font = ("Arial", 18, "bold")
    text_font = ("Arial", 14)

    # CPU Information
    cpu_label = customtkinter.CTkLabel(master=info_frame, text="CPU Information", font=label_font)
    cpu_label.pack(anchor="center")
    cpu_text = f"""Model: {info['cpu']['name']}
Cores: {info['cpu']['cores']}
Threads: {info['cpu']['threads']}
Current Speed: {info['cpu']['current_speed']} GHz
Architecture: {info['cpu']['architecture']}"""
    cpu_details = customtkinter.CTkLabel(master=info_frame, text=cpu_text, font=text_font)
    cpu_details.pack(anchor="center", pady=5)

    # RAM Information
    ram_label = customtkinter.CTkLabel(master=info_frame, text="RAM Information", font=label_font)
    ram_label.pack(anchor="center")
    ram_text = f"""Speed: {info['ram']['speed']} MHz
Total: {info['ram']['total'] / (1024 ** 3):.2f} GB"""
    ram_details = customtkinter.CTkLabel(master=info_frame, text=ram_text, font=text_font)
    ram_details.pack(anchor="center", pady=5)

    # GPU Information (only if detected)
    if info['gpu']:
        for i, gpu in enumerate(info['gpu'], 1):
            gpu_label = customtkinter.CTkLabel(master=info_frame, text=f"GPU Information {i}", font=label_font)
            gpu_label.pack(anchor="center")
            gpu_text = f"""Name: {gpu['name']}
Total VRAM: {gpu['total_memory']} MB
Load: {gpu['load']}%"""
            gpu_details = customtkinter.CTkLabel(master=info_frame, text=gpu_text, font=text_font)
            gpu_details.pack(anchor="center", pady=5)

    # DirectX Information
    directx_label = customtkinter.CTkLabel(master=info_frame, text="DirectX Information", font=label_font)
    directx_label.pack(anchor="center", pady=5)
    directx_text = f"DirectX Version: {info['directx_version']}"
    directx_details = customtkinter.CTkLabel(master=info_frame, text=directx_text, font=text_font)
    directx_details.pack(anchor="center")


# Function to create a frame for usage bars
def create_progress_frame(root):
    prog_frame = customtkinter.CTkFrame(master=root, border_width=2)
    prog_frame.pack(side="left", padx=10, pady=10, fill="y")

    # Function to update progress bars periodically
    def update_progress():
        cpu_usage = psutil.cpu_percent(interval=0.5)
        ram_usage = psutil.virtual_memory().percent

        cpu_bar.set(cpu_usage / 100.0)
        cpu_percent_label.configure(text=f"{cpu_usage}%")

        ram_bar.set(ram_usage / 100.0)
        ram_percent_label.configure(text=f"{ram_usage}%")

        root.after(250, update_progress)

    # Center-align and set font size
    label_font = ("Arial", 14, "bold")
    text_font = ("Arial", 12)

    # CPU Usage
    cpu_label = customtkinter.CTkLabel(master=prog_frame, text="CPU Usage", font=label_font)
    cpu_label.pack(anchor="center")
    cpu_bar = customtkinter.CTkProgressBar(master=prog_frame, orientation="horizontal", width=300)
    cpu_bar.pack(anchor="center", pady=5)
    cpu_percent_label = customtkinter.CTkLabel(master=prog_frame, text="")
    cpu_percent_label.pack(anchor="center")

    # RAM Usage
    ram_label = customtkinter.CTkLabel(master=prog_frame, text="RAM Usage", font=label_font)
    ram_label.pack(anchor="center", pady=10)
    ram_bar = customtkinter.CTkProgressBar(master=prog_frame, orientation="horizontal", width=300)
    ram_bar.pack(anchor="center", pady=5)
    ram_percent_label = customtkinter.CTkLabel(master=prog_frame, text="")
    ram_percent_label.pack(anchor="center")

    update_progress()  # Initial call to start updating progress bars


# List all .json theme files in the themes folder
themes_folder = "themes"
if not os.path.exists(themes_folder):
    os.makedirs(themes_folder)
themes = [f for f in os.listdir(themes_folder) if f.endswith(".json")]


# Function to change the theme
def change_theme(selected_theme):
    theme_path = os.path.join(themes_folder, selected_theme)
    print(f"Changing theme to: {theme_path}")  # Debugging statement
    customtkinter.set_default_color_theme(theme_path)
    save_theme_preference(selected_theme)
    print("Theme saved.")  # Debugging statement

    # Update the theme variable to ensure the text updates
    theme_var.set(selected_theme)

    # Re-initialize the entire application with the new theme
    reinitialize_app()


# Function to change the appearance mode
def change_appearance_mode(mode):
    customtkinter.set_appearance_mode(mode)
    save_mode_preference(mode)


# Function to simulate send action
def send_message(event=None):
    print("Send button pressed or Enter key pressed.")
    global text_box
    text = text_box.get()
    print(text)
    if text:
        ai.ai(text)
        text_box.delete(0, tk.END)

def handle_voice_command():
    ai.ai(speech_text.listen())


# Function to refresh the UI by reinitializing everything
def initialize_ui(root):
    global text_box
    for widget in root.winfo_children():
        widget.destroy()

    # Load the images using PIL
    voice_icon_image = Image.open("images/voice_icon.png")
    send_icon_image = Image.open("images/send_icon.png")

    # Create a transparent frame at the bottom of the window
    bottom_frame = customtkinter.CTkFrame(master=root, width=1024, height=50)
    bottom_frame.pack(side="bottom", fill="x")

    # Create a sub-frame for the input area to contain the voice button, text box and send button together
    input_frame = customtkinter.CTkFrame(master=bottom_frame)
    input_frame.pack(side="top", pady=5)

    # Add the voice command button to the left of the text box
    voice_button = customtkinter.CTkButton(master=input_frame,
                                           width=50,
                                           height=50,
                                           image=customtkinter.CTkImage(voice_icon_image.convert("RGBA")),
                                           text="",
                                           command=handle_voice_command)
    voice_button.pack(side="left", padx=(0, 10))

    # Add the text box to the middle of the input frame
    text_box = customtkinter.CTkEntry(master=input_frame,
                                      width=600,  # Adjust width to fit window
                                      height=50,
                                      placeholder_text="Type your message here...")
    text_box.pack(side="left", expand=True)

    # Add the send button to the right of the text box
    send_button = customtkinter.CTkButton(master=input_frame,
                                          width=50,
                                          height=50,
                                          image=customtkinter.CTkImage(send_icon_image.convert("RGBA")),
                                          text="",
                                          command=send_message)
    send_button.pack(side="left", padx=(10, 0))

    # Bind the Enter key to the send_message function
    text_box.bind("<Return>", send_message)

    # Add a frame for dropdown menus and make it transparent
    dropdown_frame = customtkinter.CTkFrame(master=root, fg_color="transparent")
    dropdown_frame.pack(side="top", anchor="ne", padx=10, pady=10)

    # Add a dropdown (combobox) for appearance mode selection to the left of the theme selection box
    appearance_combobox = customtkinter.CTkOptionMenu(master=dropdown_frame,
                                                      values=["System", "Light", "Dark"],
                                                      command=change_appearance_mode,
                                                      variable=appearance_var)
    appearance_combobox.pack(side="left", padx=10)

    # Add a dropdown (combobox) for theme selection
    theme_combobox = customtkinter.CTkOptionMenu(master=dropdown_frame,
                                                 values=themes,
                                                 command=change_theme,
                                                 variable=theme_var)
    theme_combobox.pack(side="left")

    # Add a button to the top center to add new commands
    add_command_button = customtkinter.CTkButton(master=root,
                                                 text="Add Command",
                                                 command=show_add_command_window)
    add_command_button.pack(side="top", pady=10)

    # Create a scrollable frame to display the commands
    global central_frame, canvas
    central_frame = customtkinter.CTkScrollableFrame(master=root, width=620, height=int(root.winfo_height() * 0.5))
    central_frame.pack(side="top", anchor="c", pady=20)

    # Add device info frame below central frame
    create_device_info_frame(root)

    # Add commands to the central frame
    refresh_commands_ui()

    # Create the hardware information frame
    create_info_frame(root)

    # Create the progress bars frame
    create_progress_frame(root)

# Function to get device information
def get_device_info():
    os_info = platform.uname()
    device_info = {
        "name": os_info.node,
        "system": os_info.system,
        "version": os_info.version,
        "release": os_info.release,
        "build": os_info.version,  # Assuming build refers to the version here
    }
    return device_info


# Function to create a frame displaying device information
def create_device_info_frame(root):
    device_info_frame = customtkinter.CTkFrame(master=root, width=768, height=600, border_width=2)
    device_info_frame.pack(side="top", anchor="center", pady=20)

    device_info = get_device_info()
    label_font = ("Arial", 18, "bold")
    text_font = ("Arial", 14)

    # Device Information
    device_label = customtkinter.CTkLabel(master=device_info_frame, text="Device Information", font=label_font)
    device_label.pack(anchor="center")
    device_text = f"""Device Name: {device_info['name']}
OS Name: {device_info['system']}
Version: {device_info['version']}
Release: {device_info['release']}
Build: {device_info['build']}"""
    device_details = customtkinter.CTkLabel(master=device_info_frame, text=device_text, font=text_font)
    device_details.pack(anchor="center", pady=5)


# Function to dynamically refresh the commands UI
def refresh_commands_ui():
    for widget in central_frame.winfo_children():
        widget.destroy()

    for command in commands:
        command_frame = customtkinter.CTkFrame(master=central_frame)
        command_frame.pack(fill="x", pady=5)

        command_label = customtkinter.CTkLabel(master=command_frame, text=command["name"])
        command_label.pack(side="left", padx=10)

        edit_button = customtkinter.CTkButton(master=command_frame, text="Edit",
                                              command=lambda c=command: show_edit_command_window(c))
        edit_button.pack(side="right", padx=5)

        delete_button = customtkinter.CTkButton(master=command_frame, text="Delete",
                                                command=lambda c=command: delete_command(c))
        delete_button.pack(side="right")


# Function to show a window to add a new command
def show_add_command_window():
    add_window = customtkinter.CTkToplevel(root)
    add_window.title("Add Command")
    add_window.geometry("400x250")
    add_window.grab_set()  # Ensure window stays on top

    url_label = customtkinter.CTkLabel(master=add_window, text="Web URL/File Path/CMD Command/Powershell Command:")
    url_label.pack(pady=10)
    url_entry = customtkinter.CTkEntry(master=add_window, width=300)
    url_entry.pack(pady=5)

    command_label = customtkinter.CTkLabel(master=add_window, text="Command:")
    command_label.pack(pady=10)
    command_entry = customtkinter.CTkEntry(master=add_window, width=300)
    command_entry.pack(pady=5)

    def add_command_confirmed(event=None):
        if (2 <= len(url_entry.get()) <= 100) and (2 <= len(command_entry.get()) <= 100):
            commands.append({"name": command_entry.get(), "url": url_entry.get()})
            save_custom_commands()
            refresh_commands_ui()
            add_window.destroy()
        else:
            messagebox.showwarning("Invalid Input", "Both fields must be between 2 and 100 characters long!")

    enter_button = customtkinter.CTkButton(master=add_window, text="Enter", command=add_command_confirmed)
    enter_button.pack(pady=20)

    # Bind Enter key to add command
    add_window.bind("<Return>", add_command_confirmed)


# Function to show a window to edit an existing command
def show_edit_command_window(command):
    edit_window = customtkinter.CTkToplevel(root)
    edit_window.title("Edit Command")
    edit_window.geometry("400x250")
    edit_window.grab_set()  # Ensure window stays on top

    url_label = customtkinter.CTkLabel(master=edit_window, text="Web URL/File Path/CMD Command/Powershell Command:")
    url_label.pack(pady=10)
    url_entry = customtkinter.CTkEntry(master=edit_window, width=300)
    url_entry.pack(pady=5)
    url_entry.insert(0, command["url"])

    command_label = customtkinter.CTkLabel(master=edit_window, text="Command:")
    command_label.pack(pady=10)
    command_entry = customtkinter.CTkEntry(master=edit_window, width=300)
    command_entry.pack(pady=5)
    command_entry.insert(0, command["name"])

    def edit_command_confirmed(event=None):
        if (2 <= len(url_entry.get()) <= 100) and (2 <= len(command_entry.get()) <= 100):
            command["name"] = command_entry.get()
            command["url"] = url_entry.get()
            save_custom_commands()
            refresh_commands_ui()
            edit_window.destroy()
        else:
            messagebox.showwarning("Invalid Input", "Both fields must be between 2 and 100 characters long!")

    enter_button = customtkinter.CTkButton(master=edit_window, text="Enter", command=edit_command_confirmed)
    enter_button.pack(pady=20)

    # Bind Enter key to edit command
    edit_window.bind("<Return>", edit_command_confirmed)


# Function to delete an existing command
def delete_command(command):
    global commands
    commands = [cmd for cmd in commands if cmd != command]
    print(f"Deleted Command: {command['name']}")
    save_custom_commands()
    refresh_commands_ui()


def reinitialize_app():
    global root, saved_theme, saved_mode

    root.destroy()

    # Save the current state
    current_theme = load_theme_preference()
    current_mode = load_mode_preference()

    # Create a new root window
    root = customtkinter.CTk()
    root.title("Aurora AI")
    root.iconbitmap("images/icon.ico")
    root.geometry("1024x768")  # Fixed geometry parameter

    # Apply the saved state
    customtkinter.set_appearance_mode(current_mode)
    customtkinter.set_default_color_theme(os.path.join(themes_folder, current_theme))

    # Reinitialize the GUI components
    initialize_ui(root)

    # Run the main loop again
    root.mainloop()


# Main function to run the application
def run_app():
    global root, saved_theme, saved_mode, theme_var, appearance_var

    # Load custom commands when the script starts
    load_custom_commands()

    # Load saved theme preference or select a random theme if none exists
    saved_theme = load_theme_preference()
    if not saved_theme and themes:
        saved_theme = random.choice(themes)  # Randomly select a theme
        save_theme_preference(saved_theme)  # Save the selected theme

    # Load saved appearance mode preference or set to "System" if none exists
    saved_mode = load_mode_preference()
    customtkinter.set_appearance_mode(saved_mode)

    customtkinter.set_default_color_theme(os.path.join(themes_folder, saved_theme))

    root = customtkinter.CTk()
    root.title("Aurora AI")
    root.iconbitmap("images/icon.ico")
    root.geometry("1024x768")

    # Initialize StringVars for the themes and appearance mode
    theme_var = tk.StringVar(value=saved_theme)
    appearance_var = tk.StringVar(value=saved_mode)

    # Initialize the UI components
    initialize_ui(root)

    # Run the tkinter main loop
    root.mainloop()

