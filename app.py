import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from textblob import TextBlob
from datetime import datetime, timedelta
import json
import requests
import random
from streamlit_option_menu import option_menu
import time
import os

# Page config must be first Streamlit command
st.set_page_config(
    page_title="MindTrack AI - Your Wellness Companion",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- OpenRouter API Setup ----------
# Define constants
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Try to get API key from multiple sources
api_key = None

# Method 1: Streamlit secrets (for deployment)
try:
    api_key = st.secrets.get("OPENROUTER_API_KEY")
except:
    pass

# Method 2: Environment variable (for local development)
if not api_key:
    api_key = os.getenv("OPENROUTER_API_KEY")

# Method 3: Hardcoded for testing (remove in production)
# Only use if others fail - NEVER commit this to GitHub!
if not api_key:
    # api_key = "your-key-here"  # Uncomment for testing only
    pass

if api_key:
    ai_available = True
else:
    ai_available = False
    st.warning("⚠️ OpenRouter API key not found. AI features will be limited. Please add your API key to .streamlit/secrets.toml")

# ---------- Session State ----------
if 'mood_history' not in st.session_state:
    st.session_state.mood_history = []
if 'journals' not in st.session_state:
    st.session_state.journals = []
if 'habits' not in st.session_state:
    st.session_state.habits = {
        'Meditation': {'streak': 0, 'completed': False, 'last_completed': None, 'icon': '🧘'},
        'Exercise': {'streak': 0, 'completed': False, 'last_completed': None, 'icon': '🏃'},
        'Journaling': {'streak': 0, 'completed': False, 'last_completed': None, 'icon': '📝'},
        'Sleep 8h': {'streak': 0, 'completed': False, 'last_completed': None, 'icon': '😴'},
        'Drink Water': {'streak': 0, 'completed': False, 'last_completed': None, 'icon': '💧'}
    }
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = "dashboard"
if 'notifications' not in st.session_state:
    st.session_state.notifications = []
if 'achievements' not in st.session_state:
    st.session_state.achievements = {
        'first_journal': False,
        'habit_master': False,
        'streak_7': False,
        'mood_tracker': False
    }

# ---------- Helper Functions ----------
def add_notification(message, type="info"):
    st.session_state.notifications.append({
        'message': message,
        'type': type,
        'time': datetime.now()
    })

def check_achievements():
    if len(st.session_state.journals) >= 1 and not st.session_state.achievements['first_journal']:
        st.session_state.achievements['first_journal'] = True
        add_notification("🏆 Achievement Unlocked: First Journal Entry!", "success")
    
    if sum(1 for h in st.session_state.habits.values() if h['streak'] >= 7) >= 3 and not st.session_state.achievements['habit_master']:
        st.session_state.achievements['habit_master'] = True
        add_notification("🏆 Achievement Unlocked: Habit Master!", "success")
    
    if len(st.session_state.mood_history) >= 7 and not st.session_state.achievements['mood_tracker']:
        st.session_state.achievements['mood_tracker'] = True
        add_notification("🏆 Achievement Unlocked: Mood Tracker!", "success")

# ---------- AI Functions ----------
def call_openrouter(messages, model="openai/gpt-3.5-turbo", max_tokens=200):
    if not ai_available or not api_key:
        return None
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://mindtrack-ai.streamlit.app",
        "X-Title": "MindTrack AI"
    }
    
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        print(f"API Error: {e}")
        return None

def chat_with_ai(user_message):
    if not ai_available:
        return generate_motivational_quote()
    
    try:
        recent_messages = st.session_state.messages[-6:] if st.session_state.messages else []
        messages = [
            {"role": "system", "content": """You are MindTrack AI, a warm, empathetic wellness companion. 
            Keep responses concise (2-3 sentences), supportive, and actionable. Use occasional emojis.
            Focus on mindfulness, gratitude, and small positive steps."""}
        ]
        
        for msg in recent_messages:
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        messages.append({"role": "user", "content": user_message})
        response = call_openrouter(messages, max_tokens=150)
        
        if response:
            return response
        else:
            return generate_motivational_quote()
    except Exception:
        return generate_motivational_quote()

