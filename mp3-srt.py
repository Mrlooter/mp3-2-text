import os
import json
import whisper
from pydub import AudioSegment
from pydub.utils import which
from tqdm import tqdm
from tkinter import Tk, filedialog
import logging
import warnings


warnings.filterwarnings("ignore", category=FutureWarning, module="whisper")

# Set up logging
logging.basicConfig(
    filename="mp3_to_srt.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Set explicit paths to ffmpeg and ffprobe
AudioSegment.converter = r"C:\ffmpeg-6.1.1-full_build\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"C:\ffmpeg-6.1.1-full_build\bin\ffprobe.exe"


def convert_mp3_to_wav(mp3_file, wav_file):
    """Converts an MP3 file to WAV format with a live progress bar."""
    try:
        audio = AudioSegment.from_mp3(mp3_file)
        total_duration = len(audio)  # Duration in milliseconds

        # Simulate progress
        with tqdm(total=total_duration, desc="Converting MP3 to WAV", unit="ms") as pbar:
            audio.export(wav_file, format="wav")
            pbar.update(total_duration)  # Update progress to 100%

        logging.info(f"Converted '{mp3_file}' to '{wav_file}'.")
    except Exception as e:
        logging.error(f"Error converting '{mp3_file}' to WAV: {e}")
        raise


def transcribe_audio_to_subtitles(wav_file, model_name):
    """Transcribes audio from a WAV file to text using Whisper and returns timestamped segments."""
    try:
        logging.info(f"Loading Whisper model '{model_name}'...")
        model = whisper.load_model(model_name)
        logging.info(f"Model '{model_name}' loaded successfully.")
        
        logging.info(f"Starting transcription for '{wav_file}'...")
        result = model.transcribe(wav_file, verbose=True)
        logging.info(f"Transcription completed for '{wav_file}'.")
        
        return result["segments"]
    except Exception as e:
        logging.error(f"Error during transcription of '{wav_file}': {e}")
        raise



def create_srt_file(segments, output_file):
    """Creates an SRT file from Whisper transcription segments with a live progress bar."""
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            with tqdm(total=len(segments), desc="Creating subtitles") as pbar:
                for i, segment in enumerate(segments):
                    start_time = segment['start']
                    end_time = segment['end']
                    text = segment['text']

                    # Write SRT entry
                    f.write(f"{i + 1}\n")
                    f.write(f"{format_time(start_time)} --> {format_time(end_time)}\n")
                    f.write(f"{text.strip()}\n\n")

                    # Update progress bar
                    pbar.update(1)

        logging.info(f"SRT file '{output_file}' created.")
    except Exception as e:
        logging.error(f"Error creating SRT file '{output_file}': {e}")
        raise


def format_time(seconds):
    """Formats time in seconds to SRT timestamp format."""
    milliseconds = int((seconds % 1) * 1000)
    seconds = int(seconds)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"


def select_mp3_files():
    """Opens a file dialog to select MP3 files and saves the list to a JSON file."""
    root = Tk()
    root.withdraw()  # Hide the main window
    root.attributes('-topmost', True)  # Bring the dialog to the front
    mp3_files = filedialog.askopenfilenames(title="Select MP3 Files", filetypes=[("MP3 Files", "*.mp3")])

    if mp3_files:
        with open("mp3_files.json", "w") as f:
            json.dump(list(mp3_files), f, indent=4)
        print("Selected MP3 files have been saved to 'mp3_files.json'.")
        logging.info(f"Selected MP3 files: {mp3_files}")
    else:
        print("No files selected.")
        with open("mp3_files.json", "w") as f:
            json.dump([], f)  # Save an empty list
        logging.warning("No MP3 files selected.")


def get_model_choice():
    """Prompts the user to select a Whisper model."""
    print("Select a Whisper model: (base, small, medium, large)")
    model_name = input("Enter model name (default: base): ").strip()
    return model_name if model_name else "base"


def main():
    # Step 0: Select MP3 files dynamically
    print("Step 0: Selecting MP3 files...")
    select_mp3_files()

    # Load selected MP3 files from JSON
    if not os.path.exists("mp3_files.json"):
        print("Error: No MP3 files selected. Please run the program again.")
        logging.error("No MP3 files selected. Exiting.")
        return

    with open("mp3_files.json", "r") as f:
        mp3_files = json.load(f)

    if not mp3_files:  # Check if the list is empty
        print("No MP3 files to process. Exiting.")
        logging.warning("MP3 file list is empty. Exiting.")
        return

    # Get Whisper model choice
    model_name = get_model_choice()

    for mp3_file in mp3_files:
        print(f"Processing file: {mp3_file}")
        logging.info(f"Processing file: {mp3_file}")

        if not os.path.exists(mp3_file):
            print(f"Error: File '{mp3_file}' not found. Skipping.")
            logging.error(f"File '{mp3_file}' not found. Skipping.")
            continue

        wav_file = os.path.splitext(mp3_file)[0] + ".wav"  # Temporary WAV file
        srt_file = os.path.splitext(mp3_file)[0] + ".srt"  # Output SRT file

        try:
            # Step 1: Convert MP3 to WAV
            print(f"Step 1: Converting '{mp3_file}' to WAV...")
            convert_mp3_to_wav(mp3_file, wav_file)

            # Step 2: Transcribe audio to subtitles
            print(f"Step 2: Transcribing '{wav_file}' to subtitles...")
            segments = transcribe_audio_to_subtitles(wav_file, model_name)

            # Step 3: Create SRT file
            print(f"Step 3: Creating subtitles for '{mp3_file}'...")
            create_srt_file(segments, srt_file)

            print(f"Subtitle file saved as '{srt_file}'.")
        except Exception as e:
            print(f"An error occurred while processing '{mp3_file}': {e}")
            logging.error(f"An error occurred while processing '{mp3_file}': {e}")
        finally:
            # Clean up temporary WAV file
            if os.path.exists(wav_file):
                os.remove(wav_file)
                logging.info(f"Temporary WAV file '{wav_file}' deleted.")


if __name__ == "__main__":
    main()
