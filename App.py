
हाँ। अब वास्तव में अलग-अलग आवाज़ चाहिए तो gTTS से नहीं होगा। gTTS में अलग character voices का control बहुत सीमित है।

हम Edge TTS लगाएंगे, जिसमें अलग-अलग वास्तविक neural voices मिलेंगी, जैसे:

👦 बच्चा — अलग voice

👧 बच्ची — अलग voice

👨 पुरुष — अलग voice

👩 महिला — अलग voice

👴 दादा — अलग आवाज़/धीमी pitch

👵 दादी — अलग आवाज़/धीमी pitch

और हर character के लिए अलग voice चुनने का option रहेगा।

पहले यह करें
आपकी requirements.txt में अभी:

streamlit>=1.40.0
google-genai>=1.0.0
Pillow>=10.0.0
gTTS>=2.5.0
इसे बदलकर यह करें:

streamlit>=1.40.0
google-genai>=1.0.0
Pillow>=10.0.0
gTTS>=2.5.0
edge-tts>=7.0.0
पहले सिर्फ edge-tts>=7.0.0 जोड़कर Commit करें।

उसके बाद मैं आपको अगला पूरा TTS code दूँगा, जिसमें चुनी हुई character voice सच में audio में इस्तेमाल होगी।


Mtlb alag alag awaz me bolega

हाँ, सही तरीके से लगाने पर अलग-अलग character अलग-अलग आवाज़ में बोलेंगे। 👍

उदाहरण कहानी:

राहुल: “दादा जी, आज हम जंगल चलें?”
दादा जी: “हाँ बेटा, लेकिन मेरे साथ रहना।”
पिंकी: “मैं भी चलूँगी!”

Audio में:

🎙️ राहुल → बच्चे की आवाज़
🎙️ दादा जी → बुजुर्ग पुरुष जैसी आवाज़
🎙️ पिंकी → बच्ची की आवाज़

यानी पूरी कहानी एक ही आवाज़ में नहीं चलेगी।

लेकिन इसके लिए हमें अभी आपके gTTS वाले पूरे TTS सिस्टम को बदलना होगा और कहानी को character के dialogue के हिसाब से अलग-अलग audio segments में बनाकर जोड़ना होगा।

आपने edge-tts requirements में जोड़ दिया है तो अब अगला बदलाव यही TTS वाला करेंगे।


