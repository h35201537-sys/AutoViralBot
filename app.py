import streamlit as st
import requests
import os
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip

st.set_page_config(page_title="AutoViralBot", page_icon="🤖", layout="centered")

st.title("🤖 AutoViralBot: AI Video Creator")
st.write("Script qofa galchi; viidiyoo HD, sagalee qulqulluu fi Editing guutuu TikTok/YouTube qopheessa!")

st.sidebar.header("🔑 Fungoo Meeshaalee (API Keys)")
pexels_key = st.sidebar.text_input("Pexels API Key (Viidiyoo/Fakkii HD):", type="password")

script_text = st.text_area("✍️ Script kee ykn yaada viidiyoo kee asitti barreessi:", height=150, placeholder="Fakkeenya: Waa'ee milkaa'ina jireenyaa gabaabaatti barreessi...")
video_format = st.selectbox("📱 Format Viidiyoo:", ["TikTok / Shorts (9:16)", "YouTube (16:9)"])

if st.button("🚀 Viidiyoo Hawwataa Uumi"):
    if not pexels_key or not script_text:
        st.error("Maaloo, sidebar irratti Pexels API Key galchi, akkasumas script kee barreessi!")
    else:
        with st.spinner("AutoViralBot hojii jalqabeera..."):
            try:
                st.write("🎙️ Sagalee AI qulqullina qabu oomishaa jira...")
                tts = gTTS(text=script_text, lang='en', tld='com', slow=False)
                audio_path = "voice.mp3"
                tts.save(audio_path)
                
                audio_clip = AudioFileClip(audio_path)
                duration = audio_clip.duration
                
                st.write("🖼️ Viidiyoo HD/4K script kee waliin deemu barbaadaa jira...")
                headers = {"Authorization": pexels_key}
                search_word = script_text.split() if len(script_text.split()) > 0 else "motivation"
                
                orientation = "portrait" if "TikTok" in video_format else "landscape"
                url = f"https://pexels.com{search_word}&per_page=1&orientation={orientation}"
                
                response = requests.get(url, headers=headers).json()
                
                if "photos" in response and len(response["photos"]) > 0:
                    image_url = response["photos"]["src"]["large2x"]
                    img_data = requests.get(image_url).content
                    image_path = "background.jpg"
                    with open(image_path, "wb") as handler:
                        handler.write(img_data)
                else:
                    st.error("Fakkii argachuu hin dandeenye. Maaloo API Key kee qori.")
                    st.stop()

                st.write("🎬 Editing fi Wal-simsiisa hojjechaa jira...")
                video_clip = ImageClip(image_path).set_duration(duration)
                video_clip = video_clip.set_audio(audio_clip)
                
                output_path = "autoviral_output.mp4"
                video_clip.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
                
                audio_clip.close()
                video_clip.close()
                
                st.success("🎉 Viidiyoon kee bifa hawwataa ta'een xumurameera!")
                with open(output_path, "rb") as file:
                    st.download_button(label="📥 Viidiyoo Download Godhadhu", data=file, file_name="autoviral_video.mp4", mime="video/mp4")
                    
            except Exception as e:
                st.error(f"Dogoggorri uumameera: {e}")
