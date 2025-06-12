import streamlit as st
import os
import tempfile
from ingestion import ingest_pdf
from retrieval import get_vector_db, get_answer_from_query
import time
import json

# Configure page with custom theme and layout
st.set_page_config(
    page_title="📘 Chat with your PDF",
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
        border-radius: 10px;
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        padding: 1rem;
        border-radius: 8px;
        background-color: white !important;
        color: #333 !important;
        border: 1px solid #ddd !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        text-align: left !important;
        height: auto !important;
        white-space: normal !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        border-color: #1e88e5 !important;
        animation: glow 2s infinite;
    }
    .stButton>button:disabled {
        background-color: #f5f5f5 !important;
        cursor: not-allowed;
        transform: none;
    }
    .persona-selector {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .persona-selector h3 {
        color: #1e88e5;
        margin-bottom: 1.5rem;
        text-align: center;
        font-size: 1.5rem;
    }
    /* Fix image container styling */
    .stImage {
        margin: 0 !important;
        padding: 0 !important;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .stImage > img {
        border-radius: 8px;
        width: 100% !important;
        height: 100px !important;
        object-fit: cover;
        margin-bottom: 0 !important;
        transition: all 0.3s ease;
    }
    /* Special styling for Naruto's image */
    [data-testid="stImage"] img[src*="naruto"] {
        object-fit: contain !important;
        background-color: #f0f2f6;
        padding: 4px;
        border: 2px solid #ff9800;
    }
    /* Hover effect for all persona images */
    .stImage > img:hover {
        transform: scale(1.02);
    }
    /* Adjust columns spacing */
    .st-emotion-cache-12w0qpk {
        gap: 1.5rem !important;
    }
    /* Improve button text layout */
    .stButton>button>div {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }
    .persona-name {
        font-weight: bold;
        font-size: 1.1em;
        color: #1e88e5;
        margin-bottom: 0.25rem;
    }
    .persona-description {
        font-size: 0.9em;
        color: #666;
        line-height: 1.4;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        animation: fadeIn 0.5s;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 5px solid #1e88e5;
    }
    .assistant-message {
        background-color: #f5f5f5;
        border-left: 5px solid #4CAF50;
    }
    .chat-history-title {
        color: #1e88e5;
        text-align: center;
        padding: 1rem;
        border-bottom: 2px solid #e0e0e0;
        margin-bottom: 1rem;
    }
    .chat-history-item {
        padding: 0.5rem;
        margin: 0.5rem 0;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .chat-history-item:hover {
        background-color: #f0f2f6;
    }
    .chat-history-item.selected {
        background-color: #e3f2fd;
        border-left: 3px solid #1e88e5;
    }
    .sidebar .chat-history {
        max-height: 80vh;
        overflow-y: auto;
        padding-right: 1rem;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    /* Override Streamlit's default file size limit text */
    .st-emotion-cache-1rpn56r {
        display: none;
    }
    .st-emotion-cache-1rpn56r::after {
        content: "Limit 10MB per file • PDF";
        display: block;
    }
    @keyframes ninja-flip {
        0% { transform: rotateY(0deg); }
        50% { transform: rotateY(180deg); }
        100% { transform: rotateY(360deg); }
    }
    @keyframes ninja-jump {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-20px); }
    }
    @keyframes bot-wave {
        0%, 100% { transform: rotate(0deg); }
        25% { transform: rotate(-20deg); }
        75% { transform: rotate(20deg); }
    }
    .ninja {
        font-size: 3rem;
        display: inline-block;
        animation: ninja-flip 2s infinite, ninja-jump 1s infinite;
    }
    .processing-text {
        color: #1e88e5;
        font-size: 1.5rem;
        margin: 1rem 0;
    }
    .bot-emoji {
        font-size: 2rem;
        display: inline-block;
        animation: bot-wave 2s infinite;
    }
    .typewriter {
        overflow: hidden;
        white-space: pre-wrap;
        animation: typing 2s steps(40, end);
    }
    @keyframes typing {
        from { width: 0 }
        to { width: 100% }
    }
    /* Persona Guide Animations */
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }

    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }

    @keyframes glow {
        0% { box-shadow: 0 0 5px rgba(30, 136, 229, 0.2); }
        50% { box-shadow: 0 0 20px rgba(30, 136, 229, 0.4); }
        100% { box-shadow: 0 0 5px rgba(30, 136, 229, 0.2); }
    }

    /* Persona Container Styling */
    .stButton>button {
        width: 100%;
        padding: 1rem;
        border-radius: 8px;
        background-color: white !important;
        color: #333 !important;
        border: 1px solid #ddd !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        text-align: left !important;
        height: auto !important;
        white-space: normal !important;
        position: relative;
        overflow: hidden;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        border-color: #1e88e5 !important;
        animation: glow 2s infinite;
    }

    .stButton>button:hover::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: shine 1.5s infinite;
    }

    @keyframes shine {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }

    /* Image Hover Effects */
    .stImage {
        margin: 0 !important;
        padding: 0 !important;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        overflow: hidden;
        border-radius: 8px;
        transition: all 0.3s ease;
    }

    .stImage:hover {
        transform: scale(1.02);
    }

    .stImage > img {
        border-radius: 8px;
        width: 100% !important;
        height: 100px !important;
        object-fit: cover;
        margin-bottom: 0 !important;
        transition: all 0.3s ease;
    }

    /* Specific persona animations */
    [data-testid="stImage"] img[src*="naruto"]:hover {
        animation: float 2s ease-in-out infinite;
    }

    [data-testid="stImage"] img[src*="modi"]:hover {
        animation: pulse 2s ease-in-out infinite;
    }

    [data-testid="stImage"] img[src*="hitesh"]:hover {
        animation: glow 2s infinite;
    }

    [data-testid="stImage"] img[src*="baburao"]:hover {
        animation: shake 0.5s ease-in-out infinite;
    }

    [data-testid="stImage"] img[src*="chaatu"]:hover {
        animation: bow 1s ease-in-out infinite;
    }

    [data-testid="stImage"] img[src*="bot"]:hover {
        animation: rotate 2s linear infinite;
    }

    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }

    @keyframes bow {
        0%, 100% { transform: rotateX(0deg); }
        50% { transform: rotateX(20deg); }
    }

    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    /* Persona selector container */
    .persona-selector {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }

    .persona-selector:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    /* Add shimmer effect to buttons */
    @keyframes shimmer {
        0% {
            background-position: -100% 0;
        }
        100% {
            background-position: 100% 0;
        }
    }

    .stButton>button::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255, 255, 255, 0.2),
            transparent
        );
        transform: translateX(-100%);
        animation: shimmer 3s infinite;
        pointer-events: none;
    }

    /* Guide Header Styling */
    .guide-header {
        text-align: center;
        padding: 1rem;
        margin-bottom: 2rem;
        position: relative;
    }
    
    .guide-header h3 {
        font-size: 1.8rem;
        font-weight: 600;
        color: transparent;
        background: linear-gradient(45deg, #2196F3, #4CAF50);
        background-clip: text;
        -webkit-background-clip: text;
        position: relative;
        margin: 0;
        padding: 0.5rem 0;
    }
    
    .guide-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 60px;
        height: 3px;
        background: linear-gradient(90deg, transparent, #2196F3, transparent);
    }
    
    .guide-header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 120px;
        height: 2px;
        background: linear-gradient(90deg, transparent, #4CAF50, transparent);
    }
    
    .guide-header .sparkle {
        position: absolute;
        width: 20px;
        height: 20px;
        animation: sparkle 1.5s infinite;
    }
    
    .guide-header .sparkle:nth-child(1) {
        top: 0;
        left: 20%;
        animation-delay: 0s;
    }
    
    .guide-header .sparkle:nth-child(2) {
        top: 20%;
        right: 20%;
        animation-delay: 0.3s;
    }
    
    .guide-header .sparkle:nth-child(3) {
        bottom: 0;
        left: 30%;
        animation-delay: 0.6s;
    }
    
    @keyframes sparkle {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.2); opacity: 1; }
    }
    
    /* Enhance persona selector container */
    .persona-selector {
        background-color: #f8f9fa;
        padding: 2rem 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        position: relative;
        overflow: hidden;
    }
    
    .persona-selector::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #2196F3, #4CAF50);
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'pdf_processed' not in st.session_state:
    st.session_state.pdf_processed = False