File "/mount/src/bacho-ki-kahani/App.py", line 210
                  role = st.selectbox(
                 ^
IndentationError: unexpected indent

हाँ, अभी voice का काम रोकिए। पहले line 210 का indentation ठीक करना है। सबसे सुरक्षित तरीका है पूरा Characters section replace करना।

क्या करें
App.py में:

# ============================================================
# CHARACTERS
# ============================================================
से लेकर इस line तक:

st.markdown("</div>", unsafe_allow_html=True)
पूरा हटाएँ।

फिर यह पूरा code एक बार में paste करें:

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
                "50-60 साल",
                "60-70 साल",
                "70+ साल"
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

        voice_type = st.selectbox(
            "🎙️ आवाज़ चुनें",
            [
                "👦 छोटा बच्चा",
                "👧 छोटी बच्ची",
                "👨 पुरुष",
                "👩 महिला",
                "👴 दादा जी",
                "👵 दादी जी",
                "🐰 मजेदार आवाज़",
                "🐘 भारी आवाज़",
                "🤖 Robot",
                "🎭 Cartoon"
            ],
            key=f"voice_type_{i}"
        )

        if name.strip():

            characters.append({
                "name": name.strip(),
                "age": age,
                "role": role,
                "voice_type": voice_type
            })

st.markdown("</div>", unsafe_allow_html=True)
फिर
Save/Commit → app reload करें।

अभी TTS वाला code बिल्कुल मत छेड़िए।

अगर error फिर भी आए, तो line 200–230 का screenshot भेज दें। मैं उसी line को ठीक कर दूँगा।



Pasted text(3).txt
Document

हाँ, मैंने आपका पूरा uploaded code देख लिया है। 


अभी code में कई जगह indentation और duplicate TTS code की समस्या है। खासकर:

role = st.selectbox(...) में extra indentation है।

MULTI CHARACTER VOICE वाला section if st.session_state.story: के अंदर/बाहर गलत जगह है।

नीचे data=st.session_state.audio... वाला पुराना हिस्सा दोबारा बच गया है।

इसलिए अभी इसे थोड़ा-थोड़ा ठीक करने से फिर error आने की संभावना है।

सबसे अच्छा तरीका: मैं आपके इसी पूरे code को साफ करके एक पूरा corrected App.py बना दूँ, जिसमें:

5 characters

उम्र 70+ तक

हर character का अलग voice option

Edge TTS

dialogue के हिसाब से अलग-अलग आवाज़

Khortha सहित languages

कहानी save

WhatsApp share

Google Analytics

सब एक साथ सही indentation के साथ रहेगा।

अगर आप चाहें तो मैं पूरा final code एक ही बार में दे देता हूँ, जिसे पुराने App.py की जगह पूरा paste करना होगा।


Bahoot jaruri wla kaise kre

हाँ। आपके uploaded code को देखकर सबसे जरूरी बदलाव ये हैं:

🔴 सबसे पहले यही 3 चीजें ठीक करनी हैं
1. role = st.selectbox की indentation
अभी extra spaces हैं, इसी से IndentationError आ रहा है। 


2. पुराना TTS code हटाना जरूरी है
आपके code में नया Edge TTS लगाने के बाद भी पुराना data=st.session_state.audio... वाला हिस्सा बचा हुआ है। इसे हटाना जरूरी है। 


3. Gemini prompt में character dialogue format जोड़ना जरूरी है
अलग-अलग आवाज़ तभी सही character पर लगेगी जब कहानी में dialogue इस तरह आए:

[NARRATOR]: राहुल जंगल की ओर गया।

[राहुल]: दादा जी, मैं आपके साथ चलूँगा।

[दादा जी]: ठीक है बेटा।
🟢 बाकी चीजें अभी मत छेड़िए
Language, WhatsApp, Analytics, Saved Story आदि अभी ठीक रहने दें।

मेरी सलाह: आपके current code में जगह-जगह हाथ से बदलाव करने के बजाय मैं पूरा corrected final App.py दूँ। इससे indentation और duplicate TTS वाली समस्या एक साथ खत्म हो जाएगी।


Pura ek compleye code banao

हाँ। मैंने आपका पूरा corrected App.py बना दिया है। इसमें आपके पुराने code की indentation और duplicate TTS वाली समस्या भी हटा दी गई है।

पूरा App.py डाउनलोड करें

इसमें शामिल है
5 Characters

उम्र 70+ साल तक

हर character के लिए 🎙️ अलग voice option

Edge TTS

Character dialogue के अनुसार अलग आवाज़

Khortha सहित languages

Gemini story generation

Saved Stories

WhatsApp Share

Google Analytics

Bedtime Mode

जरूरी: requirements.txt में यह line भी होनी चाहिए:

edge-tts>=7.0.0
और इस बार पुराने App.py में नीचे-नीचे code जोड़ने के बजाय पूरा पुराना App.py हटाकर यह नया वाला पूरा paste करें। 


App.py
Code


No file chosen
Library
/
App.py


import streamlit as st
from google import genai
import edge_tts
import asyncio
from datetime import datetime
import io
import urllib.parse
import streamlit.components.v1 as components


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

GA_ID = st.secrets.get("GA_MEASUREMENT_ID", "")

if GA_ID:
    components.html(
        f"""
        <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
        <script>
        window.dataLayer = window.dataLayer || [];
        function gtag() {{ dataLayer.push(arguments); }}
        gtag('js', new Date());
        gtag('config', '{GA_ID}');
        </script>
        """,
        height=0
    )


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "story": "",
    "story_title": "",
    "story_data": {},
    "saved_stories": [],
    "audio": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


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
# VOICE OPTIONS
# ============================================================

VOICE_OPTIONS = [
    "👦 छोटा बच्चा",
    "👧 छोटी बच्ची",
    "👨 पुरुष",
    "👩 महिला",
    "👴 दादा जी",
    "👵 दादी जी",
    "🐰 मजेदार आवाज़",
    "🐘 भारी आवाज़",
    "🤖 Robot",
    "🎭 Cartoon",
]

# Available Hindi neural voices are reused with different
# rate/pitch so the selected character styles sound different.
VOICE_MAP = {
    "👦 छोटा बच्चा": {
        "voice": "hi-IN-MadhurNeural",
        "rate": "+15%",
        "pitch": "+8Hz",
    },
    "👧 छोटी बच्ची": {
        "voice": "hi-IN-SwaraNeural",
        "rate": "+12%",
        "pitch": "+10Hz",
    },
    "👨 पुरुष": {
        "voice": "hi-IN-MadhurNeural",
        "rate": "+0%",
        "pitch": "+0Hz",
    },
    "👩 महिला": {
        "voice": "hi-IN-SwaraNeural",
        "rate": "+0%",
        "pitch": "+0Hz",
    },
    "👴 दादा जी": {
        "voice": "hi-IN-MadhurNeural",
        "rate": "-18%",
        "pitch": "-8Hz",
    },
    "👵 दादी जी": {
        "voice": "hi-IN-SwaraNeural",
        "rate": "-15%",
        "pitch": "-5Hz",
    },
    "🐰 मजेदार आवाज़": {
        "voice": "hi-IN-SwaraNeural",
        "rate": "+20%",
        "pitch": "+15Hz",
    },
    "🐘 भारी आवाज़": {
        "voice": "hi-IN-MadhurNeural",
        "rate": "-20%",
        "pitch": "-12Hz",
    },
    "🤖 Robot": {
        "voice": "hi-IN-MadhurNeural",
        "rate": "-5%",
        "pitch": "-15Hz",
    },
    "🎭 Cartoon": {
        "voice": "hi-IN-SwaraNeural",
        "rate": "+18%",
        "pitch": "+12Hz",
    },
}


# ============================================================
# CHARACTERS
# ============================================================

st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown("## 👨‍👩‍👧‍👦 कहानी के पात्र")
st.caption("अधिकतम 5 पात्र जोड़ सकते हैं। हर पात्र की अलग आवाज़ चुन सकते हैं।")

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
                "14-16 साल",
                "17-20 साल",
                "21-30 साल",
                "31-40 साल",
                "41-50 साल",
                "51-60 साल",
                "61-70 साल",
                "70+ साल",
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
                "जानवर",
                "अन्य",
            ],
            key=f"role_{i}"
        )

        voice_type = st.selectbox(
            "🎙️ आवाज़ चुनें",
            VOICE_OPTIONS,
            key=f"voice_type_{i}"
        )

        if name.strip():
            characters.append({
                "name": name.strip(),
                "age": age,
                "role": role,
                "voice_type": voice_type,
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
            "अंतरिक्ष की कहानी",
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
            "20 मिनट",
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
            "اردو (Urdu)",
        ]
    )

