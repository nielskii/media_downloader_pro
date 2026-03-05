from instagrapi import DownloadVideoMixin
from urllib.parse import urlparse

url = "https://www.instagram.com/reels/DT1bxuMke-r/"
resultado = urlparse(url)
path_limpo = resultado.path.strip("/")
resultado_limpo = path_limpo.split("/")
print(resultado_limpo[-1])
teste = DownloadVideoMixin()
teste.video_download(media_pk=resultado_limpo, )
pasta = 'C:/Downloads'

print("Baixado com sucesso")