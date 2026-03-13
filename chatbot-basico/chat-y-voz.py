import google.generativeai as genai
import asyncio
import edge_tts
import os

# --- CONFIGURACIÓN ---
GEMINI_API_KEY = "tu_api_key"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    system_instruction="Responde de forma concisa y humana. No uses asteriscos ni Markdown."
)

# Voz en español (puedes probar 'es-MX-JorgeNeural' o 'es-ES-AlvaroNeural')
VOICE = "es-MX-DaliaNeural" 
OUTPUT_FILE = "respuesta.mp3"

async def generar_audio(texto):
    communicate = edge_tts.Communicate(texto, VOICE)
    await communicate.save(OUTPUT_FILE)
    print(f"-> Audio generado: {OUTPUT_FILE}")
    # Opcional: reproducir en Windows
    os.system(f"start {OUTPUT_FILE}")

async def main():
    print("--- Chatbot Gratuito (Gemini + EdgeTTS) ---")
    print("Escribe 'salir' para terminar.\n")

    while True:
        user_input = input("Tú: ")
        
        if user_input.lower() in ["salir", "exit", "quit"]:
            print("¡Hasta luego!")
            break

        try:
            # 1. Obtener respuesta de Gemini
            response = model.generate_content(user_input)
            texto_respuesta = response.text.strip()
            print(f"Gemini: {texto_respuesta}")

            # 2. Generar audio (Asíncrono)
            await generar_audio(texto_respuesta)

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())