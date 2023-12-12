from tkinter import (
    Tk,
    Listbox,
    PhotoImage,
    Button,
    Frame,
    Menu,
    Label,
    Scale,
    Toplevel,
    BooleanVar,
    Checkbutton,
    Entry,
)
from tkinter.ttk import Style
from model import model
import platform
import os


class view:
    def __init__(self, master):
        self.master = master
        master.title("La Vida")

        if platform.system() == "Windows":
            master.geometry(
                "300x500"
            )  # Tingkatkan tinggi untuk menampung fitur pencarian pada platform Windows
        else:
            master.geometry("300x450")

        style = Style()
        style.theme_use("clam")

        master.config(bg="white")
        master.resizable(False, False)
        master.iconphoto(True, PhotoImage(file=os.getcwd() + "/gui/logo.png"))

        # Widget Listbox untuk menampilkan daftar lagu
        self.songs_list = Listbox(
            master=master,
            fg="black",
            bg="white",
            borderwidth=5,
            justify="left",
            width=29,
            font=("poppins", 14),
        )

        # Frame untuk menampilkan informasi waktu dan slider untuk mengatur musik
        self.time_frame = Frame(master, bg="white")
        self.start_time = Label(
            master=self.time_frame, text="", fg="black", anchor="w", bg="white", padx=10
        )
        self.end_time = Label(
            master=self.time_frame, text="", fg="black", anchor="e", bg="white", padx=10
        )
        self.music_slider = Scale(
            master=master,
            from_=0,
            to=100,
            orient="horizontal",
            bg="white",
            relief="flat",
            length=270,
            showvalue=False,
        )

        # Frame untuk mengatur volume musik
        self.volume_frame = Frame(master, bg="white")
        self.volume_but = Button(
            master=self.volume_frame,
            borderwidth=0,
            relief="flat",
            bg="white",
            highlightthickness=0,
        )
        self.volume_slider = Scale(
            master=self.volume_frame,
            from_=0,
            to=100,
            relief="flat",
            orient="horizontal",
            bg="white",
            length=240,
            showvalue=False,
            label="",
        )
        self.volume_label = Label(
            master=master,
            text="100%",
            fg="white",
            relief="flat",
            anchor="center",
            bg="white",
        )

        # Instance dari kelas model untuk mengelola logika aplikasi
        self.model = model(
            self.songs_list,
            self.start_time,
            self.end_time,
            self.music_slider,
            self.volume_label,
            self.volume_slider,
            self.volume_but,
        )

        # Gambar-gambar untuk tombol kontrol pemutar musik
        self.previous_img = PhotoImage(file=os.getcwd() + "/gui/previous.png")
        self.play_img = PhotoImage(file=os.getcwd() + "/gui/play.png")
        self.pause_img = PhotoImage(file=os.getcwd() + "/gui/pause.png")
        self.next_img = PhotoImage(file=os.getcwd() + "/gui/next.png")
        self.add_img = PhotoImage(file=os.getcwd() + "/gui/add.png")
        self.add2_img = PhotoImage(file=os.getcwd() + "/gui/folder.png")
        self.remove_img = PhotoImage(file=os.getcwd() + "/gui/remove.png")
        self.repeat_img = PhotoImage(file=os.getcwd() + "/gui/repeat.png")
        self.search_img = PhotoImage(file=os.getcwd() + "/gui/search_bar.png")

        # Frame untuk menempatkan tombol kontrol pemutar musik
        self.btn_frame = Frame(master, bg="white")
        self.previous_btn = Button(
            master=self.btn_frame,
            image=self.previous_img,
            borderwidth=0,
            relief="flat",
            bg="white",
            command=self.model.previous_song,
            highlightthickness=0,
        )
        self.play_btn = Button(
            master=self.btn_frame,
            image=self.play_img,
            borderwidth=0,
            relief="flat",
            bg="white",
            command=self.model.play_song,
            highlightthickness=0,
        )
        self.pause_btn = Button(
            master=self.btn_frame,
            image=self.pause_img,
            borderwidth=0,
            relief="flat",
            bg="white",
            command=self.model.pause_song,
            highlightthickness=0,
        )
        self.next_btn = Button(
            master=self.btn_frame,
            image=self.next_img,
            borderwidth=0,
            relief="flat",
            bg="white",
            command=self.model.next_song,
            highlightthickness=0,
        )

        # Frame untuk mengedit daftar lagu
        self.edit_list_frame = Frame(master, bg="white")
        self.add_btn = Button(
            master=self.edit_list_frame,
            image=self.add_img,
            borderwidth=0,
            relief="flat",
            bg="white",
            command=self.model.add_file_to_playlist,
            highlightthickness=0,
        )
        self.add2_btn = Button(
            master=self.edit_list_frame,
            image=self.add2_img,
            borderwidth=0,
            relief="flat",
            bg="white",
            command=self.model.add_folder_to_playlist,
            highlightthickness=0,
        )
        self.remove_btn = Button(
            master=self.edit_list_frame,
            image=self.remove_img,
            borderwidth=0,
            relief="flat",
            bg="white",
            command=self.model.remove,
            highlightthickness=0,
        )

        # Checkbuttons untuk mengaktifkan mode acak 
        
        self.repeat_var = BooleanVar()
        self.repeat_btn = Checkbutton(
            master=self.edit_list_frame,
            image=self.repeat_img,
            variable=self.repeat_var,
            borderwidth=0,
            relief="flat",
            bg="white",
            command=self.model.toggle_loop,
            highlightthickness=0,
        )

        # Mengatur tata letak untuk tombol kontrol dan checkbuttons
        self.add_btn.pack(side="left", padx=20)
        self.add2_btn.pack(side="left", padx=20)
        self.remove_btn.pack(side="left", padx=20)
        self.repeat_btn.pack(side="right", padx=1)

        # Menempatkan daftar lagu di jendela
        self.songs_list.pack()

        # Frame untuk pencarian lagu
        self.search_frame = Frame(master=master, bg="#f0f0f0")  # Warna latar belakang abu-abu muda
        self.search_entry = Entry(
            master=self.search_frame, bg="white", fg="black", relief="flat", width=20
        )
        self.search_btn = Button(
            master=self.search_frame,
            image=self.search_img,
            bg="green",  # Warna hijau untuk tombol pencarian
            fg="white",   # Warna teks putih untuk kontras
            relief="flat",
            command=lambda: self.model.search_songs(self.search_entry.get()),
        )
        # Menempatkan kotak entri dan tombol pencarian di dalam frame pencarian
        self.search_frame.pack(fill="x", pady=5, padx=50)
        self.search_entry.pack(side="left", padx=(5,10) )
        self.search_btn.pack(side="right", padx=(10,5))

        # Menempatkan frame pengeditan daftar lagu
        self.edit_list_frame.pack(fill="x", pady=5, padx=20)
        self.time_frame.pack(fill="x", pady=5, padx=10)
        self.start_time.pack(side="left")
        self.end_time.pack(side="right")
        self.music_slider.pack()
        self.btn_frame.pack(fill="x", pady=10)
        self.previous_btn.grid(row=0, column=0, padx=(12, 10))
        self.play_btn.grid(row=0, column=1, padx=10)
        self.pause_btn.grid(row=0, column=2, padx=10)
        self.next_btn.grid(row=0, column=3, padx=(10, 12))
        self.volume_frame.pack(fill="x", pady=(5, 0))
        self.volume_but.pack(padx=(12, 10), side="left")
        self.volume_slider.pack(padx=(10, 22), side="right")
        self.volume_label.pack()

       
        # Mengonfigurasi tindakan tombol volume
        self.volume_but.config(command=self.model.mute)
        self.volume_slider.config(command=self.model.volume_slide)
