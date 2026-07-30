import tkinter as tk
from tkinter import filedialog, Menu, Frame, Button, Listbox, PhotoImage, END
import pygame
import os

root = tk.Tk()
root.title('Minimal Music Player')
root.geometry("1280x720")
root.directory = ""

pygame.mixer.init()

menubar = Menu(root)
root.config(menu=menubar)

songs = []
current_song = ""
paused = False

def load_music():
    global current_song
    root.directory = filedialog.askdirectory()
    if root.directory:
        print(f"Loading music from: {root.directory}")
    
    songs.clear()
    songlist.delete(0, END)
    try:
        for song in os.listdir(root.directory):
            name, ext = os.path.splitext(song)
            if ext.lower() == '.mp3':
                songs.append(song)

        for song in songs:
            songlist.insert(END, song)

        if songs:
            songlist.selection_set(0)
            current_song = songlist.get(tk.ACTIVE)
        else:
            current_song = ""
    except Exception:
        current_song = ""

def play_music():
    global current_song, paused
    if getattr(root, 'directory', "") == "":
        print("Error: Please load a music folder first.")
        return

    selected_indices = songlist.curselection()
    if selected_indices:
        current_song = songlist.get(selected_indices[0])
    if not current_song:
        print("Error: Please select a song from the list first.")
        return

    if not paused:
        try:
            pygame.mixer.music.load(os.path.join(root.directory, current_song))
            pygame.mixer.music.play()
        except Exception as e:
            print("Unable to play:", e)
    else:
        pygame.mixer.music.unpause()
        paused = False

def pause_music():
    global paused
    pygame.mixer.music.pause()
    paused = True

def next_music():
    global current_song, paused

    try:
        songlist.selection_clear(0, END)
        songlist.selection_set(songs.index(current_song) + 1)
        current_song = songs[songlist.curselection()[0]]
        play_music()
    except:
        pass    

def prev_music():
    global current_song, paused

    try:
        songlist.selection_clear(0, END)
        songlist.selection_set(songs.index(current_song) - 1)
        current_song = songs[songlist.curselection()[0]]
        play_music()
    except:
        pass                   

organise_menu = Menu(menubar, tearoff=False)
organise_menu.add_command(label='Select Folder', command=load_music)
menubar.add_cascade(label='organise', menu=organise_menu)

songlist = Listbox(root, bg="light blue", fg="white", width=100, height=15)
songlist.pack()

play_btn_image = PhotoImage(file='play.png')
pause_btn_image = PhotoImage(file='pause.png')
next_btn_image = PhotoImage(file='next.png')
prev_btn_image = PhotoImage(file='previous.png')

control_frame = Frame(root)
control_frame.pack()

play_btn = Button(control_frame, image=play_btn_image, borderwidth=0, command=play_music)
pause_btn = Button(control_frame, image=pause_btn_image, borderwidth=0, command=pause_music)
next_btn = Button(control_frame, image=next_btn_image, borderwidth=0, command=next_music)
prev_btn = Button(control_frame, image=prev_btn_image, borderwidth=0, command=prev_music)

play_btn.grid(row=0, column=1, padx=7, pady=10)
pause_btn.grid(row=0, column=2, padx=7, pady=10)
next_btn.grid(row=0, column=3, padx=7, pady=10)
prev_btn.grid(row=0, column=0, padx=7, pady=10)

selected_folder = filedialog.askdirectory(title="Select Music Folder")
print("You Selected:", selected_folder)

root.mainloop()
