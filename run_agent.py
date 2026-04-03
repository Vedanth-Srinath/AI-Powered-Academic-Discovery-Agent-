from rabbit_agent import agent
from config.settings import LOGS_DIR
import datetime
import os

# Ensure logs directory exists
LOGS_DIR.mkdir(exist_ok=True)

# Create log file for session
log_file = LOGS_DIR / f"chat_session_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

def log_interaction(user_input, bot_response):
    """Log user interactions"""
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"[{datetime.datetime.now()}] USER: {user_input}\n")
        f.write(f"[{datetime.datetime.now()}] BOT: {bot_response}\n\n")

print("🔬  Research-Rabbit ready! (type 'quit' to exit)")
print(f"📝  Session logged to: {log_file}")
print()

while True:
    q = input("🧑‍🔬  Your question: ")
    if q.lower().startswith("quit"):
        break

    try:
        result = agent.invoke(
            {"messages": [("user", q)]}
        )
        response = result["messages"][-1].content
        print(f"\n🤖 {response}\n")
        
        # Log the interaction
        log_interaction(q, response)
        
    except Exception as e:
        error_msg = f"❌ Error: {e}"
        print(f"\n{error_msg}\n")
        log_interaction(q, error_msg)

