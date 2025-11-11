import streamlit as st
import requests

st.title("🎨 AI Art Coach (Hugging Face API Key Input)")

st.markdown("""
Welcome! Enter your Hugging Face API key below to use the AI Art Coach.
""")

# --- API Key input in the app ---
hf_api_key = st.text_input("Enter your Hugging Face API Key:", type="password")

if not hf_api_key:
    st.warning("🔑 Please enter your API key to continue.")
    st.stop()

HF_MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
headers = {"Authorization": f"Bearer {hf_api_key}"}

# --- Define Coach Roles ---
coach_roles = {
    "🖍️ Drawing Coach": "You are a patient drawing coach for beginners. Help with sketching, line, proportion, perspective, and observation.",
    "🎨 Color Coach": "You are a color theory coach. Explain color harmony, mood, mixing, and practical palette design.",
    "🪶 Texture Coach": "You are a texture and materials coach. Teach rendering of surfaces like fur, glass, cloth, brushwork, and layering.",
    "🧠 Composition Coach": "You are a composition coach. Teach visual storytelling, balance, contrast, focal points, and layout.",
    "👩‍🏫 General Art Teacher": "You are a general art teacher who explains concepts clearly, encourages creativity, and answers general art questions.",
    "🌟 Overall Art Advisor": "You are an overall art advisor. Give guidance combining drawing, color, texture, and composition. Help beginners improve step-by-step."
}

selected_role = st.selectbox("Choose your Art Coach:", list(coach_roles.keys()))

# --- Initialize chat memory ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Reset conversation when switching coach
if "current_role" not in st.session_state or st.session_state["current_role"] != selected_role:
    st.session_state["messages"] = [{"role": "system", "content": coach_roles[selected_role]}]
    st.session_state["current_role"] = selected_role

# --- User input ---
user_input = st.chat_input("Ask your coach a question...")

def get_hf_response(prompt):
    payload = {"inputs": prompt}
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=60)
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and "generated_text" in result[0]:
                return result[0]["generated_text"]
            elif isinstance(result, dict) and "error" in result:
                return f"Error from model: {result['error']}"
            else:
                return str(result)
        else:
            return f"Request failed with status {response.status_code}"
    except Exception as e:
        return f"Exception: {e}"

# --- Chat processing ---
if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.spinner(f"🎨 {selected_role} is thinking..."):
        conversation_text = ""
        for msg in st.session_state["messages"]:
            role = "User" if msg["role"] == "user" else "Coach"
            conversation_text += f"{role}: {msg['content']}\n"
        conversation_text += "Coach:"

        reply = get_hf_response(conversation_text)
        st.session_state["messages"].append({"role": "assistant", "content": reply})

# --- Display conversation ---
for msg in st.session_state["messages"][1:]:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    else:
        st.chat_message("assistant").markdown(msg["content"])

