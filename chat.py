import tkinter as tk
import threading
import sounddevice as sd
import scipy.io.wavfile as wav
import whisper
import cohere
from gtts import gTTS
import io
import pygame
model = whisper.load_model("base")
# Add your Cohere API key below before running
co = cohere.Client("")



def record_audio(filename, duration=5, fs=44100):
    chat_box.insert(tk.END, "🎙 جاري الاستماع...\n")
    chat_box.see(tk.END)
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    wav.write(filename, fs, recording)
    chat_box.insert(tk.END, "✅ تم التسجيل\n")
    chat_box.see(tk.END)

def speak(text):
    tts = gTTS(text=text, lang="ar")
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    pygame.mixer.init()
    pygame.mixer.music.load(fp)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue


def handle_voice():
    filename = "input.wav"
    record_audio(filename)
    result = model.transcribe(filename, language="ar")
    user_input = result["text"].strip()

    chat_box.insert(tk.END, f"👤 أنت: {user_input}\n")
    chat_box.see(tk.END)

    
    response = co.generate(
        model='command',
        prompt=user_input,
        max_tokens=50
    )
    reply = response.generations[0].text.strip()

    reply = reply.split("In Arabic:")[-1].split("English:")[0].strip()
    if "\n" in reply:
        reply = reply.split("\n")[0].strip()

    chat_box.insert(tk.END, f"🤖 المساعد: {reply}\n")
    chat_box.see(tk.END)
    speak(reply)


root = tk.Tk()
root.title("🤖مساعدك الصوتي الذكي")
root.geometry("520x520")
root.configure(bg="#fefefe")

title = tk.Label(root, text="🤖 مساعدك الصوتي الذكي", font=("Arial", 18), bg="#fefefe", fg="#3b3b3b")
title.pack(pady=10)

chat_box = tk.Text(root, font=("Arial", 12), height=20, width=60, bg="white")
chat_box.pack(padx=10)

record_btn = tk.Button(root, text="🎙 تسجيل صوت", font=("Arial", 12), bg="#8ab6d6", fg="white", command=lambda: threading.Thread(target=handle_voice).start())
record_btn.pack(pady=15)

root.mainloop()
