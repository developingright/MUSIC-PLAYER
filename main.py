from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import font
import pygame
import time
from tkinter import filedialog
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
import tkinter.ttk as ttk
import pickle
import os

root = Tk()
root.title("Music App")
root.iconbitmap("../images/icon 1.ico")
root.geometry("1920x1080")

#pygame mixer
pygame.mixer.init()                        
paused = False
l = []

songlen = 0
def makefile():
    try:
        with open("mydata.dat","rb") as reader:
            print("file exists")
            pass
    except FileNotFoundError :
        with open("mydata.dat","wb")as writer:
            pass
makefile()
def rmsong(choice):    
    with open("mydata.dat", "rb") as reader, open("temp.dat", "wb") as writer:
        found = False
        try:
            while True:
                # Read one record from the file
                rec = pickle.load(reader)

                # If this is the record to delete
                if rec[0] == choice:
                    found = True
                else:
                    pickle.dump(rec, writer)
        except EOFError:
            pass
    os.remove("mydata.dat")
    os.rename("temp.dat", "mydata.dat")

    if found == False:
        print("No record for this name found")
    
def initialize():
    global l
    with open("mydata.dat", "rb") as reader:
        print("The file data is as follows : ")
        try:
            # Keep repeating
            while True:
                rec = pickle.load(reader)
                f = rec[0]
                playlist.insert(END, f)
        except EOFError:
            # EOFError will be raised when an attempt is made
            # to read beyond end of file.Dont do anything then.
            pass

def readlist():
    global l
    with open("mydata.dat", "rb") as reader:
        try:
            # Keep repeating
            while True:
                rec = pickle.load(reader)
                # Display the record
                data = rec[0]
                l.append(data)
        except EOFError:
            # EOFError will be raised when an attempt is made
            # to read beyond end of file.Dont do anything then.
            pass

def savelist(x):
    with open("mydata.dat", "ab")as writer:
        rec = [x]
        pickle.dump(rec, writer)

def playtime():
    if stopped:
        return
    currenttime = pygame.mixer.music.get_pos()/1000
##    sliderlabel.config(text=f'Slider: {int(slider.get())} and Song Pos: {int(currenttime)}')
    timeconv = time.strftime('%M:%S',time.gmtime(currenttime))
   
   
    current_song = playlist.curselection()
    song = playlist.get(current_song)

    songimp = MP3(song)
    global songlen
    songlen = songimp.info.length      
    csonglen = time.strftime('%M:%S',time.gmtime(songlen))
    currenttime+=1

    if int(slider.get())== int(currenttime):
        sliderpos = int(songlen)
        slider.config(to=sliderpos,value=int(currenttime))
       
    else:
        sliderpos = int(songlen)
        slider.config(to=sliderpos,value=int(slider.get()))
        timeconv = time.strftime('%M:%S',time.gmtime(slider.get()))
        status.config(text=f'Time Elapsed: {timeconv} of {csonglen}')
        ntime = int(slider.get()) +1
        slider.config(value=ntime)
    status.after(1000,playtime)
    if timeconv == csonglen:
        nextsong(2)

def addsong():
    song = filedialog.askopenfilename(initialdir="./")
    savelist(song)
    readlist()

    playlist.insert(END, song)  
   
   
def delsong():
    stop(2)
    choice = playlist.get(ACTIVE)
    playlist.delete(ANCHOR)
    dsong = playlist.get(ACTIVE)
    pygame.mixer.music.stop()
   
    rmsong(choice)
def deleteallsong():
    stop(2)
    playlist.delete(0,END)
    pygame.mixer.music.stop()
    choice = playlist.get(ACTIVE)
    rmsong(choice)
def play(event):
    next_song = playlist.curselection()
    stop(2)
    playlist.selection_clear(0,END)
    playlist.activate(next_song)
    playlist.selection_set(next_song,last=None)
    global stopped
    stopped=False
    global songlen
    song = playlist.get(ACTIVE)
    path = '{}'.format(song)
    print(path)
    audio = ID3(path) #path: path to file

    #print(audio['TPE1'].text[0]) #Artist
    # print(audio["TCON"].text[0])
    track = audio["TIT2"].text[0] #Track
    print(track)
    print(type(track))
    entry.delete(0,END)
    entry.insert(0,str(track))
    print(song)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    playtime()
global stopped
stopped = False
def stop(event):
    status.config(text="")
    slider.config(value=0)
    pygame.mixer.music.stop()
    playlist.selection_clear(ACTIVE)
    status.config(text="")

    global stopped
    stopped = True          

def pause(is_paused):
    global paused
    paused = is_paused
    if paused == False:
        pygame.mixer.music.pause()
        paused = True
    else:
        pygame.mixer.music.unpause()
        paused = False
##pauseb = Button(root,text="Pause",command=lambda: pause(paused))

def p(event):
   global paused
   pause(paused)

global count
count = 0

def btnchange(event):

    global count
    global b
    global f
    if count==0:
        c.tag_bind(a,"<Button-1>",play)
    else:
##        pause_btn=PhotoImage(file="images/new pause 2.gif")
##        b = c.create_image(756,8,image=pause_btn,anchor=NW)
        c.tag_bind(b,"<Button-1>",p)
        c.itemconfig(f,image=pause)
    count+=1
    print(count)


def nextsong(event):
    status.config(text="")
    slider.config(value=0)
    next_song = playlist.curselection()
    next_song = next_song[0]+1
    song = playlist.get(next_song)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    playlist.selection_clear(0,END)
    playlist.activate(next_song)
    playlist.selection_set(next_song,last=None)
    path = '{}'.format(song)
    print(path)
    try:
        audio = ID3(path) #path: path to file
        track = audio["TIT2"].text[0] #Track
        entry.delete(0,END)
        entry.insert(0,str(track))
    except:
        
    
   
