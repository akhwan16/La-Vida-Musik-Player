
from tkinter import filedialog, messagebox, PhotoImage
from time import strftime, gmtime, sleep
from pygame import mixer
import mutagen
import random
import os


class model:
    def __init__(
        self,
        songs_list,
        start_time,
        end_time,
        music_slider,
        volume_label,
        volume_slider,
        volume_but,
    ):
        self.mixer = mixer
        self.songs_list = songs_list
        self.start_time = start_time
        self.end_time = end_time
        self.music_slider = music_slider
        self.volume_label = volume_label
        self.volume_slider = volume_slider
        self.volume_but = volume_but
        self.songs_list_full = {}
        self.ispaused = False
        self.islooped = False
        self.ismuted = False
        self.mixer.init()
        self.volume_slider.set(50)
        self.mixer.music.set_volume(50)
        self.volume_none_img = PhotoImage(file="./gui/volume_none.png")
        self.volume_low_img = PhotoImage(file="./gui/volume_low.png")
        self.volume_mid_img = PhotoImage(file="./gui/volume_mid.png")
        self.volume_high_img = PhotoImage(file="./gui/volume_high.png")
        self.volume_but.config(image=self.volume_high_img)
        self.last_volume = 100


    def get_full_path(self, song_name):
        return self.songs_list_full[song_name]

    def add_file_to_playlist(self):
        songs = filedialog.askopenfilenames(
            title="Choose A Song",
            filetypes=[
                ("mp3 Files", "*.mp3"),
                ("wav Files", "*.wav"),
                ("flac Files", "*.flac"),
            ],
        )  
        for song in songs:  
            if song.split(".")[-1] not in [
                "mp3",
                "wav",
                "flac",
            ]:  
                messagebox.showwarning(
                )
            else:
                song_name = ".".join(
                    [
                        song.split("/")[-1].split(".")[i]
                        for i in range(0, len(song.split("/")[-1].split(".")) - 1)
                    ]
                )  
                self.songs_list_full[song_name] = song
                self.songs_list.insert("end", song_name)

    def add_folder_to_playlist(self):
        folder_path = filedialog.askdirectory(title="Choose A Folder")
        if not folder_path:
            return  

        supported_formats = [".mp3", ".wav", ".flac"]

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(tuple(supported_formats)):
                    song_name, _ = os.path.splitext(file)
                    song_path = os.path.join(root, file)

                    self.songs_list_full[song_name] = song_path
                    self.songs_list.insert("end", song_name)
                    
    def remove(self):
        self.songs_list_full.pop(self.songs_list.get("active"))
        self.songs_list.delete("active")

    def stop(self):
        try:
            self.start_time.after_cancel(self.loop)
        except:
            pass
        self.mixer.music.stop()
        self.music_slider.set(0)
        self.music_slider.config(from_=0, to=100)
        self.start_time.config(text="")
        self.end_time.config(text="")

    def previous_song(self):
        if len(self.songs_list_full) != 0:
            self.stop()
            if self.islooped:
                next_song_id = self.songs_list.curselection()[0]
            else:
                try:
                    next_song_id = self.songs_list.curselection()[0] - 1
                except:
                    next_song_id = 0

            self.songs_list.select_clear(0, "end")
            self.songs_list.activate(next_song_id)
            self.songs_list.select_set(next_song_id)

            self.play_song()

    def play_song(self):
        selected_song_index = self.songs_list.curselection()
        if not selected_song_index:
            return

        selected_song = self.songs_list.get(selected_song_index)
        self.stop()
        song_path = self.get_full_path(selected_song)

        try:
            self.mixer.music.load(song_path)
            self.mixer.music.play(start=0)
        except Exception as e:
            self.remove()  
            return

        song_length = int(mutagen.File(song_path).info.length)
        
        self.music_slider.set(0)
        self.start_time.config(text="00:00:00")
        self.end_time.config(text=strftime("%H:%M:%S", gmtime(song_length)))
        self.music_slider.config(from_=0, to=song_length)
        
        self.play_time()


    def pause_song(self):
        if len(self.songs_list_full) != 0:
            if self.ispaused:
                self.mixer.music.unpause()
            elif not self.ispaused:
                self.mixer.music.pause()
            self.ispaused = not self.ispaused

    def next_song(self):
        if len(self.songs_list_full) != 0:
            self.stop()
            if self.islooped:
                next_song_id = self.songs_list.curselection()[0]
            else:
                try:
                    next_song_id = self.songs_list.curselection()[0] + 1
                except:
                    next_song_id = 0
            
            self.songs_list.select_clear(0, "end")
            self.songs_list.activate(next_song_id)
            self.songs_list.select_set(next_song_id)
            self.play_song()
            

    def play_time(self):
        cur_time = int(self.mixer.music.get_pos() / 1000) + 1
        song = self.get_full_path(self.songs_list.get("anchor"))
        try:
            song_info = mutagen.File(song)
        except:
            pass
        if int(self.music_slider.get()) + 1 == song_info.info.length:
            return self.next_song()
        elif self.ispaused:
            pass
        elif abs(int(self.music_slider.get()) - cur_time) < 2:
            self.music_slider.set(cur_time)
            self.start_time.config(text=strftime("%H:%M:%S", gmtime(cur_time - 1)))
        else:
            self.music_slider.set(int(self.music_slider.get()))
            self.start_time.config(
                text=strftime("%H:%M:%S", gmtime(int(self.music_slider.get())))
            )
            self.music_slider.set(int(self.music_slider.get()) + 1)
            try:
                self.mixer.music.set_pos(int(self.music_slider.get()))
            except:
                return self.next_song()

        self.loop = self.start_time.after(1000, self.play_time)

    def volume_slide(self, val):
        slider_val = int(val)
        self.mixer.music.set_volume(int(slider_val) / 100.0)
        self.volume_label.config(text=str(slider_val) + "%")
        if slider_val == 0:
            self.volume_but.config(image=self.volume_none_img)
        elif slider_val <= 33:
            self.volume_but.config(image=self.volume_low_img)
        elif 33 < slider_val <= 66:
            self.volume_but.config(image=self.volume_mid_img)
        elif 66 < slider_val <= 100:
            self.volume_but.config(image=self.volume_high_img)

    def mute(self):
        if int(self.volume_slider.get()) == 0:
            self.volume_slider.set(self.last_volume)
        else:
            last_volume_temp = int(self.volume_slider.get())
            self.volume_slider.set(0)
            self.last_volume = last_volume_temp

    def toggle_loop(self):
        if len(self.songs_list_full) != 0:
            self.islooped = not self.islooped

    def show_all_songs(self):
        self.songs_list.delete(0, "end")
        for song_name in self.songs_list_full.keys():
            self.songs_list.insert("end", song_name)

    def show_songs(self, filtered_songs):
        self.songs_list.delete(0, "end")
        for song_name in filtered_songs:
            self.songs_list.insert("end", song_name)

    def search_songs(self, query):
        query = query.lower()
        if query:
            filtered_songs = [
                song for song in self.songs_list_full.keys() if query in song.lower()
            ]
            self.show_songs(filtered_songs)
        else:
            self.show_all_songs()