if 'current_file_name' not in st.session_state:
    st.session_state.current_file_name = None
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'analyzing' not in st.session_state:
    st.session_state.analyzing = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'chat_histories' not in st.session_state:
    st.session_state.chat_histories = {}  # Store chat histories per file and persona
if 'selected_persona' not in st.session_state:
    st.session_state.selected_persona = None
if 'selected_chat' not in st.session_state:
    st.session_state.selected_chat = None
if "input_key" not in st.session_state:
    st.session_state.input_key = 0

# Define available personas
PERSONAS = {
    "Hitesh Choudhary": {
        "image": "assets/hitesh.png",  # A professional photo of Hitesh
        "description": "A practical tech educator who explains system design with a focus on real-world applications",
        "greeting": "Haanji kaise hain aap"
    },
    "Narendra Modi": {
        "image": "assets/modiji.jpeg",  # An animated GIF of Modi speaking
        "description": "A visionary leader who communicates with inspiration and emphasis on progress",
        "greeting": "Mere pyare bhaiyo aur behno"
    },
    "Naruto Uzumaki": {
        "image": "assets/naruto.jpg",  # An animated GIF of Naruto
        "description": "An enthusiastic ninja who never gives up and encourages others to believe in themselves",
        "greeting": "Believe it! (Dattebayo!)"
    },
    "Baburao": {
        "image": "assets/baburao.jpg",  # A funny GIF of Baburao
        "description": "A grumpy but lovable character who gives advice with a touch of frustration",
        "greeting": "Ae Raju!"
    },
    "Employee": {
        "image": "assets/chaatu.png",  # An animated GIF of someone bowing repeatedly
        "description": "An overly flattering employee who explains everything with excessive praise",
        "greeting": "Sir/Ma'am, aapne bulaya aur main chala aaya!"
    },
    "Bot": {
        "image": "assets/bot.webp",  # An animated robot or AI visualization
        "description": "A focused and precise AI that explains content with accuracy and clarity",
        "greeting": "Hello! I'm ready to help you understand the content."
    }
}

