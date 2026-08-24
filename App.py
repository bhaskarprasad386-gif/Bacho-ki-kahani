import streamlit as st
import asyncio
import edge_tts
import tempfile
import os
import base64

# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="Phonic Picture A-Z",
    page_icon="🔤",
    layout="wide"
)

# ============================================================
# PHONIC DATA
# ============================================================

PHONICS = [
    {
        "letter": "A",
        "word": "Apple",
        "picture": "🍎",
        "sound": "Aaa"
    },
    {
        "letter": "B",
        "word": "Ball",
        "picture": "⚽",
        "sound": "Buh"
    },
    {
        "letter": "C",
        "word": "Cat",
        "picture": "🐱",
        "sound": "Kuh"
    },
    {
        "letter": "D",
        "word": "Dog",
        "picture": "🐶",
        "sound": "Duh"
    },
    {
        "letter": "E",
        "word": "Egg",
        "picture": "🥚",
        "sound": "Eh"
    },
    {
        "letter": "F",
        "word": "Fish",
        "picture": "🐟",
        "sound": "Fff"
    },
    {
        "letter": "G",
        "word": "Goat",
        "picture": "🐐",
        "sound": "Guh"
    },
    {
        "letter": "H",
        "word": "Hat",
        "picture": "🎩",
        "sound": "Hhh"
    },
    {
        "letter": "I",
        "word": "Igloo",
        "picture": "🏠",
        "sound": "Ih"
    },
    {
        "letter": "J",
        "word": "Jug",
        "picture": "🏺",
        "sound": "Juh"
    },
    {
        "letter": "K",
        "word": "Kite",
        "picture": "🪁",
        "sound": "Kuh"
    },
    {
        "letter": "L",
        "word": "Lion",
        "picture": "🦁",
        "sound": "Lll"
    },
    {
        "letter": "M",
        "word": "Mango",
        "picture": "🥭",
        "sound": "Mmm"
    },
    {
        "letter": "N",
        "word": "Nest",
        "picture": "🪺",
        "sound": "Nnn"
    },
    {
        "letter": "O",
        "word": "Orange",
        "picture": "🍊",
        "sound": "Ooo"
    },
    {
        "letter": "P",
        "word": "Parrot",
        "picture": "🦜",
        "sound": "Puh"
    },
    {
        "letter": "Q",
        "word": "Queen",
        "picture": "👑",
        "sound": "Kwuh"
    },
    {
        "letter": "R",
        "word": "Rabbit",
        "picture": "🐰",
        "sound": "Rrr"
    },
    {
        "letter": "S",
        "word": "Sun",
        "picture": "☀️",
        "sound": "Sss"
    },
    {
        "letter": "T",
        "word": "Tiger",
        "picture": "🐯",
        "sound": "Tuh"
    },
    {
        "letter": "U",
        "word": "Umbrella",
        "picture": "☂️",
        "sound": "Uh"
    },
    {
        "letter": "V",
        "word": "Van",
        "picture": "🚐",
        "sound": "Vvv"
    },
    {
        "letter": "W",
        "word": "Watch",
        "picture": "⌚",
        "sound": "Wuh"
    },
    {
        "letter": "X",
        "word": "Xylophone",
        "picture": "🎵",
        "sound": "Kss"
    },
    {
        "letter": "Y",
        "word": "Yak",
        "picture": "🐂",
        "sound": "Yuh"
    },
    {
        "letter": "Z",
        "word": "Zebra",
        "picture": "🦓",
        "sound": "Zzz"
    }
]

# ============================================================
# EDGE TTS
# ============================================================

VOICE = "en-US-AriaNeural"


async def make_audio(text, file_path):

    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE,
        rate="-5%",
        volume="+0%"
    )

    await communicate.save(file_path)


def generate_audio(text):

    file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp3"
    )

    file_path = file.name
    file.close()

    try:

        asyncio.run(
            make_audio(
                text,
                file_path
            )
        )

        with open(
            file_path,
            "rb"
        ) as f:

            audio_data = f.read()

        return audio_data

    finally:

        if os.path.exists(file_path):

            os.remove(file_path)


# ============================================================
# PLAY VOICE
# ============================================================

def play_voice(text):

    try:

        audio_data = generate_audio(text)

        audio_base64 = base64.b64encode(
            audio_data
        ).decode()

        audio_html = f"""
        <audio autoplay>
            <source
                src="data:audio/mp3;base64,{audio_base64}"
                type="audio/mpeg"
            >
        </audio>
        """

        st.markdown(
            audio_html,
            unsafe_allow_html=True
        )

    except Exception as error:

        st.error(
            f"Voice बनाने में समस्या: {error}"
        )


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        margin-top: 10px;
    }

    .subtitle {
        text-align: center;
        font-size: 19px;
        color: #666666;
        margin-bottom: 25px;
    }

    .card {

        background: white;

        border-radius: 22px;

        padding: 18px;

        margin-bottom: 12px;

        text-align: center;

        border: 2px solid #eeeeee;

        box-shadow:
        0 4px 12px
        rgba(0,0,0,0.10);

        min-height: 290px;
    }

    .letter {

        font-size: 55px;

        font-weight: 900;
    }

    .picture {

        font-size: 72px;

        margin: 8px;
    }

    .word {

        font-size: 27px;

        font-weight: 700;
    }

    .sound {

        font-size: 20px;

        color: #555555;

        margin-top: 6px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="title">🔤 Phonic Picture A-Z</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'देखो • पढ़ो • सुनो • दोहराओ'
    '</div>',
    unsafe_allow_html=True
)

st.info(
    "👆 किसी भी कार्ड के 🔊 बटन को दबाकर "
    "उसका phonic sound और word सुनें।"
)

# ============================================================
# A-Z CARDS
# ============================================================

for row_start in range(0, 26, 4):

    row_data = PHONICS[
        row_start:row_start + 4
    ]

    columns = st.columns(4)

    for column, item in zip(
        columns,
        row_data
    ):

        with column:

            letter = item["letter"]
            word = item["word"]
            picture = item["picture"]
            sound = item["sound"]

            # ----------------------------
            # CARD
            # ----------------------------

            st.markdown(
                f"""
                <div class="card">

                    <div class="letter">
                        {letter}
                    </div>

                    <div class="picture">
                        {picture}
                    </div>

                    <div class="word">
                        {word}
                    </div>

                    <div class="sound">
                        🔊 {sound}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            # ----------------------------
            # VOICE BUTTON
            # ----------------------------

            if st.button(
                f"🔊 सुनें {letter}",
                key=f"button_{letter}",
                use_container_width=True
            ):

                text_to_speak = (
                    f"{sound}. {word}."
                )

                play_voice(
                    text_to_speak
                )

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div style="
        text-align:center;
        font-size:17px;
        color:#777;
    ">
        🌟 Learn Phonics with Pictures 🌟
    </div>
    """,
    unsafe_allow_html=True
)
