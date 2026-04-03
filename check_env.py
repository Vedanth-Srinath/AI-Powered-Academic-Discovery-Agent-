# check_env.py
import os
from dotenv import load_dotenv
from pathlib import Path

print("--- Starting Environment Variable Check ---")

# Define the explicit path to the .env file in the current directory
env_path = Path('.') / '.env'
print(f"Looking for .env file at this location: {env_path.resolve()}")

# Check if the .env file actually exists
if not env_path.exists():
    print("\n❌ CRITICAL ERROR: The .env file was NOT FOUND in your project directory.")
    print("   Please ensure you have created a file named exactly '.env' (with the leading dot).")
    exit()

print(".env file was found.")

# Load the .env file
load_dotenv(dotenv_path=env_path)
print("Attempted to load variables from .env file.")

# Check for the API key in the environment
api_key = os.getenv("GROQ_API_KEY")

print("\n--- Final Diagnosis ---")
if api_key:
    print("✅ SUCCESS: The GROQ_API_KEY was found!")
    # For security, only print a portion of the key
    print(f"   The key begins with: {api_key[:7]}...")
else:
    print("❌ FAILURE: The GROQ_API_KEY was NOT found after loading the .env file.")
    print("\n   Next Steps:")
    print("   1. Check the .env file's contents.")
    print("   2. Is the variable name EXACTLY 'GROQ_API_KEY' (all uppercase)?")
    print("   3. Is there an equals sign (=) with no spaces around it?")
    print("   4. Are there any hidden characters or quotes in the file?")
