import os
import whisper
from transformers import MarianMTModel, MarianTokenizer
import evaluate  # For WER and BLEU metrics
import warnings  # For suppressing warnings

# I had this warning so I asked chatgpt to get rid of it so I have a cleaner result
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

# to load the whisper model
model_whisper = whisper.load_model("medium")

# this function is to transcribe the audio file into text. From the audio file returning the transcibred text
def transcribe_audio(audio_path):
    result = model_whisper.transcribe(audio_path)
    return result['text']

# to load the translation Model
model_name = "Helsinki-NLP/opus-mt-en-de"
tokenizer = MarianTokenizer.from_pretrained(model_name)
translation_model = MarianMTModel.from_pretrained(model_name)

#this function is for translation retunring the translated gemrna text
def translate_text(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    translated_tokens = translation_model.generate(**inputs)
    return tokenizer.decode(translated_tokens[0], skip_special_tokens=True)

# these functions are for the metrics WER and BLEU
wer_metric = evaluate.load("wer")
bleu_metric = evaluate.load("bleu")

def calculate_wer(reference, hypothesis):
    # Normalize the text: remove punctuation and convert to lowercase
    reference = reference.lower().replace(".", "").replace("?", "").replace("!", "").replace(",", "")
    hypothesis = hypothesis.lower().replace(".", "").replace("?", "").replace("!", "").replace(",", "")

    wer = wer_metric.compute(references=[reference], predictions=[hypothesis])
    return wer

def calculate_bleu(reference, hypothesis):
    bleu = bleu_metric.compute(predictions=[hypothesis], references=[[reference]])
    return bleu["bleu"]

# function to read from the given transcription and translation file
def read_ground_truth(file_path):
    ground_truth = {}
    with open(file_path, "r") as file:
        lines = file.readlines()
        current_audio = None
        for line in lines:
            line = line.strip()  # Remove whitespace for higher WER
            if line.startswith("recording_"): 
                current_audio = line
                ground_truth[current_audio] = {"transcription": "", "translation": ""}
            elif line.startswith("Transcription:"):  # Transcription
                ground_truth[current_audio]["transcription"] = line.split("Transcription:")[1].strip()
            elif line.startswith("Translation:"):  # Translation
                ground_truth[current_audio]["translation"] = line.split("Translation:")[1].strip()
    return ground_truth

# Path to the text file containing transcription and translation text
ground_truth_file = "/Users/dohahammouda/Desktop/Project1/Translation_Transcription_Unclean.txt"
ground_truth_data = read_ground_truth(ground_truth_file)

# get the real-life audios
audio_folder = "/Users/dohahammouda/Desktop/Project1/audio/Unclean_audio"
audio_files = []

# Walk through the directory as i had some in .mp3 and some in .wav
for subdir, _, files in os.walk(audio_folder):
    for file in files:
        if file.endswith(".mp3") or file.endswith(".wav"):
            audio_files.append(os.path.join(subdir, file))

# to process each audio file
for audio_file in audio_files:
    print(f"\nProcessing: {audio_file}")
    file_name = os.path.basename(audio_file)

    # transcribe the audio
    english_text = transcribe_audio(audio_file)
    print("English (Transcription):", english_text)

    # translate the transcription
    german_translation = translate_text(english_text)
    print("German (Translation):", german_translation)

    # Get translation and transcription text for this audio file
    if file_name in ground_truth_data:
        reference_transcription = ground_truth_data[file_name]["transcription"]
        reference_translation = ground_truth_data[file_name]["translation"]

        # in case no transcrition found
        if not reference_transcription.strip():
            print("Warning: Reference transcription is empty. Skipping WER calculation.")
        else:
            # in case if transcription is found, WER will be calculated
            wer_score = calculate_wer(reference_transcription, english_text)
            print(f"WER: {wer_score}")
        # in case no translation found
        if not reference_translation.strip():
            print("Warning: Reference translation is empty. Skipping BLEU calculation.")
        else:
            # in case if translation is found, Bleu will be calculated
            bleu_score = calculate_bleu(reference_translation, german_translation)
            print(f"BLEU: {bleu_score}")
    else:
        print(f"No data found for {file_name}.")

        #I added one audio with no transcription nor translation to test