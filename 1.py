import streamlit as st
from googletrans import Translator
import requests
import os
import time
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

# Configure app
st.set_page_config(
    page_title="Global Translator",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f0f2f6;
    }
    .stTextArea textarea {
        border-radius: 15px !important;
    }
    .stButton>button {
        border-radius: 10px;
        background: linear-gradient(90deg, #6e48aa 0%, #9d50bb 100%);
        color: white;
    }
    .stSelectbox div[data-baseweb="select"] {
        border-radius: 10px;
    }
    .language-tag {
        font-size: 0.8em;
        padding: 2px 6px;
        border-radius: 4px;
        margin-right: 5px;
    }
    .source-lang {
        background-color: #ffaaaa;
    }
    .target-lang {
        background-color: #aaffaa;
    }
</style>
""", unsafe_allow_html=True)

# Initialize translator
@st.cache_resource
def init_translator():
    return Translator()

translator = init_translator()

# Enhanced language support
languages = {
    'Auto Detect': {'code': 'auto', 'note': 'Let our AI detect the language'},
    'English': {'code': 'en', 'note': 'Most widely spoken language globally'},
    'Spanish': {'code': 'es', 'note': 'Second most spoken native language'},
    'French': {'code': 'fr', 'note': 'Language of diplomacy'},
    'German': {'code': 'de', 'note': 'Most spoken native language in EU'},
    'Japanese': {'code': 'ja', 'note': 'Uses three writing systems'},
    'Arabic': {'code': 'ar', 'note': 'Read right-to-left'},
    'Hindi': {'code': 'hi', 'note': 'Official language of India'},
    'Russian': {'code': 'ru', 'note': 'Uses Cyrillic alphabet'},
    'Portuguese': {'code': 'pt', 'note': 'Fastest-growing European language'}
}

# Custom function to replace annotated-text
def display_translation(source_text, src_code, translated_text, dest_code):
    st.markdown(f"""
    <div style="margin-bottom: 20px;">
        <div>
            <span class="language-tag source-lang">{src_code}</span>
            <strong>Original:</strong> {source_text}
        </div>
        <div style="margin-top: 10px;">
            <span class="language-tag target-lang">{dest_code}</span>
            <strong>Translated:</strong> {translated_text}
        </div>
    </div>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("Global Translator")
    st.markdown("""
    ### 🌍 Cross-Language Communication
    *Breaking barriers with AI translation*
    """)
    
    st.markdown("---")
    st.markdown("### 💡 Did You Know?")
    st.info("""
    There are approximately 7,000 languages spoken worldwide today,
    but about 40% of them are endangered.
    """)

    if 'translation_count' not in st.session_state:
        st.session_state.translation_count = 0
    st.markdown(f"📊 Translations this session: **{st.session_state.translation_count}**")

# Main app
st.title("🌐 Global Translator")
st.markdown("*Real-time translation with cultural context*")

tab1, tab2 = st.tabs(["🧭 Translator", "🌍 Cultural Guide"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Input Text")
        source_text = st.text_area(
            "Enter text to translate",
            height=200,
            placeholder="Type or paste your text here...",
            key="source_text"
        )
        
        source_lang = st.selectbox(
            "Source Language",
            list(languages.keys()),
            index=0,
            help=languages[list(languages.keys())[0]]['note']
        )

    with col2:
        st.subheader("Translated Text")
        target_lang = st.selectbox(
            "Target Language",
            [lang for lang in languages.keys() if lang != "Auto Detect"],
            index=1,
            help=languages[list(languages.keys())[1]]['note']
        )
        
        if st.button("✨ Translate", type="primary"):
            if source_text.strip():
                with st.spinner("🔍 Translating..."):
                    start_time = time.time()
                    
                    try:
                        if source_lang == "Auto Detect":
                            detected_lang = detect(source_text)
                            src_code = detected_lang
                            lang_name = [k for k, v in languages.items() if v['code'] == detected_lang][0]
                            st.toast(f"🔍 Detected: {lang_name}")
                        else:
                            src_code = languages[source_lang]['code']
                        
                        dest_code = languages[target_lang]['code']
                        
                        result = translator.translate(
                            source_text,
                            src=src_code,
                            dest=dest_code
                        )
                        
                        # Display translation with custom formatting
                        display_translation(source_text, src_code, result.text, dest_code)
                        
                        st.session_state.translation_count += 1
                        
                        end_time = time.time()
                        st.success(f"✅ Translation completed in {end_time - start_time:.2f} seconds")
                        
                        st.markdown("---")
                        st.markdown(f"**🌍 Cultural Insight for {target_lang}:**")
                        st.info(languages[target_lang]['note'])
                        
                    except Exception as e:
                        st.error(f"⚠️ Translation error: {str(e)}")
                        st.markdown("---")
                        st.markdown("**🛠️ Trying alternative method...**")
                        
                        try:
                            url = "https://libretranslate.de/translate"
                            params = {
                                "q": source_text,
                                "source": src_code,
                                "target": dest_code,
                                "format": "text"
                            }
                            response = requests.post(url, json=params)
                            translation = response.json()["translatedText"]
                            
                            # Display fallback translation
                            display_translation(source_text, src_code, translation, dest_code)
                            st.session_state.translation_count += 1
                        except:
                            st.error("❌ All translation services failed")
            else:
                st.warning("Please enter some text to translate")

with tab2:
    st.subheader("🌍 Cultural Communication Guide")
    
    selected_lang = st.selectbox(
        "Select a language to learn about:",
        [lang for lang in languages.keys() if lang != "Auto Detect"],
        key="culture_select"
    )
    
    st.markdown(f"## {selected_lang} Cultural Notes")
    
    cultural_notes = {
        'English': [
            "**Gestures**: 👍 Thumbs up means approval",
            "**Communication**: Direct communication is valued",
            "**Taboos**: Avoid overly personal questions"
        ],
        'Japanese': [
            "**Gestures**: 👐 Bowing shows respect (deeper bows show more respect)",
            "**Business**: Always present business cards with both hands",
            "**Dining**: Never stick chopsticks upright in rice (resembles funeral rites)"
        ],
        'Arabic': [
            "**Gestures**: Use your right hand for eating and greeting",
            "**Communication**: Building personal relationships is essential in business",
            "**Religion**: Avoid scheduling meetings during prayer times"
        ]
    }
    
    if selected_lang in cultural_notes:
        for note in cultural_notes[selected_lang]:
            st.markdown(note)
            st.write("")  # Add spacing
    else:
        st.info("Cultural guide coming soon for this language!")
        st.markdown(f"""
        **General tips for {selected_lang}:**
        - Always greet people properly
        - Research appropriate body language
        - When in doubt, ask politely about local customs
        """)
    
    st.markdown("---")
    st.markdown("""
    **📚 Communication Tips:**
    - Learn basic greetings in the local language
    - Observe how locals interact with each other
    - Be patient with communication differences
    - Smiling is universally appreciated
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center;">
    <p>Made with ❤️ for global communicators</p>
</div>
""", unsafe_allow_html=True)