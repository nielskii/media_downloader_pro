from flask import Flask, request, render_template, jsonify, send_file # Adicionado send_file
import yt_dlp
import ffmpeg
import re
import os

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("index.html", yt=None)

#Cria uma rota para retornar as informações de thumb, titulo e autor assim que a pessoa coloca o input
@app.route('/get_info', methods=["GET", "POST"])
def get_info():
    url = request.args.get('url_video')
    yt = yt_dlp.YoutubeDL()
    info = yt.extract_info(url,download=False)
    titulo = info.get('title')
    autor = info.get('uploader')
    thumbnail = info.get('thumbnail')
    return jsonify({
        'url_imagem': thumbnail,
        'title': titulo,
        'author': autor
    })

#Cria uma rota que utiliza a função de baixar os videos
@app.route("/download", methods=['GET', 'POST'])
def download():
    url = request.args.get('url_video')
    formato = request.args.get('formato')
    qualidade = request.args.get('qualidade')
    caminho_video = './videos'
    extensao = '*.webm'
    if (formato == 'mp4' and qualidade == "1080"):
        yt_opts = {
        'ffmpeg_location':'./ffmpeg/bin',
        'format':'bestvideo[vcodec^=avc]+bestaudio[acodec^=mp4a]/best[vcodec^=avc]/best',
        'merge_output_format':'mp4',
        'outtmpl': f'{caminho_video}/%(title)s.%(ext)s'
        }
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

    if (formato == 'mp4' and qualidade == "720"):
        yt_opts = {
        'ffmpeg_location':'./ffmpeg/bin',
        'format':'bestvideo[height<=720][vcodec^=avc]+bestaudio[acodec^=mp4a]/best[vcodec^=avc]/best',
        'merge_output_format':'mp4',
        'outtmpl': f'{caminho_video}/%(title)s.%(ext)s'
        }
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
    
    else:
        yt_opts = {
        'ffmpeg_location':'./ffmpeg/bin',
        'postprocessors':[{
            'key':'FFmpegExtractAudio',
            'preferredcodec':'mp3',
            'preferredquality':'192',
        }],
        'format':'bestaudio/best',
        'outtmpl': f'{caminho_video}/%(title)s.%(ext)s'
        }
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
            
    return jsonify({'mensagem': 'O video já está na pasta /videos, do seu projeto'})


if __name__ == "__main__":
    app.run(debug=True)