def generate_motivational_quote():
    quotes = [
        "✨ You're stronger than you think! Keep going!",
        "🌱 Small steps every day lead to big changes.",
        "💪 Every day is a new opportunity to grow.",
        "🌟 Your future self will thank you for starting today.",
        "🌸 Progress, not perfection. You're doing great!",
        "🧠 Your mind is powerful. Nurture it with kindness."
    ]
    return random.choice(quotes)

# ---------- Custom CSS for Modern UI ----------
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main background with animated gradient */
    .stApp {
        background: linear-gradient(-45deg, #0f172a, #1e1b4b, #0f172a, #1e1b4b);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Glass morphism card effect */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(255, 255, 255, 0.2);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }
    
    /* Hero section */
    .hero-section {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.2), rgba(16, 163, 127, 0.2));
        border-radius: 30px;
        padding: 40px;
        margin-bottom: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        animation: fadeInUp 0.8s ease;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.03));
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .metric-card:hover {
        transform: scale(1.05);
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.2), rgba(16, 163, 127, 0.2));
    }
    
    .metric-value {
        font-size: 2.5em;
        font-weight: bold;
        background: linear-gradient(135deg, #8b5cf6, #10a37f);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Custom button styling */
    .stButton > button {
        background: linear-gradient(135deg, #8b5cf6, #10a37f);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(139, 92, 246, 0.4);
    }
    
    /* Chat message styling */
    .chat-message-user {
        background: linear-gradient(135deg, #8b5cf6, #10a37f);
        border-radius: 20px;
        padding: 12px 20px;
        margin: 10px 0;
        max-width: 80%;
        margin-left: auto;
        animation: slideInRight 0.3s ease;
    }
    
    .chat-message-assistant {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 12px 20px;
        margin: 10px 0;
        max-width: 80%;
        animation: slideInLeft 0.3s ease;
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Custom tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        padding: 8px 24px;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #8b5cf6, #10a37f);
        color: white;
    }
    
    /* Progress bar styling */
    .stProgress > div > div {
        background: linear-gradient(135deg, #8b5cf6, #10a37f);
    }
    
    /* Input field styling */
    .stTextArea textarea, .stTextInput input {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        color: white;
        transition: all 0.3s ease;
    }
    
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #8b5cf6;
        box-shadow: 0 0 10px rgba(139, 92, 246, 0.3);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.95);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# ---------- Hero Section ----------
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class="hero-section">
        <h1 style="font-size: 3.5em; margin-bottom: 0;">
            🧠 MindTrack AI
        </h1>
        <p style="font-size: 1.2em; color: #8b5cf6; margin-top: 10px;">
            Your Intelligent Wellness Companion
        </p>
        <p style="font-size: 1em; opacity: 0.8;">
            Track mood • Journal thoughts • Build habits • Transform life
        </p>
        <div style="margin-top: 20px;">
            <span style="background: rgba(139, 92, 246, 0.3); padding: 5px 15px; border-radius: 20px; font-size: 0.9em;">
                ✨ AI-Powered
            </span>
            <span style="background: rgba(16, 163, 127, 0.3); padding: 5px 15px; border-radius: 20px; font-size: 0.9em; margin-left: 10px;">
                🌟 Personalized
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="text-align: center; padding: 20px;" class="floating">
        <h1 style="font-size: 5em; margin: 0;">🌟</h1>
        <p style="margin-top: 10px; opacity: 0.8;">Your journey to wellness starts here</p>
    </div>
    """, unsafe_allow_html=True)

# ---------- Metrics Row with Enhanced UI ----------
col1, col2, col3, col4 = st.columns(4)

# Calculate metrics
if st.session_state.mood_history:
    avg_mood = int(sum([m['score'] for m in st.session_state.mood_history[-7:]]) / len(st.session_state.mood_history[-7:]))
else:
    avg_mood = 75

# Calculate streak
streak = 0
if st.session_state.journals:
    dates = sorted(set([j['date'].date() for j in st.session_state.journals]), reverse=True)
    if dates:
        streak = 1
        for i in range(1, len(dates)):
            if (dates[i-1] - dates[i]).days == 1:
                streak += 1
            else:
                break

completed_habits = sum(1 for h in st.session_state.habits.values() if h['completed'])

metrics_data = [
    {"icon": "😊", "label": "Mood Score", "value": f"{avg_mood}%", "change": "+8%"},
    {"icon": "🔥", "label": "Current Streak", "value": f"{streak} days", "change": "Keep going!"},
    {"icon": "📝", "label": "Total Journals", "value": str(len(st.session_state.journals)), "change": "✨"},
    {"icon": "✅", "label": "Habits Today", "value": f"{completed_habits}/5", "change": f"{completed_habits*20}%"}
]

for col, metric in zip([col1, col2, col3, col4], metrics_data):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 2.5em;">{metric['icon']}</div>
            <div style="font-size: 0.85em; opacity: 0.7; margin-top: 10px;">{metric['label']}</div>
            <div class="metric-value">{metric['value']}</div>
            <div style="font-size: 0.8em; color: #10a37f;">{metric['change']}</div>
        </div>
        """, unsafe_allow_html=True)

# ---------- Main Navigation with Icons ----------
st.markdown("---")

# Create custom tabs with icons
tab_dashboard, tab_journal, tab_habits, tab_chat, tab_insights = st.tabs([
    "📊 Dashboard", "📝 AI Journal", "🎯 Habits", "🤖 AI Chat", "📈 Insights"
])

# Check for achievements
check_achievements()

# ---------- DASHBOARD TAB ----------
with tab_dashboard:
    st.markdown("### 🌟 Welcome to Your Wellness Dashboard")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Quick mood check
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 😊 Quick Mood Check")
        
        mood_options = {
            "😔 Very Low": 25,
            "😐 Okay": 50, 
            "🙂 Good": 75,
            "😊 Great": 90,
            "🤩 Excellent": 100
        }
        
        mood_emoji = st.select_slider(
            "How are you feeling right now?",
            options=list(mood_options.keys()),
            value="🙂 Good",
            key="mood_slider"
        )
        
        mood_score = mood_options[mood_emoji]
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("✅ Log Mood", key="log_mood", use_container_width=True):
                st.session_state.mood_history.append({
                    'date': datetime.now(),
                    'score': mood_score,
                    'emoji': mood_emoji
                })
                add_notification(f"Mood logged: {mood_emoji}!", "success")
                st.success(f"✨ Mood logged: {mood_emoji}!")
                st.balloons()
                time.sleep(1)
                st.rerun()
        
        with col_b:
            if st.button("📊 View Trends", key="view_trends", use_container_width=True):
                st.info(f"You've logged {len(st.session_state.mood_history)} moods so far!")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Motivational quote of the day
        st.markdown('<div class="glass-card" style="margin-top: 20px;">', unsafe_allow_html=True)
        st.markdown("#### 💫 Quote of the Day")
        quotes = [
            "The journey of a thousand miles begins with a single step.",
            "You are capable of amazing things.",
            "Every day is a new beginning.",
            "Progress, not perfection.",
            "Small steps every day lead to big changes."
        ]
        st.info(f"✨ {random.choice(quotes)}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Mood trend chart
        if st.session_state.mood_history:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 📈 Your Mood Journey")
            
            mood_df = pd.DataFrame(st.session_state.mood_history[-14:])
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=mood_df['date'],
                y=mood_df['score'],
                mode='lines+markers',
                name='Mood Score',
                line=dict(color='#8b5cf6', width=3),
                marker=dict(size=8, color='#10a37f')
            ))
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis_title="Date",
                yaxis_title="Mood Score",
                xaxis=dict(showgrid=False, tickangle=45),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.info("📊 Log your first mood to see trends and insights!")
            st.markdown('</div>', unsafe_allow_html=True)

# ---------- JOURNAL TAB ----------
with tab_journal:
    st.markdown("### 📝 AI-Powered Journaling")
    st.markdown("*Write freely, and let AI help you gain deeper insights*")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        journal_entry = st.text_area(
            "How are you feeling today? What's on your mind?",
            height=250,
            placeholder="Dear journal, today I feel...\n\nI've been thinking about...\n\nSomething that made me smile was...\n\nA challenge I faced today...",
            key="journal_entry"
        )
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("💾 Save Journal", type="primary", key="save_journal", use_container_width=True):
                if journal_entry:
                    blob = TextBlob(journal_entry)
                    sentiment = blob.sentiment.polarity
                    
                    st.session_state.journals.append({
                        'date': datetime.now(),
                        'entry': journal_entry,
                        'sentiment': sentiment
                    })
                    add_notification("Journal saved! 🎉", "success")
                    st.success("✨ Journal saved! Your consistency is building!")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()
                else:
                    st.warning("📝 Please write something before saving!")
        
        with col_btn2:
            if st.button("🤖 Analyze with AI", key="analyze_journal", use_container_width=True):
                if journal_entry:
                    if ai_available:
                        with st.spinner("🧠 AI is analyzing your journal..."):
                            # Simple analysis for now
                            blob = TextBlob(journal_entry)
                            sentiment = blob.sentiment.polarity
                            mood_score = int((sentiment + 1) * 50)
                            
                            st.markdown(f"""
                            <div style="background: linear-gradient(135deg, rgba(139,92,246,0.2), rgba(16,163,127,0.2)); 
                                        border-radius: 15px; padding: 20px; margin-top: 20px;">
                                <h4>🤖 AI Analysis</h4>
                                <p>🎯 <b>Mood Score:</b> {mood_score}%</p>
                                <p>💭 <b>Sentiment:</b> {'Positive' if sentiment > 0 else 'Neutral' if sentiment == 0 else 'Negative'}</p>
                                <p>💡 <b>Insight:</b> {generate_motivational_quote()}</p>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("✨ Your journal is saved! Continue writing to see AI insights.")
                else:
                    st.warning("📝 Write something to analyze!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 📚 Recent Journal Entries")
        
        if st.session_state.journals:
            for journal in reversed(st.session_state.journals[-5:]):
                with st.expander(f"📔 {journal['date'].strftime('%b %d, %Y - %H:%M')}"):
                    st.write(journal['entry'][:200] + ("..." if len(journal['entry']) > 200 else ""))
                    sentiment_color = "🟢 Positive" if journal['sentiment'] > 0.1 else "🔴 Negative" if journal['sentiment'] < -0.1 else "🟡 Neutral"
                    st.caption(f"Sentiment: {sentiment_color} | Score: {journal['sentiment']:.2f}")
        else:
            st.info("✨ Your journal entries will appear here")
            st.markdown("""
            <div style="text-align: center; padding: 20px;">
                <p style="font-size: 3em;">📝</p>
                <p>Start your first journal entry!</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Journal stats
        if st.session_state.journals:
            st.markdown("---")
            st.markdown("#### 📊 Journal Stats")
            st.metric("Total Entries", len(st.session_state.journals))
            avg_sentiment = sum([j['sentiment'] for j in st.session_state.journals]) / len(st.session_state.journals)
            st.metric("Average Sentiment", f"{avg_sentiment:.2f}")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ---------- HABITS TAB ----------
with tab_habits:
    st.markdown("### 🎯 Daily Habit Tracker")
    st.markdown("*Small actions, big transformations*")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### ✅ Today's Habits")
        
        for habit, data in st.session_state.habits.items():
            col_a, col_b, col_c = st.columns([3, 1, 1])
            with col_a:
                completed = st.checkbox(f"{data['icon']} {habit}", value=data['completed'], key=f"habit_{habit}")
            with col_b:
                streak_display = f"🔥 {data['streak']}"
                st.write(streak_display)
            with col_c:
                if data['streak'] >= 7:
                    st.write("🏆")
                elif data['streak'] >= 3:
                    st.write("⭐")
            
            if completed and not data['completed']:
                data['completed'] = True
                data['streak'] += 1
                data['last_completed'] = datetime.now()
                add_notification(f"🎉 Great job completing {habit}!", "success")
                st.success(f"🎉 Amazing! +1 day streak for {habit}!")
                st.balloons()
            elif not completed and data['completed']:
                data['completed'] = False
        
        st.markdown("---")
        
        if st.button("🔄 Reset for New Day", key="reset_habits", use_container_width=True):
            for habit in st.session_state.habits:
                st.session_state.habits[habit]['completed'] = False
            add_notification("Habits reset for a new day! 🌅", "info")
            st.success("✨ Ready for a new day!")
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 📊 Habit Statistics")
        
        total_streak = sum([h['streak'] for h in st.session_state.habits.values()])
        
        # Progress ring
        completion_rate = (completed_habits / 5) * 100
        st.markdown(f"""
        <div style="text-align: center; padding: 20px;">
            <div style="position: relative; display: inline-block;">
                <svg width="150" height="150">
                    <circle cx="75" cy="75" r="60" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="10"/>
                    <circle cx="75" cy="75" r="60" fill="none" stroke="#8b5cf6" stroke-width="10"
                            stroke-dasharray="{2 * 3.14159 * 60}" stroke-dashoffset="{2 * 3.14159 * 60 * (1 - completion_rate/100)}"
                            transform="rotate(-90 75 75)"/>
                </svg>
                <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center;">
                    <div style="font-size: 2em;">{completed_habits}</div>
                    <div style="font-size: 0.8em;">/5</div>
                </div>
            </div>
            <p style="margin-top: 10px;">Today's Progress</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.metric("Total Habit Streak", f"{total_streak} days", "Keep building!")
        
        best_habit = max(st.session_state.habits.items(), key=lambda x: x[1]['streak'])
        st.success(f"🌟 Your strongest habit: **{best_habit[1]['icon']} {best_habit[0]}** (🔥 {best_habit[1]['streak']} days)")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # AI Habit Coach
        st.markdown('<div class="glass-card" style="margin-top: 20px;">', unsafe_allow_html=True)
        st.markdown("#### 🤖 AI Habit Coach")
        
        if st.button("Get Personalized Advice", key="habit_advice", use_container_width=True):
            with st.spinner("Generating personalized tips..."):
                completed_list = [h for h, d in st.session_state.habits.items() if d['completed']]
                advice = f"Based on your progress with {', '.join(completed_list) if completed_list else 'your habits'}, keep up the great work! Try adding a 2-minute meditation to your routine."
                st.info(f"💡 {advice}")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ---------- AI CHAT TAB ----------
with tab_chat:
    st.markdown("### 🤖 Chat with MindTrack AI")
    st.markdown("*Your compassionate AI wellness companion, always here to listen*")
    
    # Display chat history
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message-user">
                <strong>You</strong><br>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message-assistant">
                <strong>🧠 MindTrack AI</strong><br>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
    
    # Chat input
    if prompt := st.chat_input("How are you feeling? Share anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("🧠 MindTrack AI is thinking..."):
                response = chat_with_ai(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
        
        st.rerun()
    
    if st.session_state.messages and st.button("🗑️ Clear Chat History", key="clear_chat"):
        st.session_state.messages = []
        add_notification("Chat history cleared", "info")
        st.rerun()

# ---------- INSIGHTS TAB ----------
with tab_insights:
    st.markdown("### 📈 Deep Insights & Analytics")
    st.markdown("*Understand your patterns and track your growth*")
    
    if st.button("🔄 Generate Weekly Report", type="primary", key="weekly_report", use_container_width=True):
        with st.spinner("Analyzing your data..."):
            if st.session_state.journals or st.session_state.mood_history:
                # Stats cards
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Journals", len(st.session_state.journals))
                with col2:
                    if st.session_state.journals:
                        avg_sentiment = sum([j['sentiment'] for j in st.session_state.journals]) / len(st.session_state.journals)
                        st.metric("Avg Sentiment", f"{avg_sentiment:.2f}")
                    else:
                        st.metric("Avg Sentiment", "N/A")
                with col3:
                    total_streak = sum([h['streak'] for h in st.session_state.habits.values()])
                    st.metric("Total Habit Streak", total_streak)
                with col4:
                    st.metric("Mood Logs", len(st.session_state.mood_history))
                
                # Mood trend over time
                if st.session_state.mood_history:
                    st.markdown("#### 📊 Mood Progression")
                    mood_df = pd.DataFrame(st.session_state.mood_history)
                    fig = px.line(mood_df, x='date', y='score', title="Your Mood Journey",
                                color_discrete_sequence=['#8b5cf6'])
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        xaxis_title="Date",
                        yaxis_title="Mood Score"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # AI Insights
                st.markdown("#### 🤖 AI-Powered Insights")
                insights = [
                    "📝 You've been consistent with journaling - keep it up!",
                    "🎯 Your habit streaks are building momentum",
                    "💪 Small daily actions lead to big changes"
                ]
                for insight in insights:
                    st.info(insight)
                
            else:
                st.warning("📊 Not enough data yet. Keep journaling and logging your mood to see insights!")
    
    # Achievements section
    st.markdown("#### 🏆 Achievements Gallery")
    col1, col2, col3 = st.columns(3)
    
    achievements_list = [
        {"name": "First Journal", "icon": "📝", "unlocked": st.session_state.achievements['first_journal']},
        {"name": "Habit Master", "icon": "🏆", "unlocked": st.session_state.achievements['habit_master']},
        {"name": "Mood Tracker", "icon": "😊", "unlocked": st.session_state.achievements['mood_tracker']}
    ]
    
    for col, achievement in zip([col1, col2, col3], achievements_list):
        with col:
            if achievement['unlocked']:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(139,92,246,0.2), rgba(16,163,127,0.2));
                            border-radius: 15px; padding: 15px; text-align: center;">
                    <div style="font-size: 3em;">{achievement['icon']}</div>
                    <div><b>{achievement['name']}</b></div>
                    <div style="font-size: 0.8em; color: #10a37f;">✓ Unlocked</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.05); border-radius: 15px; padding: 15px; text-align: center; opacity: 0.5;">
                    <div style="font-size: 3em;">{achievement['icon']}</div>
                    <div><b>{achievement['name']}</b></div>
                    <div style="font-size: 0.8em;">🔒 Locked</div>
                </div>
                """, unsafe_allow_html=True)

# ---------- Notifications Display ----------
if st.session_state.notifications:
    latest_notification = st.session_state.notifications[-1]
    if latest_notification['type'] == "success":
        st.success(latest_notification['message'])
    elif latest_notification['type'] == "info":
        st.info(latest_notification['message'])

# ---------- Sidebar with Enhanced UI ----------
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h1 style="font-size: 2.5em;">🧠</h1>
        <h3>MindTrack AI</h3>
        <p style="opacity: 0.7;">Version 2.0</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # User stats in sidebar
    st.markdown("### 📊 Your Stats")
    
    total_activities = len(st.session_state.journals) + len(st.session_state.mood_history)
    st.metric("Total Activities", total_activities)
    
    if st.session_state.mood_history:
        best_mood = max(st.session_state.mood_history, key=lambda x: x['score'])
        st.success(f"Best Mood: {best_mood['emoji']} ({best_mood['score']}%)")
    
    st.markdown("---")
    
    # Quick tips
    st.markdown("### 💡 Wellness Tips")
    tips = [
        "Take 3 deep breaths",
        "Practice gratitude",
        "Stay hydrated",
        "Move your body",
        "Connect with others"
    ]
    for tip in random.sample(tips, 3):
        st.info(f"✨ {tip}")
    
    st.markdown("---")
    
    # Progress
    st.markdown("### 🎯 Your Progress")
    total_habits_streak = sum([h['streak'] for h in st.session_state.habits.values()])
    st.progress(min(total_habits_streak / 50, 1.0))
    st.caption(f"Total habit streak: {total_habits_streak} days")
    
    st.markdown("---")
    
    if st.button("🗑️ Reset All Data", key="reset_all", use_container_width=True):
        st.session_state.clear()
        add_notification("All data has been reset", "info")
        st.rerun()

# ---------- Footer ----------
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px;">
    <p>🧠 MindTrack AI © 2024 | Your wellness journey starts here 🌟</p>
    <p style="font-size: 0.8em; opacity: 0.6;">Powered by OpenRouter AI | Making mental wellness accessible to all</p>
</div>
""", unsafe_allow_html=True)