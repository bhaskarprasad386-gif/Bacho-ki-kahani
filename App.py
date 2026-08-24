import streamlit as st
from google import genai
from gtts import gTTS
from datetime import datetime
import io


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="Bal Kahani",
    page_icon="🌈",
    layout="wide"
)
# ============================================================
# GOOGLE ANALYTICS
# ============================================================

import streamlit.components.v1 as components

GA_ID = st.secrets.get(
    "GA_MEASUREMENT_ID",
    ""
)

if GA_ID:
    components.html(
        f"""
        <script async
        src="https://www.googletagmanager.com/gtag/js?id={GA_ID}">
        </script>

        <script>
        window.dataLayer = window.dataLayer || [];

        function gtag() {{
            dataLayer.push(arguments);
        }}

        gtag('js', new Date());
        gtag('config', '{GA_ID}');
        </script>
        """,
        height=0
    )

# ============================================================
# SESSION STATE
# ============================================================

if "story" not in st.session_state:
    st.session_state.story = ""

if "story_title" not in st.session_state:
    st.session_state.story_title = ""

if "saved_stories" not in st.session_state:
    st.session_state.saved_stories = []

if "audio" not in st.session_state:
    st.session_state.audio = None


# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        180deg,
        #b9ecff 0%,
        #eafff5 55%,
        #d9f5cf 100%
    );
}

.main-title {
    text-align: center;
    font-size: 52px;
    font-weight: 900;
    color: #ff5b6e;
    text-shadow: 3px 3px white;
}

.subtitle {
    text-align: center;
    font-size: 20px;
    font-weight: 700;
    color: #38566b;
}

.card {
    background: rgba(255,255,255,0.94);
    padding: 20px;
    border-radius: 25px;
    margin-bottom: 18px;
    box-shadow: 0 7px 20px rgba(0,0,0,0.08);
}

.story {
    background: #fffdf3;
    padding: 28px;
    border-radius: 25px;
    border: 3px solid #ffe19a;
    font-size: 18px;
    line-height: 1.9;
}

.good {
    background: #eaffea;
    padding: 20px;
    border-radius: 20px;
    border: 2px solid #9bdd9b;
}

