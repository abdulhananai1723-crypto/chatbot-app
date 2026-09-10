import streamlit as st
from google import genai

# ---------------------------------
# PAGE SETTINGS
# ---------------------------------
st.set_page_config(
    page_title="Lucky AI Chat",
    page_icon="🤖",
    layout="centered"
)

# ---------------------------------
# CUSTOM CSS
# ---------------------------------
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
    margin-bottom: 30px;
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

# ---------------------------------
# GEMINI API SETUP
# ---------------------------------
try:
    gemini_key = st.secrets["GEMINI_API_KEY"]

    client = genai.Client(
        api_key=gemini_key
    )

except KeyError:
    st.error("⚠️ GEMINI_API_KEY missing hai.")
    st.info(
        'Streamlit → Manage app → Settings → Secrets mein ye add karo:\n\n'
        'GEMINI_API_KEY = "apni_gemini_api_key"'
    )
    st.stop()

except Exception as e:
    st.error("⚠️ Gemini setup error.")
    st.code(str(e))
    st.stop()

# ---------------------------------
# SIDEBAR
# ---------------------------------
with st.sidebar:

    st.title("🤖 Lucky AI")

    st.write(
        "Your personal AI assistant powered by Gemini."
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

# ---------------------------------
# MAIN HEADING
# ---------------------------------
st.markdown(
    '<div class="main-title">🤖 Lucky AI Chat</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Ask anything. Learn anything.</div>',
    unsafe_allow_html=True
)

# ---------------------------------
# SESSION STATE
# ---------------------------------
if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "assistant",
            "content":
            "Assalam-o-Alaikum 👋 I am Lucky AI. How can I help you today?"
        }
    ]

# ---------------------------------
# DISPLAY OLD MESSAGES
# ---------------------------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------------------
# USER INPUT
# ---------------------------------
user_prompt = st.chat_input(
    "Ask Lucky AI anything..."
)

if user_prompt:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # ---------------------------------
    # PREPARE FULL CONVERSATION
    # ---------------------------------
    conversation = """
You are Lucky AI, a helpful AI assistant created by Abdul Hanan.

Instructions:
- Be friendly and helpful.
- Reply in the same language as the user.
- If user writes Roman Urdu, reply in Roman Urdu.
- If user writes Urdu, reply in Urdu.
- If user writes English, reply in English.
- Explain difficult things simply.
- Keep answers natural and clear.
- Do not repeatedly introduce yourself.
- You are called Lucky AI.

Conversation:
"""

    for msg in st.session_state.messages:

        if msg["role"] == "user":
            conversation += f"\nUser: {msg['content']}"

        elif msg["role"] == "assistant":
            conversation += f"\nLucky AI: {msg['content']}"

    conversation += "\nLucky AI:"

    # ---------------------------------
    # GEMINI RESPONSE
    # ---------------------------------
    with st.chat_message("assistant"):

        with st.spinner("Lucky AI is thinking..."):

            try:

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=conversation
                )

                ai_reply = response.text

                if ai_reply:

                    st.markdown(ai_reply)

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": ai_reply
                        }
                    )

                else:
                    st.error(
                        "⚠️ Lucky AI ne empty response return kiya."
                    )

            except Exception as e:

                error_text = str(e)

                st.error(
                    "❌ Lucky AI response generate nahi kar saka."
                )

                if "429" in error_text:
                    st.warning(
                        "Gemini free quota temporarily complete ho sakta hai. "
                        "Thori dair baad dobara try karo."
                    )

                elif "API_KEY" in error_text.upper():
                    st.warning(
                        "Gemini API key ko dobara check karo."
                    )

                else:
                    st.code(error_text)