def display_persona_selector():
    st.markdown("""
        <div class="guide-header">
            <div class="sparkle">✨</div>
            <div class="sparkle">✨</div>
            <div class="sparkle">✨</div>
            <h3>Choose your Guide</h3>
        </div>
    """, unsafe_allow_html=True)
    
    for name, details in PERSONAS.items():
        col1, col2 = st.columns([1, 3])  # Adjusted ratio for better layout
        with col1:
            st.image(details["image"], use_container_width=True, output_format="auto")
        with col2:
            if st.button(
                f"**{name}**\n\n{details['description']}",  # Added markdown formatting
                key=f"persona_{name}",
                help=f"Select {name} as your guide"
            ):
                # Store current chat history if exists
                if st.session_state.selected_persona and st.session_state.current_file_name:
                    history_key = f"{st.session_state.current_file_name}_{st.session_state.selected_persona}"
                    st.session_state.chat_histories[history_key] = st.session_state.chat_history

                # Load existing chat history for new persona if exists
                history_key = f"{st.session_state.current_file_name}_{name}"
                st.session_state.chat_history = st.session_state.chat_histories.get(history_key, [])
                
                # Set new persona
                st.session_state.selected_persona = name
                st.session_state.selected_chat = None  # Reset selected chat
                st.session_state.input_key = 0  # Reset input key
                st.session_state.analyzing = False  # Reset analyzing state
                
                # Add greeting message only if no chat history exists
                if not st.session_state.chat_history:
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": details['greeting']
                    })
                return True
    return False

