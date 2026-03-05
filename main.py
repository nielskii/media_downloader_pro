from flask import Flask, request, render_template, jsonify, send_from_directory
from pytubefix import YouTube
from pytubefix.cli import on_progress
import re
import os
import ffmpeg


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
download_folder = 'downloads'

@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("index.html", yt=None)

#Cria uma rota para retornar as informações de thumb, titulo e autor assim que a pessoa coloca o input
@app.route('/get_info', methods=["GET", "POST"])
def get_info():
    url = request.args.get('url_video')
    yt = YouTube(url)
    return jsonify({
        'url_imagem': yt.thumbnail_url,
        'title': yt.title,
        'author': yt.author
    })

#Cria uma rota que utiliza a função de baixar os videos
@app.route("/download", methods=['GET', 'POST'])
def download():
    pasta_destino = "C:/videos"
    url = request.args.get('url_video')
    formato = request.args.get('formato')
    qualidade = request.args.get('qualidade')

    if (formato == 'mp4' and qualidade == "1080"):
        yt = YouTube(url, on_progress_callback=on_progress, allow_oauth_cache=True, use_oauth=True)
        filename = yt.title
        filename_limpo = re.sub(r'[^a-zA-Z0-9\s]', "", filename)
        
        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)

        # Define os caminhos
        video_temp = os.path.join(pasta_destino, f'{filename_limpo}_video.mp4')
        audio_temp = os.path.join(pasta_destino, f'{filename_limpo}.mp3')
        file_final = os.path.join(pasta_destino, f'{filename_limpo}.mp4')

        # Download das streams
        yt.streams.filter(res="1080p").first().download(output_path=pasta_destino, filename=f'{filename_limpo}_video.mp4')
        yt.streams.get_audio_only().download(output_path=pasta_destino, filename=f'{filename_limpo}.mp3')

        #Junta o video com o audio
        video_stream = ffmpeg.input(video_temp)
        audio_stream = ffmpeg.input(audio_temp)
        ffmpeg.output(video_stream, audio_stream, file_final, vcodec='copy', acodec='aac').run(overwrite_output=True)

        os.remove(video_temp)
        os.remove(audio_temp)

        return jsonify({
            'qualidade': f'{qualidade}p',
            'download_directory': f'Salvo no diretório : {pasta_destino}',
            'name_file': f'{filename_limpo}.mp4'
        })

    elif (formato == 'mp4' and qualidade == "720"):
        yt = YouTube(url, on_progress_callback=on_progress, allow_oauth_cache=True, use_oauth=True)
        filename = yt.title
        filename_limpo = re.sub(r'[^a-zA-Z0-9\s]', "", filename)
        ys = yt.streams.get_highest_resolution()
        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)
            print("Criando pasta destino para armazenar os videos.")
        else:
            pass
        ys.download(output_path=pasta_destino, filename=f'{filename_limpo}.mp4')
        return jsonify({
            'qualidade': f'{qualidade}p',
            'download_directory': f'Salvo no diretório : {pasta_destino}',
            'name_file': f'{filename_limpo}.mp4'
        })

    else:
        yt = YouTube(url, on_progress_callback=on_progress, allow_oauth_cache=True, use_oauth=True)
        filename = yt.title
        filename_limpo = re.sub(r'[^a-zA-Z0-9\s]', "", filename)
        ys = yt.streams.get_audio_only()
        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)
            print("Criando pasta destino para armazenar os videos.")
        else:
            pass
        ys.download(output_path=pasta_destino, filename=f'{filename_limpo}.mp3')
        return jsonify({
            'qualidade': f'{qualidade}mp3',
            'download_directory': f'Salvo no diretório : {pasta_destino}',
            'name_file': f'{filename_limpo}.mp3'
        })

if __name__ == "__main__":
    app.run(debug=True)
