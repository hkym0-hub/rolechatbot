import streamlit as st
from openai import OpenAI

st.title("🎨 AI Art Coach (OpenAI GPT)")

# --- API Key input ---
api_key = st.text_input("Enter your OpenAI API Key:", type="password")
if not api_key:
    st.warning("🔑 Please enter your OpenAI API key to continue.")
    st.stop()

client = OpenAI(api_key=api_key)

# --- Coach Roles ---
coach_roles = {
    "🖍️ Drawing Coach": "You are a patient drawing coach for beginners. Help with sketching, line, proportion, perspective, and observation.",
    "🎨 Color Coach": "You are a color theory coach. Explain color harmony, mood, mixing, and practical palette design.",
    "🪶 Texture Coach": "You are a texture and materials coach. Teach rendering of surfaces like fur, glass, cloth, brushwork, and layering.",
    "🧠 Composition Coach": "You are a composition coach. Teach visual storytelling, balance, contrast, focal points, and layout.",
    "👩‍🏫 General Art Teacher": "You are a general art teacher who explains concepts clearly, encourages creativity, and answers general art questions.",
    "🌟 Overall Art Advisor": "You are an overall art advisor. Give guidance combining drawing, color, texture, and composition. Help beginners improve step-by-step."
}

selected_role = st.selectbox("Choose your Art Coach:", list(coach_roles.keys()))

# --- Initialize conversation ---
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": coach_roles[selected_role]}]

# Reset conversation if switching role
if "current_role" not in st.session_state or st.session_state["current_role"] != selected_role:
    st.session_state["messages"] = [{"role": "system", "content": coach_roles[selected_role]}]
    st.session_state["current_role"] = selected_role

# --- User input ---
user_input = st.chat_input("Ask your coach a question...")

if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.spinner(f"🎨 {selected_role} is thinking..."):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state["messages"],
            temperature=0.7
        )
        reply = response.choices[0].message.content
        st.session_state["messages"].append({"role": "assistant", "content": reply})

# --- Display chat ---
for msg in st.session_state["messages"][1:]:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    else:
        st.chat_message("assistant").markdown(msg["content"])