# Sidebar for chat history
with st.sidebar:
    st.markdown("<h2 class='chat-history-title'>💬 Chat History</h2>", unsafe_allow_html=True)
    
    if len(st.session_state.chat_history) > 0:
        st.markdown("<div class='chat-history'>", unsafe_allow_html=True)
        conversations = []
        current_conversation = []
        
        for idx, message in enumerate(st.session_state.chat_history):
            current_conversation.append(message)
            if message["role"] == "assistant":
                if len(current_conversation) > 0:
                    conversations.append((len(conversations), current_conversation[:]))
                current_conversation = []
        
        if len(current_conversation) > 0:
            conversations.append((len(conversations), current_conversation))
        
        for conv_idx, conversation in conversations:
            user_message = next((msg["content"] for msg in conversation if msg["role"] == "user"), "")
            if user_message:
                is_selected = st.session_state.selected_chat == conv_idx
                selected_class = "selected" if is_selected else ""
                if st.button(
                    f"🗣️ {user_message[:50]}...",
                    key=f"history_{conv_idx}",
                    help="Click to view this conversation"
                ):
                    st.session_state.selected_chat = conv_idx
                    st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("No chat history yet. Start a conversation!")

# Main content area
main_col1, main_col2 = st.columns([2, 1])

with main_col1:
    # Header section with gradient text
    st.markdown("""
        <h1 style='text-align: center; background: linear-gradient(45deg, #1e88e5, #4CAF50);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
        🤖 Chat with your PDF</h1>
        """, unsafe_allow_html=True)

    st.markdown("""
        <p style='text-align: center; font-size: 1.2em; color: #666;'>
        Transform your PDF into an interactive knowledge base
        </p>
        """, unsafe_allow_html=True)

    # Upload section
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded_file:
        # Check file size (10MB limit)
        if uploaded_file.size > 10 * 1024 * 1024:  # 10MB in bytes
            st.error("❌ File size exceeds 10MB limit. Please upload a smaller file.")
        else:
            # Create columns for file info
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Selected File:** {uploaded_file.name}")
            with col2:
                st.markdown(f"**Size:** {uploaded_file.size/1000000:.2f} MB")
            
            # Reset processed state if new file is uploaded
            if st.session_state.current_file_name != uploaded_file.name:
                st.session_state.pdf_processed = False
                st.session_state.current_file_name = uploaded_file.name
                # Load existing chat history for current file and persona if exists
                if st.session_state.selected_persona:
                    history_key = f"{uploaded_file.name}_{st.session_state.selected_persona}"
                    st.session_state.chat_history = st.session_state.chat_histories.get(history_key, [])
                else:
                    st.session_state.chat_history = []
            
            # Save to temporary location
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.read())
                temp_pdf_path = tmp_file.name

            process_button = st.button("🚀 Process PDF", disabled=st.session_state.pdf_processed)
            
            if process_button:
                st.session_state.processing = True

            if st.session_state.processing and not st.session_state.pdf_processed:
                with st.spinner(""):
                    st.markdown("""
                        <div style='text-align: center; padding: 2rem;'>
                            <div class='ninja'>🥷</div>
                            <div class='processing-text'>Ninja processing your document...</div>
                        </div>
                        """, unsafe_allow_html=True)
                    try:
                        ingest_pdf(temp_pdf_path)
                        st.session_state.pdf_processed = True
                        st.session_state.processing = False
                        st.success("✨ PDF processed successfully! Ready for your questions!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error processing PDF: {str(e)}")
                        st.session_state.processing = False

            if st.session_state.pdf_processed:
                # Chat Interface
                if st.session_state.selected_persona:
                    persona_name = st.session_state.selected_persona
                    st.markdown(f"""
                        <div style='margin-top: 2rem;'>
                        <h3 style='text-align: center; color: #1e88e5;'>
                        {persona_name}: {PERSONAS[persona_name]['greeting']} 💭
                        </h3>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                        <div style='margin-top: 2rem;'>
                        <h3 style='text-align: center; color: #1e88e5;'>
                        💭 Please select a persona to start chatting
                        </h3>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Display chat history
                if st.session_state.selected_chat is not None:
                    conversations = []
                    current_conversation = []
                    
                    for message in st.session_state.chat_history:
                        current_conversation.append(message)
                        if message["role"] == "assistant":
                            if len(current_conversation) > 0:
                                conversations.append(current_conversation[:])
                            current_conversation = []
                    
                    if len(current_conversation) > 0:
                        conversations.append(current_conversation)
                    
                    if 0 <= st.session_state.selected_chat < len(conversations):
                        selected_conversation = conversations[st.session_state.selected_chat]
                        for message in selected_conversation:
                            message_class = "user-message" if message["role"] == "user" else "assistant-message"
                            if message["role"] == "assistant":
                                prefix = f"{st.session_state.selected_persona}: " if st.session_state.selected_persona else ""
                            else:
                                prefix = "You: "
                            st.markdown(f"""
                                <div class='chat-message {message_class}'>
                                <strong>{prefix}</strong>{message["content"]}
                                </div>
                                """, unsafe_allow_html=True)
                else:
                    # Display full chat history if no conversation is selected
                    for message in st.session_state.chat_history:
                        message_class = "user-message" if message["role"] == "user" else "assistant-message"
                        if message["role"] == "assistant":
                            prefix = f"{st.session_state.selected_persona}: " if st.session_state.selected_persona else ""
                        else:
                            prefix = "You: "
                        st.markdown(f"""
                            <div class='chat-message {message_class}'>
                            <strong>{prefix}</strong>{message["content"]}
                            </div>
                            """, unsafe_allow_html=True)
                
                # Chat input - only enabled if persona is selected
                if st.session_state.selected_persona:
                    user_query = st.text_input(
                        "Enter your question",
                        placeholder="Type your question here...",
                        key=f"query_{st.session_state.input_key}"
                    )
                    # Send button - only enabled if there's text in the input
                    send_button = st.button("Send", key="send_message", disabled=not user_query)
                else:
                    # Disabled input with message
                    st.text_input(
                        "Enter your question",
                        placeholder="Please select a persona first...",
                        disabled=True,
                        key=f"query_disabled_{st.session_state.input_key}"
                    )
                    st.button("Send", disabled=True, key="send_message_disabled")
                
                # Only process the query when send button is clicked and we have a query
                if st.session_state.selected_persona and 'user_query' in locals() and user_query and send_button:
                    # Add user message to chat history
                    st.session_state.chat_history.append({
                        "role": "user",
                        "content": user_query
                    })
                    
                    st.session_state.analyzing = True
                    analyzing_placeholder = st.empty()
                    
                    if st.session_state.analyzing:
                        analyzing_placeholder.markdown(f"""
                            <div style='text-align: center; padding: 1rem;'>
                                <div style='font-size: 3rem; animation: ninja-flip 2s linear infinite'>
                                {'🥷'}
                                </div>
                                <p style='color: #666; margin-top: 0.5rem;'>Analyzing your question...</p>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    vector_db = get_vector_db()
                    answer = get_answer_from_query(user_query, vector_db, st.session_state.selected_persona)
                    
                    # Add assistant response to chat history
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": answer
                    })
                    
                    analyzing_placeholder.empty()
                    st.session_state.analyzing = False
                    
                    # Increment the input key to create a new input field
                    st.session_state.input_key += 1
                    st.rerun()

with main_col2:
    if st.session_state.pdf_processed:
        st.markdown("<div class='persona-selector'>", unsafe_allow_html=True)
        if display_persona_selector():
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
