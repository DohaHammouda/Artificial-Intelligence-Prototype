import pyaudio
import wave
import os
import datetime

# Change this path to your desired save location
dataset_folder = "/Users/dohahammouda/Desktop/Project1/audio2"  # macOS/Linux
# dataset_folder = "C:\\Users\\yourusername\\Documents\\MyAudioDataset"  # Windows

# Ensure the folder exists
os.makedirs(dataset_folder, exist_ok=True)

# Recording settings
FORMAT = pyaudio.paInt16  
CHANNELS = 1  
RATE = 44100  
CHUNK = 1024  
RECORD_SECONDS = 20  # Set to 20 seconds for a longer recording

def record_audio():
    """Records audio and saves it with a unique filename (timestamp)."""
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    # Generate unique filename using timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"recording_{timestamp}.wav"
    file_path = os.path.join(dataset_folder, file_name)

    print(f"Recording... Speak now for {RECORD_SECONDS} seconds.")

    frames = []
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    # Stop recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the file
    with wave.open(file_path, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
    
    print(f"Saved recording: {file_path}")

# Run the recording function
record_audio()
