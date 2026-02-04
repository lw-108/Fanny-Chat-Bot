import os
import sys
import random
import tkinter as tk
from tkinter import scrolledtext
from nltk.chat.util import Chat, reflections
from PIL import Image, ImageTk
import winsound   # ✅ Built-in WAV sound player


# ✅ Paths
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(__file__)
SOUND_FILE = os.path.join(BASE_DIR, "faaah.wav")
MEME_FOLDER = os.path.join(BASE_DIR, "memes")


# ✅ Meme Popup with Animated GIF + WAV Sound
def show_random_meme():

    gifs = [f for f in os.listdir(MEME_FOLDER) if f.endswith(".gif")]

    if not gifs:
        print("⚠ No GIFs found inside memes folder!")
        return

    gif_file = random.choice(gifs)
    gif_path = os.path.join(MEME_FOLDER, gif_file)

    # ✅ Play WAV Sound
    if os.path.exists(SOUND_FILE):
        winsound.PlaySound(SOUND_FILE, winsound.SND_ASYNC)

    # ✅ Popup Window
    popup = tk.Toplevel()
    popup.title("🤣 Meme Reaction")
    popup.geometry("420x450")

    gif = Image.open(gif_path)

    frames = []
    try:
        while True:
            frame = gif.copy()
            frame = frame.resize((380, 350))
            frames.append(ImageTk.PhotoImage(frame))
            gif.seek(len(frames))
    except EOFError:
        pass

    label = tk.Label(popup)
    label.pack(pady=10)

    # ✅ Animate GIF
    def animate(index=0):
        label.config(image=frames[index])
        popup.after(100, animate, (index + 1) % len(frames))

    animate()

    tk.Button(
        popup,
        text="Close 😂",
        font=("Arial", 12),
        command=popup.destroy
    ).pack(pady=5)


# ✅ Chatbot Patterns
pairs = [
    [r"(.*)my name is (.*)", ["Hello %2! How are you today? 😊"]],
    [r"(hi|hey|hello)", ["Hello! 👋", "Hey there! 😄"]],
    [r"(.*)your name ?", ["My name is Lingeshwarma Bot 🤖"]],
    [r"(.*)help(.*)", ["Sure! Ask me anything 😊"]],
    [r"who is (Cricketer|Batsman)?", ["Mahendra Singh Dhoni 🏏🔥"]],
    [r"(.*)(sports|game|sport)(.*)", ["I love Cricket 🏏"]],
    [r"(.*)location(.*)", ["My location is Chithode Thaiyirpalayam 🌍"]],
    [r"quit", ["Bye bye 👋"]],
    [r"(.*)", ["Yeah Yeah 😊"]]  # fallback trigger
]

chatbot = Chat(pairs, reflections)


# ✅ Desktop Chatbot App
class ChatbotApp:

    def __init__(self, root):
        self.root = root
        root.title("Lingeshwarma Bot 🤖")
        root.geometry("500x600")

        # Chat Box
        self.chat_area = scrolledtext.ScrolledText(
            root,
            wrap=tk.WORD,
            font=("Arial", 12)
        )
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.chat_area.insert(tk.END, "🤖 Lingeshwarma Bot: Hello! Type something...\n\n")
        self.chat_area.config(state=tk.DISABLED)

        # Input Box
        self.entry = tk.Entry(root, font=("Arial", 14))
        self.entry.pack(padx=10, pady=10, fill=tk.X)
        self.entry.bind("<Return>", self.send_message)

        # Send Button
        self.send_btn = tk.Button(
            root,
            text="Send 🚀",
            font=("Arial", 12),
            command=self.send_message
        )
        self.send_btn.pack(pady=5)

    def send_message(self, event=None):

        user_text = self.entry.get().strip()
        if not user_text:
            return

        self.entry.delete(0, tk.END)

        # Show user text
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, f"🧑 You: {user_text}\n")

        # Bot reply
        response = chatbot.respond(user_text.lower())
        self.chat_area.insert(tk.END, f"🤖 Bot: {response}\n\n")

        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.yview(tk.END)

        # ✅ Unknown Word → Meme Popup + Sound
        if response == "Yeah Yeah 😊":
            show_random_meme()


# ✅ Run App
if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotApp(root)
    root.mainloop()
