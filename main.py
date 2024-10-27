import yt_dlp
import shutil
import os
import librosa
import zipfile
import essentia.standard as es
import IPython.display as ipd
import time

def download_audio_from_youtube(youtube_url, output_path='./separated'):
    codec_choices = {1: 'mp3', 2: 'aac', 3: 'wav'}
    print("Pilih codec audio: 1 = mp3, 2 = aac, 3 = wav")
    codec_choice = int(input("Masukkan pilihan codec: "))
    preferredcodec = codec_choices.get(codec_choice, 'mp3')

    quality_choices = {1: '128', 2: '192', 3: '256', 4: '320'}
    print("Pilih kualitas audio: 1 = 128 kbps, 2 = 192 kbps, 3 = 256 kbps, 4 = 320 kbps")
    quality_choice = int(input("Masukkan pilihan kualitas: "))
    preferredquality = quality_choices.get(quality_choice, '128')

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': preferredcodec,
                'preferredquality': preferredquality,
            }],
            'outtmpl': output_path + '/%(title)s/original/%(title)s.%(ext)s',
            'quiet': False,
            'noplaylist': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            title = info.get('title', None)

        print(f"Berhasil diunduh dan dikonversi ke {preferredcodec} dengan kualitas {preferredquality} kbps.")
        return title

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return None

def separate_audio_demucs(input_file, stems_option, output_folder):
    print(f"Memulai pemisahan audio: {input_file}")
    if stems_option == 2:
        os.system(f'demucs --two-stems=vocals "{input_file}" -o "{output_folder}"')
    elif stems_option == 4:
        os.system(f'demucs "{input_file}" -o "{output_folder}"')
    else:
        print("Opsi tidak valid. Gunakan '2' untuk 2 stems atau '4' untuk 4 stems.")
    print("Pemisahan audio selesai.")

def analyze_audio(file_path):
    print(f"Analisis audio untuk: {file_path}")
    y, sr = librosa.load(file_path)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    tempo = round(float(tempo))
    loader = es.MonoLoader(filename=file_path)
    audio = loader()

    key_detector = es.KeyExtractor()
    key, scale, strength = key_detector(audio)

    print(f"Tempo: {tempo}, Key: {key}, Scale: {scale}")
    return tempo, key, scale

def play_audio(file_path):
    audio = ipd.Audio(file_path)
    display(audio)
    time.sleep(2)

# Memulai proses
youtube_url = input("Masukkan URL YouTube: ")

video_title = download_audio_from_youtube(youtube_url)

if video_title:
    base_path = f'./separated/{video_title}'
    os.makedirs(f'{base_path}/htdemucs', exist_ok=True)
    os.makedirs(f'{base_path}/based', exist_ok=True)
    os.makedirs(f'{base_path}/original', exist_ok=True)

    audio_files = [f for f in os.listdir(f'{base_path}/original') if f.endswith(('.mp3', '.aac', '.wav'))]
    if len(audio_files) == 0:
        print("File audio tidak ditemukan!")
    else:
        input_audio_file = os.path.join(f'{base_path}/original', audio_files[0])

        print("Pilih jumlah stems: 2 = 2 stems (vocal dan instrumental), 4 = 4 stems")
        stems_option = int(input("Masukkan pilihan: "))
        separate_audio_demucs(input_audio_file, stems_option, base_path)

        tempo, key, scale = analyze_audio(input_audio_file)

        output_folder = f"{base_path}/based"
        for stem in ['vocals', 'no_vocals', 'drums', 'bass', 'other']:
            stem_file = os.path.join(f"{base_path}/htdemucs/{audio_files[0][:-4]}", f"{stem}.wav")
            if os.path.exists(stem_file):
                new_name = f"{video_title} ({stem}) {tempo}BPM {key} {scale}.wav"
                os.rename(stem_file, os.path.join(output_folder, new_name))

        while True:
            print("Masukkan pilihan: 1 = Putar semua stem, 2 = Putar original, 3 = Lanjutkan")
            choice = input("Masukkan pilihan: ")

            if choice == '1':
                stem_files = [f for f in os.listdir(f'{base_path}/based') if f.endswith('.wav')]
                if stem_files:
                    for stem_file in stem_files:
                        print(f"Memutar stem file: {stem_file}")
                        play_audio(os.path.join(f'{base_path}/based', stem_file))
                        input("Tekan Enter untuk memutar stem berikutnya...")
                else:
                    print("Tidak ada file stem yang tersedia untuk diputar.")

            elif choice == '2':
                print(f"Memutar original file: {audio_files[0]}")
                play_audio(input_audio_file)
                input("Tekan Enter untuk melanjutkan setelah memutar original...")

            elif choice == '3':
                print("Melanjutkan ke proses pembuatan file zip...")
                zip_output_folder = f'./separated/{based_path}/output/{video_title}.zip'
                with zipfile.ZipFile(zip_output_folder, 'w') as zipf:
                    for stem_file in os.listdir(f'{base_path}/based'):
                        zipf.write(os.path.join(f'{base_path}/based', stem_file), stem_file)
                    for original_file in os.listdir(f'{base_path}/original'):
                        zipf.write(os.path.join(f'{base_path}/original', original_file), original_file)

                print(f"File zip berhasil dibuat: {zip_output_folder}")

                shutil.rmtree(f'{base_path}/htdemucs')
                shutil.rmtree(f'{base_path}/based')
                shutil.rmtree(f'{base_path}/original')
                print("Sampah telah dibersihkan.")
                break

else:
    print("Unduhan audio gagal.")
