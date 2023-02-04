import pafy

def download_video(url):
  video = pafy.new(url)
  best = video.getbest(preftype="mp4")
  best.download()

url = input("Enter the YouTube video URL: ")
download_video(url)