import requests
import streamlit as st

st.set_page_config(page_title="Quran Premium UI", page_icon="🕌", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Poppins:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: #f1f1f1; }
::-webkit-scrollbar-thumb { background: #11998e; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: #38ef7d; }
.stApp { background: linear-gradient(135deg, #f8f9fa 0%, #eef2f3 100%); }
.app-header { text-align: center; padding: 20px 0 10px 0; animation: fadeInDown 1s ease-out; }
.app-header h1 { background: linear-gradient(to right, #11998e, #38ef7d); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3.5rem; font-weight: 700; margin: 0; }
.app-header p { color: #6c757d; font-size: 1.1rem; letter-spacing: 1px; margin-top: 5px; }
.sidebar-profile { text-align: center; padding: 15px 0; margin-bottom: 20px; border-bottom: 1px solid rgba(0,0,0,0.1); }
.sidebar-profile img { width: 90px; filter: drop-shadow(0px 8px 15px rgba(17, 153, 142, 0.4)); margin-bottom: 15px; animation: pulse 2s infinite; }
.sidebar-profile h3 { background: linear-gradient(135deg, #11998e, #38ef7d); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 700; margin: 0; font-size: 1.5rem; }
.sidebar-profile p { color: #888; font-size: 0.85rem; margin-top: 5px; }
.surah-header-card { background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); border-radius: 20px; padding: 30px; text-align: center; color: white; margin-bottom: 40px; box-shadow: 0 15px 35px rgba(15, 32, 39, 0.3); animation: zoomIn 1s ease-out; position: relative; overflow: hidden; }
.surah-header-card h2 { font-family: 'Amiri', serif; font-size: 3.5rem; color: #f1c40f; margin: 0; text-shadow: 0 4px 10px rgba(0,0,0,0.5); }
.surah-header-card h3 { font-size: 1.8rem; font-weight: 600; margin: 5px 0 15px 0; }
.surah-info-badges { display: flex; justify-content: center; gap: 15px; margin-top: 15px; }
.s-badge { background: rgba(255,255,255,0.15); backdrop-filter: blur(5px); padding: 8px 20px; border-radius: 30px; font-size: 0.9rem; border: 1px solid rgba(255,255,255,0.2); }
.ayah-container { background: rgba(255, 255, 255, 0.9); border: 1px solid rgba(17, 153, 142, 0.15); border-radius: 20px; padding: 35px; margin-bottom: 25px; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.03); transition: all 0.3s ease; animation: slideUpFade 0.6s ease-out forwards; }
.ayah-container:hover { transform: translateY(-5px); box-shadow: 0 15px 35px rgba(17, 153, 142, 0.15); border-color: #38ef7d; }
.ayah-badge { background: linear-gradient(135deg, #11998e, #38ef7d); color: white; padding: 6px 18px; border-radius: 20px; font-weight: 600; font-size: 0.9rem; display: inline-block; margin-bottom: 20px; box-shadow: 0 4px 10px rgba(17,153,142,0.3); }
.arabic-text { font-family: 'Amiri', serif; font-size: 2.8rem; color: #1a1a2e; text-align: right; direction: rtl; line-height: 2.2; margin-bottom: 20px; }
.translation-text { font-size: 1.2rem; color: #4a4e69; line-height: 1.8; border-top: 1px solid rgba(0,0,0,0.05); padding-top: 20px; margin-top: 10px; }
@keyframes fadeInDown { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); } }
@keyframes zoomIn { from { opacity: 0; transform: scale(0.95); } to { opacity: 1; transform: scale(1); } }
@keyframes slideUpFade { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
@keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.05); } 100% { transform: scale(1); } }
</style>
""", unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def fetch_surah_list():
    return {s['number']: s for s in requests.get("https://api.alquran.cloud/v1/surah").json()['data']}

@st.cache_data(show_spinner=False)
def fetch_quran_data(surah, text_lang, audio_lang):
    return (requests.get(f"https://api.alquran.cloud/v1/surah/{surah}/quran-uthmani").json()["data"],
            requests.get(f"https://api.alquran.cloud/v1/surah/{surah}/{text_lang}").json()["data"],
            requests.get(f"https://api.alquran.cloud/v1/surah/{surah}/{audio_lang}").json()["data"])

surahs_dict = fetch_surah_list()

with st.sidebar:
    st.markdown("""
    <div class="sidebar-profile">
        <img src="https://cdn-icons-png.flaticon.com/512/3389/3389081.png">
        <h3>Al-Quran</h3>
        <p>Premium Digital Explorer</p>
    </div>
    <h4 style='color: #11998e; margin-bottom: 10px;'>⚙️ Navigation</h4>
    """, unsafe_allow_html=True)
    
    surah_num = int(st.selectbox("📖 Select Surah", [f"{n} - {d['englishName']}" for n, d in surahs_dict.items()]).split(" - ")[0])
    selected_surah_data = surahs_dict[surah_num]

    st.markdown("<br>", unsafe_allow_html=True)

    languages = {
        "English": {"text": "en.asad", "audio": "en.walk"},
        "Urdu": {"text": "ur.jalandhry", "audio": "ur.khan"},
        "French": {"text": "fr.hamidullah", "audio": "fr.leclerc"},
        "Arabic Only": {"text": "ar", "audio": "ar.alafasy"},
        "Persian": {"text": "fa.ayati", "audio": "ar.alafasy"},
        "Russian": {"text": "ru.kuliev", "audio": "ru.kuliev-audio"},
        "Chinese": {"text": "zh.jian", "audio": "ar.alafasy"}
    }
    
    selected_language = st.selectbox("🌐 Translation", list(languages.keys()))
    text_code, audio_code = languages[selected_language]["text"], languages[selected_language]["audio"]

    st.markdown(f"""
    <div style="background: rgba(17,153,142,0.1); padding: 10px; border-radius: 10px; text-align:center; margin-top: 20px;">
        <span style='color: #11998e; font-size: 0.85rem; font-weight: 600;'>Audio Engine Active</span><br>
        <span style='color: gray; font-size: 0.75rem;'>{audio_code}</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="app-header">
    <h1>Al-Quran Explorer</h1>
    <p>Journey Through the Divine Words</p>
</div>
""", unsafe_allow_html=True)

with st.spinner("Connecting to servers..."):
    try:
        ar_data, trans_data, audio_data = fetch_quran_data(surah_num, text_code, audio_code)
        
        bismillah_html = '<div style="margin-top: 30px;"><h2 style="font-size: 3rem; color: #11998e; text-shadow: none;">بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيم</h2></div>' if surah_num != 9 else ''
        
        st.markdown(f"""
        <div class="surah-header-card">
            <h2>{selected_surah_data['name']}</h2>
            <h3>{selected_surah_data['englishName']}</h3>
            <p style="font-size: 1.1rem; color: #ddd; margin: 0;">"{selected_surah_data['englishNameTranslation']}"</p>
            <div class="surah-info-badges">
                <span class="s-badge">📍 {selected_surah_data['revelationType']}</span>
                <span class="s-badge">🔢 {selected_surah_data['numberOfAyahs']} Ayahs</span>
            </div>
            {bismillah_html}
        </div>
        """, unsafe_allow_html=True)
            
        for ar, tr, au in zip(ar_data["ayahs"], trans_data["ayahs"], audio_data["ayahs"]):
            trans_html = f'<div class="translation-text">{tr["text"]}</div>' if selected_language != "Arabic Only" else ""
            
            st.markdown(f"""
            <div class="ayah-container">
                <span class="ayah-badge">Ayah {ar['numberInSurah']}</span>
                <div class="arabic-text">{ar['text']}</div>
                {trans_html}
            </div>
            """, unsafe_allow_html=True)
            
            if "audio" in au:
                st.audio(au["audio"])
                
    except Exception:
        st.error("Network error! Please check your internet connection.")
