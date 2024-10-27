Here's a `README.md` file you can use for your GitHub repository:

---

# YouTube Audio Downloader and Separator

This repository provides a Python-based application for downloading audio from YouTube, separating audio stems, analyzing key and tempo, and optionally playing and packaging the processed files. It utilizes `yt-dlp`, `librosa`, `essentia`, and `demucs` for various audio processing tasks.

## Features

- **Download audio from YouTube** with configurable codec and quality options.
- **Separate audio stems** using `demucs` with options for 2 stems (vocal and instrumental) or 4 stems.
- **Analyze tempo, key, and scale** of the audio file.
- **Playback** of original and separated stem files.
- **Package** processed audio files into a zip file for easy sharing.
- **Automated cleanup** of intermediate files after completion.

## Requirements

This project requires the following dependencies:

```sh
pip install yt-dlp
pip install librosa essentia
pip install demucs
```

## Usage

1. **Run the Script**: Execute the script to start the audio download, separation, and analysis process.

2. **Input YouTube URL**: Enter the YouTube URL of the audio you want to process.

3. **Choose Codec and Quality**:
   - Select audio codec: `mp3`, `aac`, or `wav`.
   - Choose audio quality: `128`, `192`, `256`, or `320 kbps`.

4. **Stem Separation**: Specify the number of stems:
   - 2 stems: separates into vocal and instrumental.
   - 4 stems: separates into vocal, bass, drums, and other.

5. **Analyze Key and Tempo**: The program will analyze and print the key, scale, and tempo of the audio.

6. **Play Audio Stems**: Choose to play individual stems or the original audio.

7. **Zip Output Files**: After playback, the processed files can be packaged into a `.zip` file.

8. **Cleanup**: The script will clean up intermediate files after zipping.

## Code Breakdown

- `download_audio_from_youtube`: Downloads audio from a YouTube URL based on user-selected codec and quality.
- `separate_audio_demucs`: Separates audio stems using `demucs`.
- `analyze_audio`: Analyzes the audio file for tempo, key, and scale.
- `play_audio`: Plays audio files using IPython’s audio display.
- **Main Flow**: Handles user inputs, coordinates the workflow, and cleans up files.

## Example

```python
python script.py
# Input prompts will guide you through codec, quality, and stem options.
```

## License

This project is licensed under the MIT License.

---

This should provide a clear structure for users to understand and work with the script.
