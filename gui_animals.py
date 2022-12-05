from tkinter import *
from tkinter import filedialog
import animals
import live_tracking
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib import cm

'''
This file contains the Graphic-User Interface developed to perform animal
tracking on video.

This video may be either a live video feed or a previously recorded video.
Once the tracking process is finished, it is possible to open the trajectory
file and plot the data. The left plot is the time evolution of the trajectory.
The right plot is a 2D histogram that shows the number of data points in each
xy coordinate combination.

IMPORTANT: It is important to point out that either form of video must show
only the region where the animal is allowed to move. Walls, the floor or any
object that is not related to the experiment must not be on video. The 
boundaries of the video feed must be the boundaries of the area the animal
is allowed to move in.

Also, there are three quantities that can be computed: the animal's total
displacement, the amount of time it spent inside the squared/rectangular 
region bounded by x1,x2,y1 and y2 and the amount of time spent by the animal
outside a region of the same kind.

These last two regions might be different, i.e., the user may want to compute
the time spent by the animal in the center of a box and on its borders without
considering the borders to be the space that is not considered the center.
However, if the user actually wants to compute the time spent inside and 
outside the same region, the regions are the same and the arguments for both
functions are equal.

The arguments x1, x2, y1 and y2 must be floats. To get these values, use
a ruler or a similar object to measure the xy coordinates of each corner that
delimits the squared/rectangular region you are interested in. The x1 and y1
coordinates are the coordinates of the corner that is closest to the origin
placed on the top left corner of the screen. The x2 and y2 coordinates are
mapped to the region's corner that is diagonal to x1 and y1 and,
therefore, they describe the region's corner that is further away from the origin.

To perform the tracking on a live video feed, the user should use the
`Cam Test` feature by filling the input field to the right of the 
corresponding button with integer values starting from zero. To begin,
insert the number zero and press the `Cam Test` button. If a live video feed
pops up on the screen, the number zero is the `cam code` that maps the
tracking algorithm to your camera. To close the window showing the
live video, press `q` on the keyboard. However, if the live video does not
pop up, it means the user should try another integer such as the number one.
This is quite useful if the user has more than one camera and needs to map
the tracking algorithm to a specific video source.

HOW TO TRACK THE ANIMAL: 

To actually track the object of interest and extract its xy coordinates,
the user must fill the following input fields where the arguments must
be separated by commas:

  Insert live/rec, cam code(int)/video path, file name:
    live = track on live video feed
    rec = track on previously recorded video
    cam code = the code of the camera that will be used to perform live tracking
    video path = the full path of the previously recorded video
    file name = the name of the .txt file where the xy coordinates will be saved
        + the name of the .mp4 video where the tracking process will be stored
        .... if a full path is provided, both the txt and mp4 files will
             be saved in that path
      
  Insert object's width,height: (must be provided wether tracking live or on video)
    width = the largest measurement of the animal as float in centimeters
    height = the other measurement as float in centimeters
    .... the unit of measurement provided by the user determines the
         unit the xy data stored will be in

Once these steps are finished, the `Track!` button must be pressed to track!

HOW TO COMPUTE THE FEATURES OF INTEREST: 

First, open the .txt file by clicking the `Open File` button, find
the corresponding file and open it as usual.
To compute the Displacement, Time on site (the time spent inside
the squared/rectangular region) and Time outside site (the time 
spent outside the squared/rectangular region), the user must
check the corresponding boxes to the left of the calculation of
interest. It is possible to compute all features at once or separately.

To compute the Displacement, only check its box and hit `Compute`.
To compute the Time on site/outside site or both, fill the
corresponding input fields with the proper information, check the boxes
and hit `Compute`.

note: The order of the results will always be (Displacement, Time on site,
Time ouside site), no matter in what order the user checked the boxes. 

To CLEAR the numerical results, press the `Clear` button. Also, if the user
checked one box, computed its feature and then decided to compute another,
press the `Clear` button select only the feature to be computed.
'''




root = Tk()
root.title('TrajPy Animals GUI')
root.geometry('600x500')
root.resizable(False, False)




results = []
features = []
global file_variables



def track_function():
    number_variables = number_entry.get().split(',')
    file_variables = file_entry.get().split(',')
    #video_variables = video_entry.get().split(',')
    if file_variables[0] == 'live':
        live_tracking.capture(str(file_variables[0]),
                              int(file_variables[1]),
                              file_variables[2],
                              float(number_variables[0]),
                              float(number_variables[1]))
    elif file_variables[0] == 'rec':
        live_tracking.capture(str(file_variables[0]),
                              str(file_variables[1]),
                              file_variables[2],
                              float(number_variables[0]),
                              float(number_variables[1]))

def test_function():
    import cv2
    test_variables = test_entry.get()
    cap = cv2.VideoCapture(int(test_variables))
    while(True):
        ret, frame = cap.read()
        if not ret:
            break
        stop_text = 'Press "q" to stop'
        cv2.putText(frame,stop_text,(50,50),cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)
        cv2.line(frame,(0,0),(511,0),(255,0,0),5)
        cv2.line(frame,(0,0),(0,511),(255,0,0),5)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


def open_function():
   root.filename = filedialog.askopenfilename(parent=root,
   initialdir='/'
   ,title='Please select a file')

def add_var1():
    if var1.get() == 'On':
        features.append('Displacement')
    elif var1.get() == 'Off':
        features.remove('Displacement')

def add_var2():
    if var2.get() == 'On':
        features.append('Center')
    elif var2.get() == 'Off':
        features.remove('Center')

