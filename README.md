# MP3 to Subtitle Converter Using Whisper
This Python script converts MP3 audio files into subtitle (SRT) files by transcribing the audio using OpenAI's Whisper model. It includes features like MP3-to-WAV conversion, audio transcription, and SRT file generation, all with error handling and logging.


## Features
- Converts MP3 files to WAV format using `pydub`.<br>
- Transcribes audio files to text with Whisper, supporting multiple models (`base`, `small`, `medium`, `large`).<br>
- Generates timestamped subtitle files in the SRT format.<br>
- Includes a graphical interface to select MP3 files.<br>
- Provides live progress bars for MP3-to-WAV conversion and subtitle creation.<br>
- Logs all key events and errors to a log file (`mp3_to_srt.log`).<br>


## Requirements
Before running the script, ensure the following dependencies are installed:<br>

## Python Libraries
Install the required libraries via pip:<br>
```
pip install whisper tqdm pydub tkinter
```
## FFmpeg
FFmpeg is required for audio processing:<br>

- Download FFmpeg from FFmpeg.org.<br>
- Update the `udioSegment.converter` and `AudioSegment.ffprobe` paths in the script to point to your FFmpeg installation.

## Usage
### 1. Select MP3 Files<br>
The script opens a file dialog to select MP3 files, saving the selection in mp3_files.json.

### 2. Model Selection<br>
You can choose a Whisper model to use for transcription:

- `base`, `small`, `medium`, or `large` (default: `base`).
  
### 3. Process Workflow
For each selected MP3 file:

1. **Convert MP3 to WAV:** Converts the MP3 file to a WAV file.<br>
2. **Transcribe Audio:** Uses the Whisper model to transcribe the WAV file.<br>
3. **Generate SRT File:** Creates a subtitle (SRT) file with timestamps.<br>

## How to Run
1. Clone or download this repository.<br>
2. Run the script in a terminal:<br>
```
python mp3_to_srt.py
```
3. Follow the prompts:<br>
   - Select MP3 files.<br>
   - Choose a Whisper model.<br>
   - Wait for processing to complete.<br>

## Example<br>
```
Step 0: Selecting MP3 files...
Step 1: Converting 'example.mp3' to WAV...
Step 2: Transcribing 'example.wav' to subtitles...
Step 3: Creating subtitles for 'example.mp3'...
Subtitle file saved as 'example.srt'.
```

## Output
- **SRT File:** A subtitle file with time-stamped transcriptions.<br>
- **Log File:** A log of all events and errors (mp3_to_srt.log).<br>

## Code Overview
### Key Functions
1. `convert_mp3_to_wav(mp3_file, wav_file)` Converts MP3 files to WAV format with progress visualization.

2. `transcribe_audio_to_subtitles(wav_file, model_name)` Transcribes WAV audio files to text using the Whisper model.

3. `create_srt_file(segments, output_file)` Generates an SRT file from transcription segments with timestamps.

4. `format_time(seconds)` Converts seconds into SRT-compatible timestamp format.

5. `select_mp3_files()` Opens a file dialog to select MP3 files and saves the list in a JSON file.

6. `get_model_choice()` Prompts the user to select a Whisper model.

7. `main()` Orchestrates the overall workflow:

    - Select MP3 files.<br>
    - Process each file (convert, transcribe, and create subtitles).<br>
    
## Logging and Error Handling
- **Log File:** All actions and errors are logged in `mp3_to_srt.log`.<br>
- **Error Handling:** Exceptions are logged, and the script gracefully skips problematic files.
