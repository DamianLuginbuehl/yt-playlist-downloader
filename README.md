# YouTube Playlist Downloader
This is a automatic downloaded for YouTube Playlists using python3. It downloads songs in the quality you can specify yourself.
The only requirement is that your desired playlist is either set to *unlisted* or *public*.\
It also applies the correct metadata (artist/s and track title).

### Programmed with CD burning in mind
This tool is optimised for CD burning as it splits up your songs into different CDs. You can set the song limit per CD and define how many songs you want to download, starting from the beginning. The factory settings are *100 songs/CD* with each song being *192 kbps CBR*. This is optimized for a *700MB CD*.

### Works with YouTube Music Radios\*
You can even download YouTube Music Playlists and Radios\* with this tool. The only requirement is that your desired playlist is either set to *"unlisted"* or *"public"*.\
\
_\* since Radios can be dynamic, it is recommended that you make a playlist out of them by saving the radio to a playlist. As per 02.06.25, this funcitonality is only available in the YouTube Music app for Android/iOS_


## How to use the downloader?
Edit the variable *PLAYLIST_URL* to the URL of your desired playlist in the *CONFIG* section. Also change the values of *SONGS_PER_CD*, *AUDIO_QUALITY* and *MAX_SONGS* depening on the capacity of your CDs, the amount of songs you want per CD and the amount of CDs you plan on burning.
```
# === CONFIG ===
PLAYLIST_URL = "<YouTube or YouTube Music playlist URL>"
SONGS_PER_CD = 100  # safety limit for 700 MB CDs with 192 kbps CBR
CD_FOLDER_PREFIX = "CD_"
OUTPUT_FOLDER = Path("download")
AUDIO_QUALITY = "192k"  # target bitrate
MAX_SONGS = 300  # hard limit: only process the first 300 songs
```
\
After that, run the script with the following command:
```
python download.py
```
\
You havt to additional packages as they are not included. Use the following command to install them:
```
pip install -r requirements.txt
```
\
Please wait, til the script is finished. All metadata and sorting operations are done *AFTER* all the songs are downloaded.\
The final Structure will look like this (example with 100 songs per CD):
```
download
├── CD_1
│   ├── 001 – Artist – Track.mp3
│   ├── 002 – Artist – Track.mp3
│   ├── 003 – Artist – Track.mp3
│   └── ...
├── CD_2
│   ├── 101 – Artist – Track.mp3
│   ├── 102 – Artist – Track.mp3
│   └── ...
├── CD_3
│   ├── 201 – Artist – Track.mp3
│   └── ...
├── CD_4
│   └── ...
└── ...
    └── ...
``` 