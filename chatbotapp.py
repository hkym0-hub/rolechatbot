import streamlit as st
from openai import OpenAI

# --- Page Title (from screenshot) ---
st.title("🎭 Role-based Creative Chatbot")

# --- Sidebar (for settings, as in screenshot) ---
with st.sidebar:
    st.title("🔑 API & Role Settings")
    
    # 1. API Key input
    api_key = st.text_input("Enter your OpenAI API Key:", type="password")
    
    # 2. Coach Roles (from your original code)
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

    # 3. Info Box (from screenshot)
    st.info(f"{selected_role_prompt}")
    
    # 4. Image Generation Checkbox (moved from main area)
    generate_image = st.checkbox("Show example image for this advice")

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

# --- Handle new user input ---
user_input = st.chat_input("e.g., How can I express sadness in movement?")

if user_input:
    # 1. Add user message to state
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.spinner(f"🎨 {selected_role_key} is thinking..."):
        # 2. Prepare messages for API
        # (Filter out image URLs, keeping only text context)
        api_messages = []
        for msg in st.session_state.messages:
            if msg["role"] == "system":
                api_messages.append({"role": "system", "content": msg["content"]})
            elif msg["role"] == "user":
                api_messages.append({"role": "user", "content": msg["content"]})
            elif msg["role"] == "assistant" and "text_content" in msg:
                # Only send assistant's text replies as history
                api_messages.append({"role": "assistant", "content": msg["text_content"]})

        # 3. Get text reply from OpenAI
        chat_resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=api_messages,
            temperature=0.7
        )
        reply_text = chat_resp.choices[0].message.content
        # Add text reply to state
        st.session_state.messages.append({"role": "assistant", "text_content": reply_text})

        # 4. Generate example image if checked
        if generate_image:
            with st.spinner("Generating example image..."):
                # Prompt based on the advice, not the question
                image_prompt = f"An illustrative example for this art advice: {reply_text}. Style should be a clear, educational art diagram or sketch."
                try:
                    image_resp = client.images.generate(
                        model="dall-e-3", # Using DALL-E 3
                        prompt=image_prompt,
                        size="1024x1024" # 512x512 is also an option
                    )
                    image_url = image_resp.data[0].url
                    # Add image reply to state
                    st.session_state.messages.append({"role": "assistant", "image_url": image_url})
                except Exception as e:
                    st.error(f"Could not generate image: {e}")

# --- Display chat history (runs every time) ---
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue  # Don't display the system prompt
    
    with st.chat_message(msg["role"]):
        if msg["role"] == "user":
            st.markdown(msg["content"])
        
        elif msg["role"] == "assistant":
            # Display text content if it exists
            if "text_content" in msg:
                st.markdown(msg["text_content"])
            # Display image if it exists
            if "image_url" in msg:
                st.image(msg["image_url"], caption="Example Illustration")

# --- Footer (from screenshot) ---
st.caption("Built for 'Art & Advanced Big Data' • Prof. Jahwan Koo (SKKU)")
