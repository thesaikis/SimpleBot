import yt_dlp

YDL_OPTIONS = {
    "format": "bestaudio",
    "noplaylist": True,
    'nocheckcertificate': True,
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'source_address': '0.0.0.0',
    "cookiefile": "cookies.txt",
}

yt = yt_dlp.YoutubeDL(YDL_OPTIONS)


def extract_audio(url: str):
    print("Extracting audio...")
    try:
        info = yt.extract_info(url, download=False)

        return {
            "source": next((f['url'] for f in info['formats'] if 'acodec' in f and f['acodec'] != 'none'), None),
            "title": info["title"],
            "thumbnail": info["thumbnail"],
            "original_url": url
        }
    except Exception as e:
        return None

    print("Finished")
