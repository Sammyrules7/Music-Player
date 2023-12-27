import tkinter as tk
from tkinter import filedialog
import os
import pygame
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from PIL import Image, ImageTk
import io

class MusicPlayer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Music Player")
        self.geometry("500x500")

        pygame.init()
        pygame.mixer.init()

        self.current_file = None
        self.music_queue = []

        self.play_button = tk.Button(self, text="Play", command=self.play_or_enqueue_music)
        self.play_button.pack(pady=5)

        self.pause_button = tk.Button(self, text="Pause", command=self.pause_music)
        self.pause_button.pack(pady=5)

        self.skip_button = tk.Button(self, text="Skip", command=self.skip_music)
        self.skip_button.pack(pady=5)

        self.choose_enqueue_button = tk.Button(self, text="Choose File", command=self.choose_enqueue_file)
        self.choose_enqueue_button.pack(pady=5)

        self.queue_label = tk.Label(self, text="Music Queue:")
        self.queue_label.pack(pady=5)

        self.queue_listbox = tk.Listbox(self)
        self.queue_listbox.pack(pady=5)

        self.album_art_label = tk.Label(self)
        self.album_art_label.pack(pady=5)

    def choose_enqueue_file(self):
        file = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file", filetypes=(("MP3 files", "*.mp3"), ("All files", "*.*")))
        if file:
            if file not in self.music_queue:
                self.music_queue.append(file)
            self.update_queue_display()
        self.display_album_art(file)

    def play_or_enqueue_music(self):
        if self.current_file:
            pygame.mixer.music.load(self.current_file)
            pygame.mixer.music.play()
        elif self.music_queue:
            file = self.music_queue.pop(0)
            pygame.mixer.music.load(file)
            pygame.mixer.music.play()
            self.update_queue_display()

    def pause_music(self):
        pygame.mixer.music.pause()

    def skip_music(self):
        pygame.mixer.music.stop()

    def update_queue_display(self):
        self.queue_listbox.delete(0, tk.END)
        for file in self.music_queue:
            self.queue_listbox.insert(tk.END, os.path.basename(file))

    def display_album_art(self, current_file):
        try:
            audio = MP3(current_file, ID3=ID3)
            raw_data = audio.tags['APIC:'].data
            cover = Image.open(io.BytesIO(raw_data))
            cover = cover.resize((500, 500), Image.LANCZOS)
            photo = ImageTk.PhotoImage(cover)

            # Hide the listbox
            self.queue_listbox.pack_forget()

            # Display the image label
            self.album_art_label.config(image=photo)
            self.album_art_label.image = photo
            self.album_art_label.place(x=0, y=0)

            # Lift buttons to the top layer
            self.play_button.lift()
            self.pause_button.lift()
            self.skip_button.lift()
            self.choose_enqueue_button.lift()
            self.queue_label.lift()

            # Place the buttons in front of the album art
            self.play_button.place(x=150, y=250)
            self.pause_button.place(x=200, y=250)
            self.skip_button.place(x=250, y=250)
            self.choose_enqueue_button.place(x=300, y=250)
            self.queue_label.place(x=200, y=300)

        except Exception as e:
            print(e)

if __name__ == "__main__":
    player = MusicPlayer()
    player.mainloop()
