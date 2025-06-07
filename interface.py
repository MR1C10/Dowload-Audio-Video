import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from downloader import baixar_audio, baixar_video, baixar_thumbnail

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        self.destino = ""

        # Título
        self.title_label = ttk.Label(root, text="YouTube Downloader", font=("Helvetica", 16))
        self.title_label.pack(pady=10)

        # Link
        self.url_label = ttk.Label(root, text="Cole a URL do vídeo:")
        self.url_label.pack()

        self.url_entry = ttk.Entry(root, width=70)
        self.url_entry.pack(pady=5)

        # Selecionar pasta
        self.destino_btn = ttk.Button(root, text="Selecionar pasta", command=self.escolher_pasta)
        self.destino_btn.pack(pady=5)

        # Botões
        self.botao_frame = ttk.Frame(root)
        self.botao_frame.pack(pady=10)

        self.audio_btn = ttk.Button(self.botao_frame, text="Baixar Áudio", command=self.baixar_audio)
        self.audio_btn.pack(side=tk.LEFT, padx=20)

        self.video_btn = ttk.Button(self.botao_frame, text="Baixar Vídeo", command=self.baixar_video)
        self.video_btn.pack(side=tk.RIGHT, padx=20)

        self.thumbnail_label = ttk.Label(root)
        self.thumbnail_label.pack(pady=10)

    def escolher_pasta(self):
        self.destino = filedialog.askdirectory()
        if self.destino:
            messagebox.showinfo("Destino", f"Arquivos serão salvos em:\n{self.destino}")

    def baixar_audio(self):
        url = self.url_entry.get().strip()
        if not url or not self.destino:
            messagebox.showwarning("Atenção", "Informe a URL e selecione uma pasta.")
            return
        try:
            titulo, thumb = baixar_audio(url, self.destino)
            baixar_thumbnail(thumb)
            self.exibir_thumbnail("thumbnail_temp.jpg")
            messagebox.showinfo("Concluído", f"Áudio baixado:\n{titulo}")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def baixar_video(self):
        url = self.url_entry.get().strip()
        if not url or not self.destino:
            messagebox.showwarning("Atenção", "Informe a URL e selecione uma pasta.")
            return
        try:
            titulo, thumb = baixar_video(url, self.destino)
            baixar_thumbnail(thumb)
            self.exibir_thumbnail("thumbnail_temp.jpg")
            messagebox.showinfo("Concluído", f"Vídeo baixado:\n{titulo}")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def exibir_thumbnail(self, caminho_img):
        try:
            img = Image.open(caminho_img)
            img = img.resize((320, 180),  Image.Resampling.LANCZOS)
            foto = ImageTk.PhotoImage(img)
            self.thumbnail_label.configure(image=foto)
            self.thumbnail_label.image = foto
        except:
            self.thumbnail_label.configure(text="(Erro ao carregar thumbnail)")