def add_var3():
    if var3.get() == 'On':
        features.append('Edges')
    elif var3.get() == 'Off':
        features.remove('Edges')

def compute_function():
    global label1
    if "Displacement" in features:
        results.append(animals.displacement(root.filename) + 'cm')

    if 'Center' in features:
        center_variables = center_entry.get().split(',')
        results.append(animals.time_center(float(center_variables[0]),
                       float(center_variables[1]),
                       float(center_variables[2]),
                       float(center_variables[3]),
                       root.filename) + 's')

    if 'Edges' in features:
        edges_variables = edges_entry.get().split(',')
        results.append(animals.time_edges(float(edges_variables[0]),
                      float(edges_variables[1]),
                      float(edges_variables[2]),
                      float(edges_variables[3]),
                      root.filename) + 's')

    label1 = Label(root,text=', '.join(results),font=('Helvetica 20'),background='white')
    label1.place(x=12,y=450)

def clear_function():
    results.clear()
    label1.destroy()
    

def plot_function():
    data = np.loadtxt(root.filename,delimiter=',')
    x = data[:,1]
    y = data[:,2]
    time = data[:,0]/60.0
    plt.figure(dpi=150)
    plt.subplot(121)
    points = np.array([x, y]).T.reshape(-1,1,2)
    segments = np.concatenate([points[:-2],points[1:-1], points[2:]], axis=1)
    lc = LineCollection(segments, cmap=cm.jet, linewidth=3)
    lc.set_array(time)
    plt.gca().add_collection(lc)
    plt.gca().autoscale()
    cbar = plt.colorbar(lc,orientation="horizontal")
    cbar.set_label(r'$t~$[min]',fontsize=16)
    plt.xlabel(r'$x~$[cm]',fontsize=16)
    plt.ylabel(r'$y~$[cm]',fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    plt.subplot(122)
    plt.hist2d(x, y, bins=(40,40),cmap='jet')
    plt.xlabel(r'$x~$[cm]',fontsize=16)
    plt.ylabel(r'$y~$[cm]',fontsize=16)
    cb = plt.colorbar(orientation="horizontal")
    cb.set_label('Number of occurrences',fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.tight_layout()
    plt.show()
    


title_label = Label(root, text="TrajPy", font=("Arial Bold", 35))
title_label.place(x=230,y=0)
version_label = Label(root, text="Animal Tracking", font=("Arial Bold", 10))
version_label.place(x=247,y=50)

track_button = Button(root,text='Track!',command=track_function,font=('Arial',20))
track_button.place(x=10,y=70)

test_button = Button(root,text='Cam Test',command=test_function,font=('Arial',20))
test_button.place(x=150,y=70)

test_label = Label(root,text='Insert 0,1,...',font=('Helvetica 12 bold'))
test_label.place(x=295,y=65)

test_entry = Entry(root,width=10,font=('Arial',12))
test_entry.insert(0,"Insert 0,1,...")
test_entry.place(x=295,y=85)



open_button = Button(root,text='Open File',
                     command=open_function,
                     font=('Arial',20))
open_button.place(x=400,y=70)

first_label = Label(root,text='Insert live/rec, cam code(int)/video path, file name',
                    font=('Helvetica 16'))
first_label.place(x=12,y=120)

file_entry = Entry(root,width=63,font=('Arial',12))
file_entry.insert(0,"Insert live/rec, cam code(int)/video path, file name")
file_entry.place(x=10,y=150)

second_label = Label(root,text="Insert object's width,height",font=('Helvetica 16'))
second_label.place(x=12,y=180)

number_entry = Entry(root,width=63,font=('Arial',12))
number_entry.place(x=10,y=210)
number_entry.insert(0,"Insert object's width,height")

third_label = Label(root,text="Insert site corners for t inside(x1,x2,y1,y2)",font=('Helvetica 16'))
third_label.place(x=12,y=240)

center_entry = Entry(root,width=63,font=('Arial',12))
center_entry.place(x=10,y=270)
center_entry.insert(0,"Insert site corners for t inside(x1,x2,y1,y2)")

fourth_label = Label(root,text="Insert site corners for t ouside(x1,x2,y1,y2)",font=('Helvetica 16'))
fourth_label.place(x=12,y=300)

edges_entry = Entry(root,width=63,font=('Arial',12))
edges_entry.place(x=10,y=330)
edges_entry.insert(0,"Insert site corners for t ouside(x1,x2,y1,y2)")

var1 = StringVar()
var2 = StringVar()
var3 = StringVar()

box1 = Checkbutton(root,text='Displacement',
                   variable=var1,onvalue='On',
                   offvalue='Off',
                   command=add_var1,
                   font=('Arial',16))
box1.deselect()
box1.place(x=10,y=360)

box2 = Checkbutton(root,text='Time on site',
                   variable=var2,onvalue='On',
                   offvalue='Off',
                   command=add_var2,
                   font=('Arial',16))
box2.deselect()
box2.place(x=200,y=360)

box3 = Checkbutton(root,text='Time ouside site',
                   variable=var3,
                   onvalue='On',
                   offvalue='Off',
                   command=add_var3,
                   font=('Arial',16))
box3.deselect()
box3.place(x=350,y=360)

compute_button = Button(root,text='Compute',
                        command=compute_function,
                        font=('Arial',20))
compute_button.place(x=20,y=390)

clear_button = Button(root,text='Clear',
                      command=clear_function,
                      font=('Arial',20))
clear_button.place(x=220,y=390)

plot_button = Button(root,text='Plot',
                     command=plot_function,
                     font=('Arial',20))
plot_button.place(x=430,y=390)


root.mainloop()