def prev(event):
    status.config(text="")
    slider.config(value=0)
    prev_song = playlist.curselection()
    prev_song = prev_song[0]-1
    song = playlist.get(prev_song)
##    song  = f'F:/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    playlist.selection_clear(0,END)
    playlist.activate(prev_song)
    playlist.selection_set(prev_song,last=None)
    path = '{}'.format(song)
    print(path)
    audio = ID3(path) #path: path to file
    track = audio["TIT2"].text[0] #Track
    entry.delete(0,END)
    entry.insert(0,str(track))

def volume(x):
    pygame.mixer.music.set_volume(volumeslider.get())


def slide(x):
    global songlen
    song = playlist.get(ACTIVE)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0,start=int(slider.get()))

def exit_app():
    global response
    response = messagebox.askyesno("Are you sure?","Are you sure you want to leave us? There is a whole party you'll be missing!!")
    Label(root, text=response).pack()
    if response == 1:
        root.destroy()
    else:
        pass

#Menu
menubar = Menu(root)
#File Menu
file_menu = Menu(menubar)
menubar.add_cascade(label="File", menu = file_menu)
file_menu.add_command(label="Add a song", command=addsong)
file_menu.add_command(label="Delete a song", command=delsong)
file_menu.add_command(label="Delete all songs", command=deleteallsong)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)
##file_menu.add_command(label="Play a song", command=play)
##file_menu.add_command(label="Pause a song", command=p)
#file_menu.add_command(label="Play a song", command=play)
#Edit Menu
edit_menu = Menu(menubar)
menubar.add_cascade(label="Edit", menu = edit_menu)
edit_menu.add_command(label="Edit Playlist", command=None)
#Help Menu
help_menu = Menu(menubar)
menubar.add_cascade(label="Help", menu = help_menu)
root.config(menu=menubar)


#Backgroung Image

img1 = ImageTk.PhotoImage(Image.open("images/img11.jpg"))
label = Label(root, image=img1, height=768, width=1366)
label.pack()

#Entry Frame
entry = Entry(root, borderwidth=5)
entry.place(x=200, y=10, width=1000, height=30)

#FRAMES

#Menu Frame
menu_frame = LabelFrame(root, text="Menu", padx = 10, pady = 10, height=690, width=150, font=('iCiel Gotham Medium',10), bg="#1c0e24", fg="#ff86a5")
menu_frame.place(x=0, y=0)
menu_frame.pack_propagate(0)
#Buttons in menu frame
btn_library = Button(menu_frame, text="My Library", bg="#ff517e", fg="white")
btn_library.place(x=30, y=0)

btn_queue = Button(menu_frame, text="Queue", height=1, width=8, bg="#ff517e", fg="White")
btn_queue.place(x=30, y=25)

btn_exit = Button(menu_frame, text="Exit", height=1, width=8, bg="#ff517e", fg="White", font=('Hero',10,'bold'),command=exit_app)
btn_exit.place(x=30, y=600)

#Queue Frame
queue_frame = LabelFrame(root, text="Your Song Queue", padx=10, pady=10, height=690, width=300, font=('iCiel Gotham Medium',10), bg="#371e46", fg="#ff86a5")
queue_frame.place(x=1240, y=0)


playlist = Listbox(queue_frame,bg="#000000",fg="white",width="47", height="41", bd=0,selectbackground="grey")
playlist.place(x=0, y=0)
readlist()
initialize()

#Canvas music control

c = Canvas(root, height=150, width=1920, bg="#552e6d", highlightthickness=0)
c.place(x=0, y=690)
##play_btn = PhotoImage(file="images/new play 2.gif")
##a = c.create_image(756,8,image=play_btn,anchor=NW)
pause_btn=PhotoImage(file="images/new pause 2.gif")
b = c.create_image(810,8,image=pause_btn,anchor=NW)
play_btn = PhotoImage(file="images/new play 2.gif")
a = c.create_image(756,8,image=play_btn,anchor=NW)
stop_btn = PhotoImage(file="images/stop n 22.gif")
k = c.create_image(660,8,image=stop_btn,anchor=NW)
back_btn = PhotoImage(file="images/back 1.gif")
d = c.create_image(710,8,image=back_btn,anchor=NW)
forward_btn = PhotoImage(file="images/next.gif")
e = c.create_image(860,8,image=forward_btn,anchor=NW)
speaker = PhotoImage(file="images/speaker.gif")
f = c.create_image(1319,25,image=speaker,anchor=NW)

c.tag_bind(a,"<Button-1>",play)
c.tag_bind(b,"<Button-1>",p)
c.tag_bind(k,"<Button-1>",stop)
c.tag_bind(d,"<Button-1>",prev)
c.tag_bind(e,"<Button-1>",nextsong)

def play_img():
    gmail=PhotoImage(file="images/new pause 2.gif")
    g = c.create_image(756,38,image=gmail,anchor=NW, command=pause_img)

def pause_img():
    play = PhotoImage(file="images/new play 2.gif")
    b = c.create_image(756,38,image=play,anchor=NW, command=play_img)

slider = ttk.Scale(c,from_= 0 , to = 100, orient=HORIZONTAL,value=0, command=slide, length=360)
slider.place(x=600 ,y=52)

#Volume Slider
volumeslider = ttk.Scale(c,from_= 0 , to = 1, orient=HORIZONTAL,value=1, command=volume,length=100)
volumeslider.place(x=1350 ,y=25)


status =  Label(root, text="",bd=1,relief=GROOVE,anchor=E)
status.pack(fill=X,side=BOTTOM,ipady=2)


root.mainloop()
