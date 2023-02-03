from pytube import YouTube

def download_video(url):
    yt = YouTube(url)
    video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    video.download()

url = input("Enter the YouTube video URL: ")
download_video(url)