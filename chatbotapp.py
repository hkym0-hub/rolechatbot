import streamlit as st
from openai import OpenAI

# --- Page Title ---
st.title("🎭 Role-based Art Coach Chatbot")

# --- Sidebar Settings ---
with st.sidebar:
    st.title("🔑 API & Role Settings")
    
    # 1. API Key input
    api_key = st.text_input("Enter your OpenAI API Key:", type="password")
    
    # 2. Coach Roles
    coach_roles = {
        "🖍️ Drawing Coach": "You are a patient drawing coach for beginners. Help with sketching, line, proportion, perspective, and observation.",
        "🎨 Color Coach": "You are a color theory coach. Explain color harmony, mood, mixing, and practical palette design.",
        "🪶 Texture Coach": "You are a texture and materials coach. Teach rendering of surfaces like fur, glass, cloth, brushwork, and layering.",
        "🧠 Composition Coach": "You are a composition coach. Teach visual storytelling, balance, contrast, focal points, and layout.",
        "👩‍🏫 General Art Teacher": "You are a general art teacher who explains concepts clearly, encourages creativity, and answers general art questions.",
        "🌟 Overall Art Advisor": "You are an overall art advisor. Give guidance combining drawing, color, texture, and composition. Help beginners improve step-by-step."
    }

    selected_role_key = st.selectbox("Choose a role:", list(coach_roles.keys()))
    selected_role_prompt = coach_roles[selected_role_key]

    st.info(f"{selected_role_prompt}")
    
    # 3. Optional Customizations
    st.subheader("🛠️ Optional Enhancements")
    show_steps = st.checkbox("Provide step-by-step instructions")
    show_exercises = st.checkbox("Include exercises / mini-quizzes")
    show_tables = st.checkbox("Include comparison tables")
    show_references = st.checkbox("Include links to tutorials / references")

# --- API Key Check ---
if not api_key:
    st.warning("🔑 Please enter your OpenAI API key in the sidebar to continue.")
    st.stop()

# Initialize OpenAI client
client = OpenAI(api_key=api_key.strip())

# --- Initialize conversation state ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": selected_role_prompt}]

# Reset chat if role changes
if "current_role" not in st.session_state or st.session_state.current_role != selected_role_key:
    st.session_state.messages = [{"role": "system", "content": selected_role_prompt}]
    st.session_state.current_role = selected_role_key

# --- User input ---
user_input = st.chat_input("Ask your coach a question...")

if user_input:
    # 1. Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 2. Build system enhancements
    extra_instructions = ""
    if show_steps:
        extra_instructions += " Break down your answer into clear step-by-step instructions."
    if show_exercises:
        extra_instructions += " Suggest a short exercise or mini-quiz related to the topic."
    if show_tables:
        extra_instructions += " Include comparison tables where helpful."
    if show_references:
        extra_instructions += " Provide links to relevant free online tutorials or resources."
    
    with st.spinner(f"🎨 {selected_role_key} is thinking..."):
        # Prepare messages for OpenAI
        api_messages = []
        for msg in st.session_state.messages:
            if msg["role"] == "system":
                # Append extra instructions only to system prompt
                api_messages.append({"role": "system", "content": msg["content"] + extra_instructions})
            else:
                api_messages.append(msg)
        
        # Get response
        chat_resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=api_messages,
            temperature=0.7
        )
        reply_text = chat_resp.choices[0].message.content
        
        # Add to state
        st.session_state.messages.append({"role": "assistant", "text_content": reply_text})

# --- Display chat ---
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue  # don't display system
    with st.chat_message(msg["role"]):
        if msg["role"] == "user":
            st.markdown(msg["content"])
        elif msg["role"] == "assistant":
            st.markdown(msg.get("text_content", ""))
            
# --- Footer ---
st.caption("Built for 'Art & Advanced Big Data' • Prof. Jahwan Koo (SKKU)")
