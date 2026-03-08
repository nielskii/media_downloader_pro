import yt_dlp
import os
import ffmpeg
caminho_video = './videos'
extensao = '*.webm'
yt_opts = {
    'ffmpeg_location': './ffmpeg/bin',
    'format':'bestvideo[vcodec^=avc]+bestaudio[acodec^=mp4a]/best[vcodec^=avc]/best',
    'merge_output_format':'mp4',
    'outtmpl': f'{caminho_video}/%(title)s.%(ext)s'
    }
url = "https://youtu.be/EgBJmlPo8Xw?si=WENeMVGOGOq-oCgz"

try:
    with yt_dlp.YoutubeDL(yt_opts) as ydl:
        ydl.download([url])
    for arquivo in os.listdir('.'):
        if arquivo.endswith(extensao):
            os.remove(arquivo)
            print(f"Arquivo com a extensão {extensao}, foi removido com sucesso")
    print("Download concluido com sucesso!")
except Exception as e:
    print(f"Ocorreu um erro, erro: {e}")

