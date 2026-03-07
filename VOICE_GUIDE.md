## 🎤 Jarvis Voice Management

### Available Voices

**OpenAI TTS (Built-in, Fastest):**
- alloy - Neutral, professional
- echo - Clear, upbeat
- fable - Warm, storytelling
- onyx - Deep, authoritative
- nova - Natural, friendly ⭐ (default)
- shimmer - Bright, energetic

**ElevenLabs Free Tier (Premium Quality, Best for Character):**
- Aria - Young, friendly female
- Charlie - Casual, energetic male
- Charlotte - Professional, composed female
- Jessica - Articulate, engaged female
- Lily - Childlike, playful female
- Matilda - Wise, mature female
- Sarah - Crisp, professional female
- Sophia - Warm, approachable female
- Victoria - Authoritative, commanding female ⭐ (current)

### Commands

**List all voices:**
```bash
jarvis voices
```

Shows all available voices with current default marked with ⭐

**Set default voice:**
```bash
jarvis voice [name]
```

Example:
```bash
jarvis voice Charlie      # Set to Charlie
jarvis voice Sophia       # Set to Sophia
jarvis voice nova         # Set to nova (OpenAI)
```

**Generate speech with specific voice:**
```bash
jarvis tts "Hello world" --voice Victoria
```

### Voice Selection Guide

**For Professional Content:**
- Victoria (authoritative)
- Charlotte (professional)
- onyx (OpenAI, deep)

**For Friendly/Casual:**
- Charlie (energetic male)
- Sophia (warm)
- nova (OpenAI, default)

**For Creative Content:**
- Fable (OpenAI, storytelling)
- Aria (young, friendly)
- Sarah (crisp, clear)

**For Technical/Explanations:**
- Jessica (articulate)
- Charlotte (professional)
- echo (OpenAI, clear)

### Storage

Your voice preference is saved in:
```
data/config.json
```

It persists across sessions, so you only need to set it once!

### Tips

- ElevenLabs voices are higher quality but standard TTS speed
- OpenAI voices are faster but slightly less natural
- Test a few voices to find your favorite
- Current default is: Victoria