conditions = st.text_area(
    "🧠 कहानी में क्या-क्या होना चाहिए?",
    placeholder=(
        "उदाहरण: कहानी में राहुल, एक खरगोश, एक बड़ा पेड़, "
        "फूल और एक छोटा घर होना चाहिए। अंत में राहुल को अच्छी सीख मिलनी चाहिए।"
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
            "दोस्तों के साथ मिलकर रहना",
            "क्रिकेट खेलना",
            "फुटबॉल खेलना",
            "बैडमिंटन खेलना",
            "दौड़ना",
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
            "बहुत देर मोबाइल चलाना",
            "गाली देना",
            "चोरी करना",
        ]
    )
    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# BEDTIME
# ============================================================

st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown("## 🌙 Bedtime Mode")

bedtime = st.toggle("🌙 सोने वाली शांत कहानी")

if bedtime:
    music = st.selectbox(
        "🎵 Music mood",
        [
            "Soft Lullaby",
            "Rain",
            "Forest Night",
            "Ocean",
            "Soft Piano",
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
            "GEMINI_API_KEY नहीं मिली। Streamlit Secrets में API key डालें।"
        )

    client = genai.Client(api_key=API_KEY)

    if characters:
        character_text = "\n".join(
            [
                f"{x['name']} - {x['age']} - {x['role']} - Voice: {x['voice_type']}"
                for x in characters
            ]
        )
    else:
        character_text = "कोई नाम नहीं दिया गया।"

    good_text = ", ".join(good_habits) if good_habits else "कोई विशेष नहीं"
    bad_text = ", ".join(bad_habits) if bad_habits else "कोई विशेष नहीं"

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
2. भाषा उम्र के अनुसार सरल और आकर्षक हो।
3. दिए गए नामों का स्वाभाविक इस्तेमाल करें।
4. कहानी में शुरुआत, समस्या, समाधान और सुंदर ending हो।
5. अच्छी आदत को कहानी के अंदर स्वाभाविक रूप से दिखाएं।
6. गलत आदत को सकारात्मक तरीके से समझाएं।
7. कहानी सुनने में मजेदार हो।
8. अनावश्यक डर या हिंसा न हो।
9. कहानी में जानवर, फूल, पेड़, घर आदि तभी डालें जब conditions में हों।
10. Bedtime mode में कहानी शांत और सुकून देने वाली हो।
11. संवादों को character के नाम के साथ EXACT इस format में लिखें:
[पात्र का नाम]: dialogue
12. Narration को EXACT इस format में लिखें:
[NARRATOR]: narration
13. हर dialogue और narration अलग line में हो।
14. पात्र का नाम वही रखें जो ऊपर दिया गया है।
15. STORY के अंदर केवल कहानी और narration/dialogue रखें।
16. Dialogue को natural, बच्चों के लिए आकर्षक और छोटा रखें।

नीचे EXACT format में जवाब दें:

TITLE:
छोटा और प्यारा title

STORY:
[NARRATOR]: कहानी की शुरुआत।
[पात्र का नाम]: संवाद।
[NARRATOR]: आगे की narration।
[दूसरे पात्र का नाम]: संवाद।

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
        "image_prompt": "",
    }

    markers = [
        ("TITLE:", "title"),
        ("STORY:", "story"),
        ("LESSON:", "lesson"),
        ("GOOD_HABITS:", "good"),
        ("AVOID:", "avoid"),
        ("SCENES:", "scenes"),
        ("IMAGE_PROMPT:", "image_prompt"),
    ]

    found = []

    for marker, key in markers:
        pos = text.find(marker)
        if pos != -1:
            found.append((pos, marker, key))

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
# EDGE TTS
# ============================================================

