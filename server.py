import requests
import json
import os # Added to help check file paths

# ================================================================
# ⚙️ CONFIGURATION SECTION: UPDATE THESE VALUES IF NECESSARY
# ================================================================


# !!! CHECK THIS URL from your LM Studio API Server GUI !!!
API_URL = "http://localhost:1234/v1/chat/completions"

# Set MODEL_NAME if you know it, otherwise leave blank to let the server decide.
MODEL_NAME = "" 


# ================================================================
# ⭐ STYLISTIC DIRECTIVE: CONTROLS THE AI'S WRITING STYLE
# ================================================================


def get_style_instructions(genre):
    """Returns specialized creative instructions based on user choice."""
    genre = genre.lower()
    if "sci-fi" in genre:
        return """
            You are a hard science fiction novelist. Write a story focused on plausible physics and technological limitations. 
            The tone must be awe-inspiring and slightly ominous. Use technical jargon related to space travel or AI logic.
            """
    elif "romance" in genre:
        return """
            You are a classic romantic poet. The narrative should be intensely emotional, focusing on subtext, shared glances, and fate. 
            Use flowery, elevated language. Avoid modern slang entirely.
            """
    elif "mystery" in genre:
        return """
            You are a hard-boiled detective novelist. Write a noir mystery setup. The tone must be cynical, rainy, and suspenseful. 
            Focus on unreliable narrators and smoky bar dialogue.
            """
    else: # Default/General Creative Mode (The original high creativity mode)
        return """
            You are an award-winning, highly imaginative, and wildly creative short story writer. 
            Your task is to write a completely original fantasy story based on the premise. 
            Rules MUST be followed: Tone must be whimsical yet slightly melancholic. Incorporate at least three unique, invented items (e.g., 'whisper-moss,' 'sky-glass'). The climax must involve an unexpected character reveal. Focus heavily on sensory details.
        """


# ================================================================
# 🤖 CORE FUNCTION: TALKING TO THE AI MODEL VIA API
# ================================================================


def generate_story(prompt, style_directive):
    """Sends the combined prompt to the local LM Studio API and gets a response."""
    print("\n" + "="*50)
    print("🤖 Sending request to the AI Model... PLEASE WAIT.")
    print("="*50)

    # Combine the user's style rules and their premise into one final instruction set for the AI.
    full_instruction = f"[STYLE GUIDE]: {style_directive}\n\n[CORE PREMISE]: {prompt}"


    payload = {
        "model": MODEL_NAME, 
        "messages": [
            {"role": "user", "content": full_instruction} 
        ],
        "temperature": 0.9,  # Increased temperature for MAXIMUM creativity
        "max_tokens": 2048   # Allow the AI to write a longer story
    }


    headers = {
        "Content-Type": "application/json"
    }


    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status() # Checks for connection errors (4xx or 5xx status codes)
        
        data = response.json()
        # Extracts the actual story text from the complex JSON structure
        story_text = data['choices'][0]['message']['content'].strip()
        return story_text


    except requests.exceptions.RequestException as e:
        print(f"\n🛑 CRITICAL ERROR connecting to the model API:")
        print(f"Error Details: {e}")
        print("HINTS: 1. Is LM Studio running in another terminal/window?")
        print(f"2. Did you correctly set the API_URL = \"{API_URL}\"?")
        return None


# ================================================================
# 💾 FILE UTILITY: SAVING THE OUTPUT
# ================================================================


def save_story(content):
    """Writes the final story text to a dedicated text file."""
    if content:
        filename = "Generated_Story.txt" # The file name it will save as
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("==================================================\n")
                f.write("✨ STORY GENERATION COMPLETE ✨\n")
                f.write("==================================================\n\n")
                f.write(content)
                f.write("\n\n--- END OF NARRATIVE ---")
            print(f"\n✅ SUCCESS! The story has been saved to '{filename}' in the current directory.")
        except Exception as e:
            print(f"\n🛑 ERROR: Could not save the story to file. Details: {e}")


# ================================================================
# 🚀 MAIN EXECUTION BLOCK (Handles User Input)
# ================================================================

def main():
    """Gathers user input and runs the story generation pipeline."""
    print("===============================================")
    print("✨ WELCOME TO THE AI STORY GENERATOR ✨")
    print("===============================================\n")
    
    # 1. GET USER INPUT (This handles the prompts correctly now)
    genre = input("❓ STEP 1: Please choose a genre for your story (e.g., Sci-Fi, Mystery, Romance): ").strip()
    premise = input("❓ STEP 2: Please provide a brief premise or character concept (What should the story be about?): ").strip()

    if not genre or not premise:
        print("\n🛑 ABORTED: You must provide both a Genre and a Premise to generate a story.")
        return

    # 2. GET INSTRUCTIONS & GENERATE STORY
    style_directive = get_style_instructions(genre)
    story = generate_story(premise, style_directive)

    # 3. SAVE OUTPUT
    if story:
        save_story(story)
    else:
        print("\n❌ Generation Failed. No story was written.")


if __name__ == "__main__":
    # This block ensures the code only runs when the script is executed directly, not imported.
    main()