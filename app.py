import streamlit as st
from google import genai

# -------------------------------
# PAGE SETTINGS
# -------------------------------
st.set_page_config(
    page_title="Lucky AI Chat",
    page_icon="🤖",
    layout="centered"
)

# -------------------------------
# CUSTOM CSS
# -------------------------------
st.markdown("""
<style>

.block-container {
    max-width: 850px;
    padding-top: 2rem;
    padding-bottom: 6rem;
}

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 5px;
}

.sub-title {
    text-align: center;
    color: gray;
    margin-bottom: 35px;
}

.stChatMessage {
    border-radius: 16px;
    padding: 8px;
    margin-bottom: 10px;
}

[data-testid="stChatInput"] {
    border-radius: 18px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# GEMINI API KEY
# -------------------------------
try:
    client = genai.Client(
        api_key=st.secrets["GEMINI_API_KEY"]
    )
except Exception:
    st.error("⚠️ Gemini API key missing hai.")
    st.info("Streamlit Secrets mein GEMINI_API_KEY add karo.")
    st.stop()

# -------------------------------
# SIDEBAR
# -------------------------------
with st.sidebar:

    st.title("🤖 Lucky AI")

    st.write(
        "Your personal AI assistant powered by artificial intelligence."
    )

    st.divider()

    if st.button(
        "🗑 Clear Chat",
        use_container_width=True
    ):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content":
                "Assalam-o-Alaikum 👋 I am Lucky AI. How can I help you today?"
            }
        ]

        st.rerun()

    st.divider()

    st.caption("Developed by Abdul Hanan")
    st.caption("Lucky Brand AI")

# -------------------------------
# MAIN HEADING
# -------------------------------
st.markdown(
    '<div class="main-title">🤖 Lucky AI Chat</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Ask anything. Learn anything.</div>',
    unsafe_allow_html=True
)

# -------------------------------
# CHAT HISTORY
# -------------------------------
if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "assistant",
            "content":
            "Assalam-o-Alaikum 👋 I am Lucky AI. How can I help you today?"
        }
    ]

# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------------------
# USER INPUT
# -------------------------------
user_prompt = st.chat_input(
    "Ask Lucky AI anything..."
)

if user_prompt:

    # User message save
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(user_prompt)

    # -------------------------------
    # BUILD CONVERSATION
    # -------------------------------
    conversation = """
You are Lucky AI, a helpful personal AI assistant created by Abdul Hanan.

Rules:
- Be friendly and helpful.
- If user writes Roman Urdu, reply in Roman Urdu.
- If user writes Urdu, reply in Urdu.
- If user writes English, reply in English.
- Explain difficult concepts simply.
- Do not repeatedly introduce yourself.
- Keep answers clear and natural.

Conversation:
"""

    for msg in st.session_state.messages:

        if msg["role"] == "user":
            conversation += f"\nUser: {msg['content']}"

        else:
            conversation += f"\nLucky AI: {msg['content']}"

    conversation += "\nLucky AI:"

    # -------------------------------
    # GEMINI RESPONSE
    # -------------------------------
    with st.chat_message("assistant"):

        with st.spinner("Lucky AI is thinking..."):

            try:

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=conversation
                )

                ai_reply = response.text

                st.markdown(ai_reply)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": ai_reply
                    }
                )

            except Exception as e:

                st.error(
                    "⚠️ Lucky AI temporarily response nahi de pa raha."
                )

                st.caption(
                    "API key, Gemini free quota ya internet connection check karein."
                )
