from gtts import gTTS

def generate_tts_audio(text, output_path):
    tts = gTTS(text=text, lang='en')
    tts.save(output_path)

texts_to_speak = [
    "Why don't skeletons fight each other? They don't have the guts.",
    "Why don’t eggs tell jokes? Because they’d crack each other up.",
    "What do you call fake spaghetti? An impasta!",
    "I’m reading a book about anti-gravity. It’s impossible to put down.",
    "Why did the math book look sad? Because it had too many problems.",
    "Why don’t oysters share their pearls? Because they’re shellfish!",
    "Why did the tomato turn red? Because it saw the salad dressing!",
    "What did one ocean say to the other ocean? Nothing, they just waved.",
    "I only know 25 letters of the alphabet. I don’t know y.",
    "Who won the neck decorating contest? It was a tie.",
    "How is my wallet like an onion? Every time I open it, I cry.",
    "What did one wall say to the other wall? I'll meet you at the corner!",
    "Why did the coffee file a police report? It got mugged!",
    "Try the seafood diet—you see food, then you eat it.",
    "Why can't a leopard hide? He's always spotted.",
    "Why did the orange lose the race? It ran out of juice.",
    "Where do boats go when they're sick? To the dock.",
    "Why was 6 afraid of 7? Because 7 ate 9!",
    "I'm so good at sleeping that I do it with my eyes closed.",
    "What do you call a pencil with two erasers? Pointless.",
    "You can't trust atoms. They make up everything!",
    "Why do bees have sticky hair? Because they use a honeycomb.",
    "What did the police officer say to her belly button? You're under a vest!",
    "Wanna hear a joke about construction? I'm still workin' on it!"
]

for i, text in enumerate(texts_to_speak, 1):
    output_audio_path = f"/Users/dohahammouda/Desktop/Project1/generated_audio{i}.mp3"
    generate_tts_audio(text, output_audio_path)
    print(f"Audio saved to {output_audio_path}")
