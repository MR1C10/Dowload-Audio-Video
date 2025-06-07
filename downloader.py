from pytubefix import YouTube
from pytubefix.cli import on_progress
import requests
from utils import limpar_nome
import os
import logging
import subprocess

# Configuração do logging
logging.basicConfig(
    filename="app.log",  
    level=logging.DEBUG, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def baixar_audio(url, destino):
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        nome = limpar_nome(yt.title)
        logging.info(f"Iniciando download de áudio: {nome}")

        # Seleciona o áudio com a maior taxa de bits usando 'abr'
        stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        stream.download(output_path=destino, filename=f"{nome}.mp3")
        logging.info(f"Áudio baixado com sucesso: {nome}.mp3")
        return yt.title, yt.thumbnail_url
    except Exception as e:
        logging.error(f"Erro ao baixar áudio: {e}")
        raise

def baixar_video(url, destino):
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        nome = limpar_nome(yt.title)
        logging.info(f"Iniciando download de vídeo: {nome}")

        
        video_stream = yt.streams.filter(adaptive=True, only_video=True, file_extension='mp4').order_by('resolution').desc().first()
        audio_stream = yt.streams.filter(adaptive=True, only_audio=True).order_by('abr').desc().first()

        video_path = os.path.normpath(os.path.join(destino, f"{nome}_video.mp4"))
        audio_path = os.path.normpath(os.path.join(destino, f"{nome}_audio.mp4"))
        output_path = os.path.normpath(os.path.join(destino, f"{nome}.mp4"))

        # Baixa os arquivos
        logging.info(f"Baixando vídeo para: {video_path}")
        video_stream.download(output_path=destino, filename=f"{nome}_video.mp4")
        logging.info(f"Baixando áudio para: {audio_path}")
        audio_stream.download(output_path=destino, filename=f"{nome}_audio.mp4")

        if not os.path.exists(video_path):
            logging.error(f"Erro: O arquivo de vídeo {video_path} não foi encontrado.")
            raise FileNotFoundError(f"Arquivo de vídeo não encontrado: {video_path}")
        if not os.path.exists(audio_path):
            logging.error(f"Erro: O arquivo de áudio {audio_path} não foi encontrado.")
            raise FileNotFoundError(f"Arquivo de áudio não encontrado: {audio_path}")

        ffmpeg_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "ffmpeg.exe"))
        ffmpeg_command = [
            ffmpeg_path, "-i", video_path, "-i", audio_path,
            "-c:v", "libx264", "-c:a", "aac", "-strict", "experimental", output_path
        ]
        logging.info(f"Executando comando: {' '.join(ffmpeg_command)}")
        try:
            result = subprocess.run(ffmpeg_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            logging.info(f"FFmpeg output: {result.stdout}")
            logging.info(f"Vídeo combinado salvo em: {output_path}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Erro ao executar o FFmpeg: {e.stderr}")
            raise Exception("Erro ao combinar vídeo e áudio com FFmpeg.")

        if os.path.exists(output_path):
            logging.info(f"Vídeo combinado criado com sucesso: {output_path}")
        else:
            logging.error("Erro: O vídeo combinado não foi criado.")

        logging.info("Removendo arquivos temporários...")
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(audio_path):
            os.remove(audio_path)

        return yt.title, yt.thumbnail_url
    except Exception as e:
        logging.error(f"Erro ao baixar vídeo: {e}")
        raise

def baixar_thumbnail(url):
    try:
        logging.info(f"Baixando thumbnail de: {url}")
        img_data = requests.get(url).content
        with open("thumbnail_temp.jpg", "wb") as handler:
            handler.write(img_data)
        logging.info("Thumbnail baixado com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao baixar thumbnail: {e}")
        raise