.bad {
    background: #fff0f0;
    padding: 20px;
    border-radius: 20px;
    border: 2px solid #ffb0b0;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="card">

<div style="text-align:center;font-size:65px;">
☀️ ☁️ 🐰 🌳 🌸 🏠 🦋 🐘
</div>

<div class="main-title">
🌈 BAL KAHANI
</div>

<div class="subtitle">
बच्चों के लिए अपनी प्यारी कहानी बनाइए 📖
</div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# API KEY
# ============================================================

try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    API_KEY = ""


# ============================================================
# CHARACTERS
# ============================================================

st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown("## 👨‍👩‍👧‍👦 कहानी के पात्र")

st.caption("अधिकतम 5 पात्र जोड़ सकते हैं।")

characters = []

cols = st.columns(5)

for i in range(5):

    with cols[i]:

        st.markdown(
            f"### {'👦' if i % 2 == 0 else '👧'} {i + 1}"
        )

        name = st.text_input(
            "नाम",
            placeholder="नाम",
            key=f"name_{i}"
        )

        age = st.selectbox(
            "उम्र",
            [
                "2-3 साल",
                "4-5 साल",
                "6-7 साल",
                "8-10 साल",
                "11-13 साल", 
                "15-20 साल", 
                "25-30 साल", 
                "30-35 साल", 
                "40-50 साल", 
                "50-60 साल"
            ],
            key=f"age_{i}"
        )

        role = st.selectbox(
            "पात्र",
            [
                "बच्चा",
                "बच्ची",
                "माँ",
                "पिता",
                "दादा",
                "दादी",
                "दोस्त",
                "शिक्षक",
                "जानवर"
            ],
            key=f"role_{i}"
        )

        if name.strip():
            characters.append({
                "name": name.strip(),
                "age": age,
                "role": role
            })

st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# STORY SETTINGS
# ============================================================

st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown("## 📖 कहानी की जानकारी")

c1, c2, c3 = st.columns(3)

with c1:
    story_type = st.selectbox(
        "🎭 कहानी का प्रकार",
        [
            "जानवरों की कहानी",
            "जंगल की कहानी",
            "परिवार की कहानी",
            "जादुई कहानी",
            "स्कूल की कहानी",
            "गाँव की कहानी",
            "एडवेंचर कहानी",
            "मजेदार कहानी",
            "मोरल कहानी",
            "सोने की कहानी",
            "दोस्ती की कहानी",
            "प्रकृति की कहानी",
            "अंतरिक्ष की कहानी"
        ]
    )

with c2:
    story_length = st.selectbox(
        "⏱️ कहानी की लंबाई",
        [
            "2 मिनट",
            "5 मिनट",
            "10 मिनट",
            "15 मिनट",
            "20 मिनट"
        ]
    )

with c3:
    language = st.selectbox(
        "🌐 भाषा",
        [
         "सरल हिंदी",
        "हिंदी",
        "Hinglish",
        "English",
        "खोरठा (Khortha)",
        "বাংলা (Bangla)",
        "मराठी (Marathi)",
        "ગુજરાતી (Gujarati)",
        "ਪੰਜਾਬੀ (Punjabi)",
        "தமிழ் (Tamil)",
        "తెలుగు (Telugu)",
        "ಕನ್ನಡ (Kannada)",
        "മലയാളം (Malayalam)",
        "ଓଡ଼ିଆ (Odia)",
        "অসমীয়া (Assamese)",
        "नेपाली (Nepali)",
        "اردو (Urdu)"
            
            
       
        ]
    )

conditions = st.text_area(
    "🧠 कहानी में क्या-क्या होना चाहिए?",
    placeholder=(
        "उदाहरण: कहानी में राहुल, एक खरगोश, "
        "एक बड़ा पेड़, फूल और एक छोटा घर होना चाहिए। "
        "अंत में राहुल को अच्छी सीख मिलनी चाहिए।"
    ),
    height=120
)

st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# GOOD / BAD HABITS
# ============================================================

c1, c2 = st.columns(2)

with c1:

    st.markdown('<div class="good">', unsafe_allow_html=True)

    st.markdown("### ❤️ अच्छी आदतें")

    good_habits = st.multiselect(
        "कहानी में अच्छी आदत",
        [
            "सच बोलना",
            "बड़ों का सम्मान",
            "सफाई रखना",
            "दूसरों की मदद करना",
            "समय पर सोना",
            "समय पर उठना",
            "दाँत साफ करना",
            "स्वस्थ भोजन करना",
            "पानी बचाना",
            "पेड़ लगाना",
            "पढ़ाई करना",
            "खिलौने व्यवस्थित रखना",
            "जानवरों से प्यार करना",
            "दोस्तों के साथ मिलकर रहना"
        ]
    )

    st.markdown("</div>", unsafe_allow_html=True)


with c2:

    st.markdown('<div class="bad">', unsafe_allow_html=True)

    st.markdown("### 🚫 क्या नहीं करना चाहिए")

    bad_habits = st.multiselect(
        "गलत आदत",
        [
            "झूठ बोलना",
            "गुस्सा करना",
            "मारपीट करना",
            "किसी को परेशान करना",
            "खाना बर्बाद करना",
            "पानी बर्बाद करना",
            "कचरा फैलाना",
            "जानवरों को परेशान करना",
            "बिना बताए बाहर जाना",
            "बहुत देर मोबाइल चलाना"
        ]
    )

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# BEDTIME
# ============================================================

st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown("## 🌙 Bedtime Mode")

bedtime = st.toggle(
    "🌙 सोने वाली शांत कहानी"
)

if bedtime:

    music = st.selectbox(
        "🎵 Music mood",
        [
            "Soft Lullaby",
            "Rain",
            "Forest Night",
            "Ocean",
            "Soft Piano"
        ]
    )

else:

    music = "None"

st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# GENERATE STORY
# ============================================================

def generate_story():

    if not API_KEY:
        raise Exception(
            "GEMINI_API_KEY नहीं मिली। "
            "Streamlit Secrets में API key डालें।"
        )

    client = genai.Client(
        api_key=API_KEY
    )

    if characters:

        character_text = "\n".join(
            [
                f"{x['name']} - {x['age']} - {x['role']}"
                for x in characters
            ]
        )

    else:

        character_text = "कोई नाम नहीं दिया गया।"


    good_text = (
        ", ".join(good_habits)
        if good_habits
        else "कोई विशेष नहीं"
    )

    bad_text = (
        ", ".join(bad_habits)
        if bad_habits
        else "कोई विशेष नहीं"
    )


    prompt = f"""
आप Bal Kahani नाम के बच्चों के लिए सुरक्षित AI storyteller हैं।

भाषा: {language}

कहानी का प्रकार: {story_type}

कहानी की लंबाई: {story_length}

पात्र:
{character_text}

यूजर की conditions:
{conditions if conditions else "कोई विशेष condition नहीं"}

अच्छी आदतें:
{good_text}

क्या नहीं करना चाहिए:
{bad_text}

Bedtime:
{bedtime}

Music mood:
{music}

नियम:

1. कहानी बच्चों के लिए सुरक्षित हो।
2. भाषा उम्र के अनुसार सरल हो।
3. दिए गए नामों का स्वाभाविक इस्तेमाल करें।
4. कहानी में शुरुआत, समस्या, समाधान और सुंदर ending हो।
5. अच्छी आदत को कहानी के अंदर स्वाभाविक रूप से दिखाएं।
6. गलत आदत को सकारात्मक तरीके से समझाएं।
7. कहानी सुनने में मजेदार हो।
8. अनावश्यक डर या हिंसा न हो।
9. कहानी में जानवर, फूल, पेड़, घर आदि तभी डालें जब conditions में हों।
10. Bedtime mode में कहानी बहुत शांत और सुकून देने वाली हो।

नीचे EXACT format में जवाब दें:

TITLE:
छोटा और प्यारा title

STORY:
पूरी कहानी

LESSON:
कहानी से सीख

GOOD_HABITS:
अच्छी आदतें

AVOID:
क्या नहीं करना चाहिए

SCENES:
Scene 1:
Scene 2:
Scene 3:
Scene 4:
Scene 5:

IMAGE_PROMPT:
कहानी के लिए children's storybook illustration prompt
"""
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text


# ============================================================
# PARSE
# ============================================================

def parse_story(text):


    result = {
        "title": "मेरी प्यारी कहानी",
        "story": text,
        "lesson": "",
        "good": "",
        "avoid": "",
        "scenes": "",
        "image_prompt": ""
    }

    markers = [
        ("TITLE:", "title"),
        ("STORY:", "story"),
        ("LESSON:", "lesson"),
        ("GOOD_HABITS:", "good"),
        ("AVOID:", "avoid"),
        ("SCENES:", "scenes"),
        ("IMAGE_PROMPT:", "image_prompt")
    ]

    found = []

    for marker, key in markers:

        pos = text.find(marker)

        if pos != -1:
            found.append(
                (pos, marker, key)
            )

    found.sort()

    for i, (pos, marker, key) in enumerate(found):

        start = pos + len(marker)

        if i + 1 < len(found):
            end = found[i + 1][0]
        else:
            end = len(text)

        result[key] = text[start:end].strip()

    return result


# ============================================================
# CREATE BUTTON
# ============================================================

st.markdown("## ✨ कहानी बनाइए")

if st.button(
    "🌈 ✨ अभी कहानी बनाओ ✨ 🌈",
    type="primary",
    use_container_width=True
):

    with st.spinner(
        "🧚 AI आपकी कहानी बना रहा है..."
    ):

        try:

            raw = generate_story()

            data = parse_story(raw)

            st.session_state.story = data["story"]

            st.session_state.story_title = data["title"]

            st.session_state.story_data = data

            st.session_state.audio = None

            st.success(
                "🎉 कहानी तैयार है!"
            )

        except Exception as e:

            st.error(
                f"कहानी बनाने में समस्या: {e}"
            )


# ============================================================
# SHOW STORY
# ============================================================

if st.session_state.story:

    data = st.session_state.get(
        "story_data",
        {}
    )

    st.markdown("---")

    st.markdown(
        f"""
        <div class="card">
        <div style="
        text-align:center;
        font-size:50px;
        ">
        📖 🐰 🌳 🌸 🦋
        </div>

        <h1 style="
        text-align:center;
        color:#ff6475;
        ">
        {st.session_state.story_title}
        </h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="story">',
        unsafe_allow_html=True
    )

    st.markdown(
        st.session_state.story
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


    # ========================================================
    # LESSON
    # ========================================================

    c1, c2 = st.columns(2)

    with c1:

        st.markdown("### ❤️ कहानी से सीख")

        st.info(
            data.get(
                "lesson",
                "अच्छी आदतें अपनानी चाहिए।"
            )
        )

    with c2:

        st.markdown("### 🌟 अच्छी आदतें")

        st.success(
            data.get(
                "good",
                "दूसरों की मदद करनी चाहिए।"
            )
        )


    st.markdown("### 🚫 क्या नहीं करना चाहिए")

    st.warning(
        data.get(
            "avoid",
            "गलत आदतों से बचना चाहिए।"
        )
    )


    # ========================================================
    # SCENES
    # ========================================================

    with st.expander(
        "🖼️ कहानी के Visual Scenes देखें"
    ):

        st.write(
            data.get(
                "scenes",
                "Scenes उपलब्ध नहीं हैं।"
            )
        )

        st.markdown(
            "### 🎨 Image Prompt"
        )

        st.code(
            data.get(
                "image_prompt",
                ""
            )
        )


    # ========================================================
    # TTS
    # ========================================================

    st.markdown("## 🔊 कहानी सुनें")

    voice_language = st.selectbox(
        "🎙️ Voice",
        [
            ("हिंदी", "hi"),
            ("English", "en"),
            ("বাংলা", "bn"),
            ("मराठी", "mr"),
            ("ગુજરાતી", "gu")
        ],
        format_func=lambda x: x[0]
    )


    if st.button(
        "🔊 Text to Speech चलाएँ",
        use_container_width=True
    ):

        with st.spinner(
            "🎙️ आवाज तैयार हो रही है..."
        ):

            try:

                audio_buffer = io.BytesIO()

                tts = gTTS(
                    text=st.session_state.story,
                    lang=voice_language[1],
                    slow=bedtime
                )

                tts.write_to_fp(
                    audio_buffer
                )

                st.session_state.audio = (
                    audio_buffer.getvalue()
                )

            except Exception as e:

                st.error(
                    f"TTS में समस्या: {e}"
                )


    if st.session_state.audio:

        st.audio(
            st.session_state.audio,
            format="audio/mp3"
        )

        st.download_button(
            "⬇️ Audio Save करें",
            data=st.session_state.audio,
            file_name="bal_kahani.mp3",
            mime="audio/mpeg",
            use_container_width=True
        )


    # ========================================================
    # SAVE STORY
    # ========================================================

    st.markdown("## 💾 Saved Story")

    if st.button(
        "❤️ कहानी Save करें",
        use_container_width=True
    ):

        st.session_state.saved_stories.append(
            {
                "title": st.session_state.story_title,
                "story": st.session_state.story,
                "date": datetime.now().strftime(
                    "%d-%m-%Y %H:%M"
                )
            }
        )

        st.success(
            "❤️ कहानी Save हो गई!"
        )


# ============================================================
# SAVED STORIES
# ============================================================

st.markdown("---")

st.markdown("## 📚 मेरी Saved Stories")

if st.session_state.saved_stories:

    for i, item in enumerate(
        reversed(st.session_state.saved_stories)
    ):

        with st.expander(
            f"📖 {item['title']} — {item['date']}"
        ):

            st.write(
                item["story"]
            )

else:

    st.info(
        "अभी कोई saved story नहीं है।"
    )
# ============================================================
# WHATSAPP SHARE
# ============================================================

import urllib.parse

app_url = st.context.url

share_message = f"""
🌈 Bal Kahani 🌈

बच्चों के लिए AI से प्यारी-प्यारी कहानियाँ बनाइए 📖🎙️

👦👧 5 Characters
🎙️ अलग-अलग Character Voices
🌙 Bedtime Stories
❤️ Moral Stories

👉 पूरी App यहाँ खोलें:
{app_url}
"""

whatsapp_link = (
    "https://wa.me/?text="
    + urllib.parse.quote(share_message)
)

st.markdown(
    f"""
    <a href="{whatsapp_link}"
       target="_blank"
       style="
       display:block;
       text-align:center;
       background:#25D366;
       color:white;
       padding:16px;
       border-radius:18px;
       font-size:21px;
       font-weight:bold;
       text-decoration:none;
       margin:15px 0;
       ">
       📲 WhatsApp पर पूरी App Share करें
    </a>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div style="
text-align:center;
padding:30px;
font-weight:700;
color:#587080;
">

🌈 Bal Kahani 🌈

<br>

🐰 🌳 🌸 🏠 🦋 🐘

<br>

बच्चों के लिए प्यार से बनाई गई कहानियाँ ❤️

</div>
""", unsafe_allow_html=True)


