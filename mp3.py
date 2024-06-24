from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
#запуск tkinter
root = Tk()
#задаём название окна плеера и его размеры
root.title("Music player")
root.geometry("550x350")

#Запустим pygame
pygame.mixer.init()

#функция позволяющая получить информацию о продолжительности песни
def play_time():
    if stopped:
        return
    current_time = pygame.mixer.music.get_pos() / 1000
    song = song_box.get(ACTIVE)
    song = f'C:/Users/user/PycharmProjects/pythonProject/music/{song}.mp3'
    song_mut = MP3(song)
    global song_length
    song_length = song_mut.info.length
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))
    current_time += 1
    if int(my_slider.get()) == int(song_length):
        status_bar.config(text=f'Пройденное время:  {converted_song_length}   ')

    elif paused:
        pass

    elif int(my_slider.get()) == int(current_time):
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(current_time))

    else:
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(my_slider.get()))
        converted_current_time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))
        status_bar.config(text=f'Пройденное время:  {converted_current_time}  из  {converted_song_length}   ')
        next_time = int(my_slider.get()) + 1
        my_slider.config(value=next_time)
    #my_slider.config(value=int(current_time))
    status_bar.after(1000, play_time)

#функция добавления музыки, воспроизведения музыки, остановка музыки
def add_song():
    song = filedialog.askopenfilename(initialdir='music/', title = "Выберите песню", filetypes=(("mp3 files", "*.mp3"),))
    song = song.replace("C:/Users/user/PycharmProjects/pythonProject/music", "")
    song = song.replace(".mp3", "")
    song_box.insert(END, song)

def add_songs():
    songs = filedialog.askopenfilenames(initialdir='music/', title="Выберите песню", filetypes=(("mp3 files", "*.mp3"),))
    for song in songs:
        song = song.replace("C:/Users/user/PycharmProjects/pythonProject/music", "")
        song = song.replace(".mp3", "")
        song_box.insert(END, song)
def play():
    global stopped
    stopped = False
    song = song_box.get(ACTIVE)
    song = f'C:/Users/user/PycharmProjects/pythonProject/music/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()
    play_time()
    current_volume = pygame.mixer.music.get_volume()
    slider_label.config(text=current_volume * 100)
    slider_position = int(song_length)
    my_slider.config(to=slider_position, value=0)

    current_volume = current_volume * 100
    slider_label.config(text=current_volume)

    if int(current_volume) < 1:
        volume_meter.config(image=vol0)
    elif int(current_volume) > 0 and int(current_volume) <= 33:
        volume_meter.config(image=vol1)
    elif int(current_volume) >= 33 and int(current_volume) <= 66:
        volume_meter.config(image=vol2)
    elif int(current_volume) >= 66 and int(current_volume) <= 100:
        volume_meter.config(image=vol3)

global stopped
stopped = False
def stop():
    status_bar.config(text='')
    my_slider.config(value=0)
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)
    status_bar.config(text='')
    global stopped
    stopped = True

def next_song():
    status_bar.config(text='')
    my_slider.config(value=0)
    next_one = song_box.curselection()
    next_one = next_one[0]+1
    song = song_box.get(next_one)
    song = f'C:/Users/user/PycharmProjects/pythonProject/music/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()
    song_box.selection_clear(0, END)
    song_box.activate(next_one)
    song_box.selection_set(next_one)

def previos_song():
    status_bar.config(text='')
    my_slider.config(value=0)
    next_one = song_box.curselection()
    next_one = next_one[0] - 1
    song = song_box.get(next_one)
    song = f'C:/Users/user/PycharmProjects/pythonProject/music/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()
    song_box.selection_clear(0, END)
    song_box.activate(next_one)
    song_box.selection_set(next_one)

def delete_song():
    stop()
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()

def delete_all_songs():
    stop()
    song_box.delete(0, END)
    pygame.mixer.music.stop()

global paused
paused = False

def pause(is_paused):
    global paused
    paused = is_paused
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True

def slide(x):
    song = song_box.get(ACTIVE)
    song = f'C:/Users/user/PycharmProjects/pythonProject/music/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(start=int(my_slider.get()))

def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())
    current_volume = pygame.mixer.music.get_volume()
    current_volume = current_volume * 100
    slider_label.config(text = current_volume)

    if int(current_volume) < 1:
        volume_meter.config(image=vol0)
    elif int(current_volume) > 0 and int(current_volume) <=33:
        volume_meter.config(image=vol1)
    elif int(current_volume) >=  33 and int(current_volume) <=66:
        volume_meter.config(image=vol2)
    elif int(current_volume) >=  66 and int(current_volume) <=100:
        volume_meter.config(image=vol3)


master_frame = Frame(root)
master_frame.pack(pady=20)

#Создадим плейлист
song_box = Listbox(master_frame, bg= "black", fg ="green", width =50, selectbackground="gray", selectforeground="black")
song_box.grid(row=0, column=0)

#Кнопки управления
back_btn_img = PhotoImage(file="back.png")
forward_btn_img = PhotoImage(file="forward.png")
play_btn_img= PhotoImage(file="play.png")
pause_btn_img= PhotoImage(file="pause.png")
stop_btn_img= PhotoImage(file="stop.png")

global vol0
global vol1
global vol2
global vol3
vol0 = PhotoImage(file="vol0.png")
vol1 = PhotoImage(file="vol1.png")
vol2 = PhotoImage(file="vol2.png")
vol3 = PhotoImage(file="vol3.png")

control_frame = Frame(master_frame)
control_frame.grid(row=1, column=0, pady=20)

volume_meter = Label(master_frame, image = vol3)
volume_meter.grid(row=1, column = 1, padx = 10)

volume_frame = LabelFrame(master_frame, text = "Громкость")
volume_frame.grid(row=0,column=1, padx=20)

slider_label = Label(root, text="0")
slider_label.pack(pady=10)

back_button = Button(control_frame, image= back_btn_img, borderwidth=0, command=previos_song)
forward_button = Button(control_frame, image= forward_btn_img, borderwidth=0, command=next_song)
play_button = Button(control_frame, image= play_btn_img, borderwidth=0, command = play)
pause_button = Button(control_frame, image= pause_btn_img, borderwidth=0, command=lambda:pause(paused))
stop_button = Button(control_frame, image= stop_btn_img, borderwidth=0, command = stop)

back_button.grid(row=0, column=0, padx=10)
forward_button.grid(row=0, column=1,padx=10)
play_button.grid(row=0, column=2,padx=10)
pause_button.grid(row=0, column=3,padx=10)
stop_button.grid(row=0, column=4,padx=10)
#создадим меню
my_menu=Menu(root)
root.config(menu=my_menu)

#меню для добавления одной песни
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label = "Добавить песню", menu=add_song_menu)
add_song_menu.add_command(label='Добавить одну песню', command=add_song)

#меню для добавления нескольких песен
add_song_menu.add_command(label = "Добавить несколько песен", command=add_songs)

#меню для удалении одной или нескольких песен
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Удалить песни", menu=remove_song_menu)
remove_song_menu.add_command(label="Удалить песню из плейлиста", command=delete_song)
remove_song_menu.add_command(label="Удалить все песни из плейлиста", command=delete_all_songs)

#создает строку для визуализации продолжительности песен
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

#создает ползунок положения песен
my_slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360)
my_slider.grid(row=2, column=0, pady=10)

#создает ползунок громкости
volume_slider = ttk.Scale(volume_frame, from_= 0, to = 1, orient= VERTICAL, value = 1, command = volume, length = 120)
volume_slider.pack(pady=8)

root.mainloop()