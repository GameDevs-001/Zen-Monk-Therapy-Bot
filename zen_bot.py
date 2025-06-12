import gradio as gr
import google.generativeai as genai
from gtts import gTTS
import tempfile
import os

# ✅ 1. Configure your Gemini API key
genai.configure(api_key="AIzaSyAn6wK59ki5c6UNyFTni6WkacvU2M6pZ-I")

# ✅ 2. Dynamically choose a supported text model
models = [m.name for m in genai.list_models()]
text_model = next((name for name in models if "gemini-1.5-flash" in name), None)
if text_model is None:
    raise Exception("No gemini-1.5-flash model found. Check API key and account access.")
print("🔎 Using model:", text_model)

model = genai.GenerativeModel(text_model)

# ✅ 3. Define response + text-to-speech function
def get_zen_response(user_input):
    try:
        response = model.generate_content(
            f"You're a calm Zen monk offering peaceful advice. User says: {user_input}"
        )
        text = response.text.strip()

        tts = gTTS(text=text, lang='en', slow=True)
        audio_path = os.path.join(tempfile.gettempdir(), "zen_bot.mp3")
        tts.save(audio_path)

        return text, audio_path

    except Exception as e:
        return f"⚠️ {str(e)}", None

# ✅ 4. Gradio interface with optional background music
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    if os.path.exists("zen_response.mp3"):
        gr.HTML("<audio src='zen_response.mp3' autoplay loop></audio>")
    gr.Markdown("## 🧘 Zensho: Your Zen Monk Bot\nShare your thoughts, find calm.")

    inp = gr.Textbox(lines=2, placeholder="Speak softly...", label="You")
    btn = gr.Button("Seek Peace")

    out_text = gr.Textbox(label="Zensho's Wisdom")
    out_audio = gr.Audio(label="Zen Voice", autoplay=True)

    btn.click(get_zen_response, inputs=inp, outputs=[out_text, out_audio])

demo.launch(share=True)