async def make_voice(text, voice, rate, pitch):
    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=rate,
        pitch=pitch,
    )

    audio = bytearray()

    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio.extend(chunk["data"])

    return bytes(audio)


def create_multi_voice_audio(story_text, characters):
    voice_lookup = {}

    for character in characters:
        voice_type = character.get(
            "voice_type",
            "👨 पुरुष"
        )

        voice_data = VOICE_MAP.get(
            voice_type,
            VOICE_MAP["👨 पुरुष"]
        )

        voice_lookup[
            character["name"].strip().lower()
        ] = voice_data

    # Narrator default
    narrator_voice = {
        "voice": "hi-IN-SwaraNeural",
        "rate": "-5%",
        "pitch": "0Hz",
    }

    lines = story_text.splitlines()
    audio_parts = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        speaker = None
        dialogue = line

        if line.startswith("[") and "]" in line:
            end = line.find("]")
            speaker = line[1:end].strip()
            dialogue = line[end + 1:].strip()

        if not dialogue:
            continue

        if speaker and speaker.lower() in voice_lookup:
            voice_data = voice_lookup[speaker.lower()]
        else:
            voice_data = narrator_voice

        audio_part = asyncio.run(
            make_voice(
                dialogue,
                voice_data["voice"],
                voice_data["rate"],
                voice_data["pitch"],
            )
        )

        if audio_part:
            audio_parts.append(audio_part)

    return b"".join(audio_parts)


