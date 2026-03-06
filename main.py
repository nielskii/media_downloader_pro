from flask import Flask, request, render_template, jsonify, send_file # Adicionado send_file
from pytubefix import YouTube
from pytubefix.cli import on_progress
import re
import os
import tempfile

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

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
    # Usa a pasta temporária do sistema (funciona em Windows e Vercel)
    pasta_destino = tempfile.gettempdir() 
    
    url = request.args.get('url_video')
    formato = request.args.get('formato')
    qualidade = request.args.get('qualidade')

    yt = YouTube(url, on_progress_callback=on_progress, allow_oauth_cache=True, use_oauth=True)
    filename = yt.title
    filename_limpo = re.sub(r'[^a-zA-Z0-9\s]', "", filename)

    if (formato == 'mp4' and qualidade == "720"):
        file_final = os.path.join(pasta_destino, f'{filename_limpo}.mp4')
        ys = yt.streams.get_highest_resolution()
        ys.download(output_path=pasta_destino, filename=f'{filename_limpo}.mp4')
        
        return send_file(file_final, as_attachment=True)

    else:
        file_final = os.path.join(pasta_destino, f'{filename_limpo}.mp3')
        ys = yt.streams.get_audio_only()
        ys.download(output_path=pasta_destino, filename=f'{filename_limpo}.mp3')
        
        return send_file(file_final, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)