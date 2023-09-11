
'''
  ____  _   _            _    
  / __ \| |_| |_ __ _ ___| | __
 / / _` | __| __/ _` / __| |/ /
| | (_| | |_| || (_| \__ \   < 
 \ \__,_|\__|\__\__,_|___/_|\_\
  \____/                       
'''
import tkinter as tk
import requests
import asyncio
import configparser
import threading

# Global variables
paused = False
message_count = 0

# Function to send the message
async def send_message():
    global message_count
    while True:
        if not paused:
            payload = {
                "content": message_entry.get()
            }
            channel_id = channel_id_entry.get()
            channel = f'https://discord.com/api/v9/channels/{channel_id}/messages'
            header = {
                'authorization': auth_entry.get()
            }
            req = requests.post(channel, data=payload, headers=header)
            await asyncio.sleep(float(delay_entry.get()))
            message_count += 1
            log_text.config(text=f"Messages Sent: {message_count}")

            # Save the current settings to the configuration file
            save_settings()

# Function to toggle pause state
def toggle_pause():
    global paused
    paused = not paused

# Function to save the current settings to the configuration file
def save_settings():
    config = configparser.ConfigParser()
    config['Settings'] = {
        'Authorization': auth_entry.get(),
        'Delay': delay_entry.get(),
        'ChannelID': channel_id_entry.get(),
        'Message': message_entry.get()
    }
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

# Function to load saved settings from the configuration file
def load_settings():
    config = configparser.ConfigParser()
    config.read('config.ini')
    if 'Settings' in config:
        auth_entry.insert(0, config['Settings']['Authorization'])
        delay_entry.insert(0, config['Settings']['Delay'])
        channel_id_entry.insert(0, config['Settings']['ChannelID'])
        message_entry.insert(0, config['Settings']['Message'])

# Function to start the background event loop
def start_event_loop():
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_message())

# Create the main GUI window
root = tk.Tk()
root.title("@ttask on discord")
root.geometry("400x400")  # Increase the size of the GUI window

auth_label = tk.Label(root, text="Authorization:")
auth_label.pack()
auth_entry = tk.Entry(root)
auth_entry.pack()

delay_label = tk.Label(root, text="Delay (in seconds):")
delay_label.pack()
delay_entry = tk.Entry(root)
delay_entry.pack()

channel_id_label = tk.Label(root, text="Channel ID:")
channel_id_label.pack()
channel_id_entry = tk.Entry(root)
channel_id_entry.pack()

message_label = tk.Label(root, text="Message:")
message_label.pack()
message_entry = tk.Entry(root)
message_entry.pack()

start_button = tk.Button(root, text="Start Sending", command=lambda: threading.Thread(target=start_event_loop).start())
start_button.pack()

pause_button = tk.Button(root, text="Pause/Resume", command=toggle_pause)
pause_button.pack()

log_text = tk.Label(root, text="Messages Sent: 0")
log_text.pack()

# Load saved settings on startup
load_settings()

# Start the GUI main loop
root.mainloop()