import tkinter as tk
from tkinter import scrolledtext
import os
from google import genai
from google.genai import types
#import google.generativeai as genai
from dotenv import load_dotenv

#Cargar API key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
#Cargando configuraciones
config_corta = types.GenerateContentConfig(
    max_output_tokens=4000, 
    temperature=0.5,
    system_instruction="Responde de forma breve, en menos de 300 caracteres."
)
# Configuracion de Gemini 3
client = genai.Client(api_key=GOOGLE_API_KEY)
#chat_session = client.chats.create(model="gemini-2.5-flash") #No limita las respuestas de gemini, consume mas tokens
chat_session = client.chats.create(
    model="gemini-2.5-flash",
    config=config_corta
)


#Función de enviar mensajes y obtener respuestas
def send_message():
    user_input = entry.get().strip()
    if not user_input:
        return
    if user_input.lower() in ["salir","exit"]:
        root.destroy()
        return
    #Mostrar mensaje del usuario en la interfaz
    chat_window.insert(tk.END, f"Tú: {user_input}\n", "user")
    entry.delete(0, tk.END)

    try:
        response = chat_session.send_message(user_input)
        chat_window.insert(tk.END, f"Gemini: {response.text}\n\n", "bot")
        chat_window.yview(tk.END)
    except Exception as e: #Captura la excepcion
        chat_window.insert(tk.END, f"Error: {e}\n", "error")

# Construye la UI
root = tk.Tk()
root.title("Chat Basico")
root.geometry("600x600")

chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Courier", 12))
chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chat_window.tag_config("user", foreground="blue")
chat_window.tag_config("bot", foreground="green")
chat_window.tag_config("error", foreground="red")
chat_window.insert(tk.END, "Gemini AI Chat (escribe 'salir' para finalizar)\n\n", "bot")

entry = tk.Entry(root, font=("Courier", 12))
entry.pack(padx=10, pady=5, fill=tk.X)
entry.bind("<Return>", lambda event: send_message())

send_btn = tk.Button(root, text="Enviar", command=send_message)
send_btn.pack(pady=5)

exit_btn = tk.Button(root, text="Salir", command=root.destroy)
exit_btn.pack(pady=5)
root.mainloop()