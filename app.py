import streamlit as st
from openai import OpenAI

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

# ---------------------------------
# API KEY
# ---------------------------------
try:
    client = OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"]
    )
except Exception:
    st.error("⚠️ API key is missing. Add OPENAI_API_KEY in Streamlit Secrets.")
    st.stop()

# ---------------------------------
# SIDEBAR
# ---------------------------------
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

        st.session_state.messages = []

        st.rerun()

    st.divider()

    st.caption("Developed by Abdul Hanan")
    st.caption("Lucky Brand AI")

# ---------------------------------
# HEADING
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
    # AI RESPONSE
    # ---------------------------------
    with st.chat_message("assistant"):

        with st.spinner("Lucky AI is thinking..."):

            try:

                conversation = []

                for msg in st.session_state.messages:

                    conversation.append(
                        {
                            "role": msg["role"],
                            "content": msg["content"]
                        }
                    )

                response = client.responses.create(

                    model="gpt-5",

                    instructions="""
You are Lucky AI, a helpful personal AI assistant.

Be friendly, intelligent and concise.

If the user speaks Urdu, Roman Urdu or English,
reply naturally in the same language.

Explain difficult concepts in simple language.
""",

                    input=conversation
                )

                ai_reply = response.output_text

                st.markdown(ai_reply)

                # Save assistant response
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": ai_reply
                    }
                )

            except Exception as e:

                st.error("❌ AI response failed.")

                st.code(str(e))
