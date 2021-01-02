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

#initializing tkinter
root = Tk()
#giving title to the window
root.title("Music App")
#setting icon of the window
imgc = PhotoImage(file='images/icon.gif')
root.tk.call('wm', 'iconphoto', root._w, imgc)

#size of the window)
root.geometry("1920x1080")
#pygame mixer
pygame.mixer.init()
#variable for pause function
paused = False
#the empty list in which we will append the list
#of all song which are stored in the binary file
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

#function for removing song from the binary file
def rmsong(choice):
   
    print(choice)
    with open("mydata.dat", "rb") as reader, open("temp.dat", "wb") as writer:
        found = False
        try:
            while True:
                rec = pickle.load(reader)
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
#function for reading the binary file and putting songs in the playlist
def initialize():
    global l
    with open("mydata.dat", "rb") as reader:
        print("The file data is as follows : ")
        try:
            while True:
                rec = pickle.load(reader)
                f = rec[0]
                playlist.insert(END, f)
        except EOFError:
            pass
#appending the music urls in the empty list "l"
def readlist():
    global l
    with open("mydata.dat", "rb") as reader:
        try:
            # Keep repeating
            while True:
                rec = pickle.load(reader)
                data = rec[0]
                l.append(data)
        except EOFError:
            pass

#function for writing the song's path which
#was currently added to the playlist (listbox)
def savelist(x):
    with open("mydata.dat", "ab")as writer:
        rec = [x]
        pickle.dump(rec, writer)

def playtime():
    #this if statement checks if the song has stopped then it
    #stops the slider from moving on its own
    if stopped:
        return
    #currenttime gets the time on which the slider is currently positioned
    currenttime = pygame.mixer.music.get_pos()/1000
    #timeconv stores converted current time which is in minute and second format
    timeconv = time.strftime('%M:%S',time.gmtime(currenttime))
    #current_song gets the currently playing/selected song
    current_song = playlist.curselection()
    #song gets the address location of the current_song
    song = playlist.get(current_song)
    songimp = MP3(song)
    #songlen is the length of the song
    global songlen
    songlen = songimp.info.length
    #csonglen is converted songlen in minute:second format
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
#function for adding the song and saving it in binary file and inserting it in
#playlist listbox
def addsong():
    song = filedialog.askopenfilename(initialdir="./")
    savelist(song)
    readlist()
    playlist.insert(END, song)  
   
#function which deletes the song from the playlist and calls
#rmsong from deleting the song from binary file
def delsong():
    #it first stops the song
    stop(2)
    #then deletes it
    choice = playlist.get(ACTIVE)
    playlist.delete(ANCHOR)
    dsong = playlist.get(ACTIVE)
    pygame.mixer.music.stop()
    #calling the rmsong function to delete the music also from the binary file
    rmsong(choice)
#function to delete all the songs from the playlist
def deleteallsong():
    stop(2)
    playlist.delete(0,END)
    pygame.mixer.music.stop()
    with open("mydata.dat", "wb") as writer:
        pass
#function which plays the currently selected song and
#displays it's name in the entry box
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
    try:
        audio = ID3(path) #path: path to file
        track = audio["TIT2"].text[0] #Track
        entry.delete(0,END)
        entry.insert(0,str(track))
    except:
        print("the audio file doesn't have any meta deta")
    print(song)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    playtime()

global stopped
stopped = False
#function which stops the music from playing
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
def p(event):
   global paused
   pause(paused)

global count
count = 0
#function which changes play button to pause button
def btnchange(event):
    global count
    global b
    global f
    if count==0:
        c.tag_bind(a,"<Button-1>",play)
    else:
        c.tag_bind(b,"<Button-1>",p)
        c.itemconfig(f,image=pause)
    count+=1
    print(count)

#function which plays the next song in the list
def nextsong(event):
    status.config(text="")
    slider.config(value=0)
    #gets the index of currently playing song
    next_song = playlist.curselection()
    #increments it by one so we get the next song which we want to play
    next_song = next_song[0]+1
    #song contains the address of the song
    song = playlist.get(next_song)
##    song  = f'F:/{song}.mp3'
    #plays the song using pygame
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    #makes the next song get selected
    playlist.selection_clear(0,END)
    playlist.activate(next_song)
    playlist.selection_set(next_song,last=None)
    path = '{}'.format(song)
    print(path)
    #changes the entrybox text to the name of the song
    try:
        audio = ID3(path) #path: path to file
        track = audio["TIT2"].text[0] #Track
        entry.delete(0,END)
        entry.insert(0,str(track))
    except:
        print("the audio file doesn't have any meta deta")
