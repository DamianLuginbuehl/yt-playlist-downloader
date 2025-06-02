import os
import subprocess
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from pathlib import Path
import shutil
import re
from mutagen.id3 import ID3, TIT2, TPE1, TRCK

# === CONFIG ===
PLAYLIST_URL = "<YouTube or YouTube Music playlist URL>"
SONGS_PER_CD = 100  # safety limit for 700 MB CDs with 192 kbps CBR
CD_FOLDER_PREFIX = "CD_"
OUTPUT_FOLDER = Path("download")
AUDIO_QUALITY = "192k"  # target bitrate
MAX_SONGS = 300  # hard limit: only process the first 300 songs

# === SETUP ===
OUTPUT_FOLDER.mkdir(exist_ok=True)
os.chdir(OUTPUT_FOLDER)

# === 1. Download with yt-dlp ===
print("\n==> Loading songs from YouTube...")
subprocess.run(
    [
        "yt-dlp",
        "-x",
        "--audio-format",
        "mp3",
        "--audio-quality",
        "0",
        "--yes-playlist",
        "--playlist-items",
        f"1-{MAX_SONGS}",
        # "--write-info-json",
        "--output",
        "%(playlist_index)03d - %(artist)s - %(title)s.%(ext)s",
        PLAYLIST_URL,
    ],
    check=True,
)

# === 2. sort and split files ===
print("\n==> Soting & distributing Songs into CD-Folders...")
all_files = sorted(Path(".").glob("*.mp3"))
# limit to MAX_SONGS songs (hard limit)
all_files = all_files[: min(len(all_files), MAX_SONGS)]
cd_index = 1
for i in range(0, len(all_files), SONGS_PER_CD):
    cd_folder = Path(f"{CD_FOLDER_PREFIX}{cd_index}")
    cd_folder.mkdir(exist_ok=True)
    for f in all_files[i : i + SONGS_PER_CD]:
        target = cd_folder / f.name
        shutil.move(f, target)
    cd_index += 1

# === 3. Adapt Metadata ===
print("\n==> Adapting ID3-Tags...")
for cd_folder in sorted(Path(".").glob(f"{CD_FOLDER_PREFIX}*")):
    for i, mp3_file in enumerate(sorted(cd_folder.glob("*.mp3")), start=1):
        try:
            audio = MP3(mp3_file)
            if audio.tags is None:
                audio.add_tags()
            # dissect filename (recognises em dash and regular dash, with or without spaces)
            filename_parts = re.split(r"\s*[–-]\s*", mp3_file.stem, maxsplit=2)
            if len(filename_parts) == 3:
                index, artist, title = filename_parts
                # manually add ID3v2.4-Tags
                audio.tags.add(TIT2(encoding=3, text=title.strip()))
                audio.tags.add(TPE1(encoding=3, text=artist.strip()))
                audio.tags.add(TRCK(encoding=3, text=index.strip()))
            else:
                audio.tags.add(TIT2(encoding=3, text=mp3_file.stem))
            audio.save(v2_version=4)
        except Exception as e:
            print(f"Error with {mp3_file.name}: {e}")

print("\n✅ Finished! Your songs are distributed, renamed and have correct metadata.")
print("   Ordner:", OUTPUT_FOLDER.resolve())