# ============================================================
# CREATE STORY BUTTON
# ============================================================

st.markdown("## ✨ कहानी बनाइए")

if st.button(
    "🌈 ✨ अभी कहानी बनाओ ✨ 🌈",
    type="primary",
    use_container_width=True
):
    with st.spinner("🧚 AI आपकी कहानी बना रहा है..."):
        try:
            raw = generate_story()
            data = parse_story(raw)

            st.session_state.story = data["story"]
            st.session_state.story_title = data["title"]
            st.session_state.story_data = data
            st.session_state.audio = None

            st.success("🎉 कहानी तैयार है!")

        except Exception as e:
            st.error(f"कहानी बनाने में समस्या: {e}")


# ============================================================
# SHOW STORY
# ============================================================

if st.session_state.story:
    data = st.session_state.get("story_data", {})

    st.markdown("---")

    st.markdown(
        f"""
        <div class="card">
        <div style="text-align:center;font-size:50px;">
        📖 🐰 🌳 🌸 🦋
        </div>

        <h1 style="text-align:center;color:#ff6475;">
        {st.session_state.story_title}
        </h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="story">', unsafe_allow_html=True)
    st.markdown(st.session_state.story)
    st.markdown("</div>", unsafe_allow_html=True)

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

    with st.expander("🖼️ कहानी के Visual Scenes देखें"):
        st.write(
            data.get(
                "scenes",
                "Scenes उपलब्ध नहीं हैं।"
            )
        )

        st.markdown("### 🎨 Image Prompt")

        st.code(
            data.get(
                "image_prompt",
                ""
            )
        )

    # ========================================================
    # MULTI CHARACTER VOICE UI
    # ========================================================

    st.markdown("## 🔊 कहानी सुनें")

    st.info(
        "🎙️ कहानी के dialogue के अनुसार चुनी हुई character voice इस्तेमाल होगी।"
    )

    if st.button(
        "🎙️ अलग-अलग Character Voices में कहानी सुनाएँ",
        use_container_width=True
    ):
        with st.spinner(
            "🎙️ अलग-अलग आवाज़ें तैयार हो रही हैं..."
        ):
            try:
                audio_data = create_multi_voice_audio(
                    st.session_state.story,
                    characters
                )

                if not audio_data:
                    raise Exception(
                        "Audio तैयार नहीं हुआ। कहानी में dialogue format जाँचें।"
                    )

                st.session_state.audio = audio_data

                st.success(
                    "🎉 अलग-अलग character voices तैयार हैं!"
                )

            except Exception as e:
                st.error(
                    f"Voice बनाने में समस्या: {e}"
                )

    if st.session_state.audio:
        st.audio(
            st.session_state.audio,
            format="audio/mp3"
        )

        st.download_button(
            "⬇️ Audio Save करें",
            data=st.session_state.audio,
            file_name="bal_kahani_multi_voice.mp3",
            mime="audio/mp3",
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

        st.success("❤️ कहानी Save हो गई!")


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
            st.write(item["story"])
else:
    st.info("अभी कोई saved story नहीं है।")


# ============================================================
# WHATSAPP SHARE
# ============================================================

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