#function which plays the previous song
def prev(event):
    #clears the timeline and sets it to 0
    status.config(text="")
    slider.config(value=0)
    #gets the index of current song playing
    prev_song = playlist.curselection()
    #decrement it by 1 so that we get the previous song
    prev_song = prev_song[0]-1
    #song variable contains the address of the previous song
    song = playlist.get(prev_song)
##    song  = f'F:/{song}.mp3'
    #plays the previous song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    #selects the previous song
    playlist.selection_clear(0,END)
    playlist.activate(prev_song)
    playlist.selection_set(prev_song,last=None)
    path = '{}'.format(song)
    print(path)
    #displays the name of the previous song which is to be played
    try:
        audio = ID3(path) #path: path to file
        track = audio["TIT2"].text[0] #Track
        entry.delete(0,END)
        entry.insert(0,str(track))
    except:
        print("the audio file doesn't have any meta deta")
   
#function which is responsible for setting the volume of the music playing
def volume(x):
    pygame.mixer.music.set_volume(volumeslider.get())
#functions which takes care of the slider which shows the time at which song is currently at
def slide(x):
    global songlen
    song = playlist.get(ACTIVE)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0,start=int(slider.get()))
#function which is called when we close the music app
def exit_app():
    #opens a messagebox to confirm the users choice, whether they want to close the app or not?
    global response
    response = messagebox.askyesno("Are you sure?","Are you sure you want to leave us? There is a whole party you'll be missing!!")
    Label(root, text=response).pack()
    #if we get yes which is response = 1 , then the app closes , else nothing happens
    if response == 1:
        root.destroy()
    else:
        pass

def help_():
    help_window = Toplevel()
    help_window.geometry("1045x255")
    help_window.title("Help window")
    help_window.iconbitmap("f:/Python/Tkinter/images/icon 1.ico")
    label = Label(help_window, text=''' To start using this app, the user first has to add a song to queue by either selecting the option of “Add a song” from the taskbar under “File” or by clicking the button “Add Song” from Menu frame.
After clicking this button, a window is opened which directs the user to his file directory where all the songs are stored and he can select a song accordingly.
This app also provides user with options: “Delete a song” to delete a single song from the song queue, and “Delete all songs” to delete all songs from the queue.
This app also includes the “Exit” button for the user to exit the party.
The song queue is displayed in the right frame under the title “Your Song Queue”.
This app also allows the user to control his music using the following buttons:
1) Play – The middlemost play button is used to play songs after they have been added into and selected from the song queue.
2) Pause – The pause button allows the user to pause a song and continue playing it.
3) Forward – The forward button allows the user to jump to the next song.
4) Backward – The backward button allows the user to jump to the previous song.
5) Stop – The stop button allows the user to stop the currently playing song.
The name of the song played in also displayed on the top.
This app also allows the user to control the volume of the songs using the volume slider.
Similarly, the user can also his song using the song slider which moves in accordance with the time of the song.
The time elapsed of the song is also displayed in the bottom right.''',bg="black", fg = "white").place(x=0,y=0)
    #Button to close the window
    but_closew = Button(help_window, text="Close", command=help_window.destroy, bg="black", fg="white").place(x=500, y=230)

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

#Help Menu
help_menu = Menu(menubar)
menubar.add_cascade(label="Help", menu = help_menu)
help_menu.add_command(label="Help", command=help_)
root.config(menu=menubar)


#Backgroung Image
img1 = ImageTk.PhotoImage(Image.open("images/img11.jpg"))
label = Label(root, image=img1, height=768, width=1366)
label.pack()

#Entry Frame
entry = Entry(root, borderwidth=5)
entry.place(x=200, y=10, width=1000, height=30)

##FRAMES

#Menu Frame
menu_frame = LabelFrame(root, text="Menu", padx = 10, pady = 10, height=690, width=150, font=('iCiel Gotham Medium',10), bg="#1c0e24", fg="#ff86a5")
menu_frame.place(x=0, y=0)
menu_frame.pack_propagate(0)
#Buttons in menu frame
btn_library = Button(menu_frame, text="Add  Song", bg="#ff517e", fg="white", command=addsong)
btn_library.place(x=30, y=0)

btn_queue = Button(menu_frame, text="Help", height=1, width=8, bg="#ff517e", fg="White")
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

#Slider
slider = ttk.Scale(c,from_= 0 , to = 100, orient=HORIZONTAL,value=0, command=slide, length=360)
slider.place(x=600 ,y=52)

#Volume Slider
volumeslider = ttk.Scale(c,from_= 0 , to = 1, orient=HORIZONTAL,value=1, command=volume,length=100)
volumeslider.place(x=1350 ,y=25)
#Status bar
status =  Label(root, text="",bd=1,relief=GROOVE,anchor=E)
status.pack(fill=X,side=BOTTOM,ipady=2)
root.mainloop() 
