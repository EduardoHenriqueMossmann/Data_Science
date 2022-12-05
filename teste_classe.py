from tkinter import *
from tkinter import filedialog
import animals
import live_tracking
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib import cm
import os

print("Tcl Version: {}".format(Tcl().eval('info patchlevel')))
class trajpy_animals_gui:
    
    def __init__(self, master):
        self.app = master
        self.init_window()
        self.app.resizable(False, False)

        self.title_label = Label(self.app, text="TrajPy",font=("Arial Bold", 35)) #title label
        self.version_label = Label(self.app, text="Animal Tracking", font=("Arial Bold", 10)) #version label
        self.test_label = Label(self.app,text='Insert 0,1,...',font=('Helvetica 12 bold')) #test label
        self.first_label = Label(self.app,text='Insert live/rec, cam code(int)/video path, file name',font=('Helvetica 16'))# first label
        self.second_label = Label(self.app,text="Insert object's width,height",font=('Helvetica 16'))#second label
        self.third_label = Label(self.app,text="Insert site corners for t inside(x1,x2,y1,y2)",font=('Helvetica 16'))#third label
        self.fourth_label = Label(self.app,text="Insert site corners for t ouside(x1,x2,y1,y2)",font=('Helvetica 16'))#fourth label

        self.test_entry = Entry(self.app,width=10,font=('Arial',12)) #test_entry
        self.test_entry.insert(0, "Insert 0,1,...")
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.file_entry = Entry(self.app,width=63,font=('Arial',12)) #file entry
        self.file_entry.insert(0,"Insert live/rec, cam code(int)/video path, file name")
        self.number_entry = Entry(self.app,width=63,font=('Arial',12)) #number entry
        self.number_entry.insert(0,"Insert object's width,height")
        self.center_entry = Entry(self.app,width=63,font=('Arial',12)) #center_entry
        self.center_entry.insert(0,"Insert site corners for t inside(x1,x2,y1,y2)")
        self.edges_entry = Entry(self.app,width=63,font=('Arial',12)) #edges_entry
        self.edges_entry.insert(0,"Insert site corners for t ouside(x1,x2,y1,y2)")
        self.results = Entry(self.app, width=60, highlightcolor='blue')


        self.track_button = Button(self.app,text='Track!',command=self.track_function,font=('Arial',20)) #track button
        self.test_button = Button(self.app,text='Cam Test',command=self.test_function,font=('Arial',20)) #test button
        self.open_button = Button(self.app,text='Open File',command=self.open_function,font=('Arial',20)) #open button
        self.compute_button = Button(self.app,text='Compute',command=self.compute_selected,font=('Arial',20)) #compute button
        self.clear_button = Button(self.app,text='Clear',command=self.clear_function,font=('Arial',20)) #clear button
        self.plot_button = Button(self.app,text='Plot',command=self.plot_function,font=('Arial',20)) #plot button

     
        self.features = ['Displacement','Time on site','Time outside site']
        self.feats_ = {}
        self.selected_features = []
        self.data = {}
        for feature in self.features:
            self.feats_[feature] = Checkbutton(self.app, text=feature,font=('Arial',16))
        
        self.placement()


    def init_window(self):
        self.app.title('TrajPy Animals GUI')
        self.app.geometry('600x500')

    def placement(self):
        self.title_label.place(x=230,y=0)
        self.version_label.place(x=247,y=50)
        self.test_label.place(x=295,y=65)
        self.first_label.place(x=12,y=120)
        self.second_label.place(x=12,y=180)
        self.third_label.place(x=12,y=240)
        self.fourth_label.place(x=12,y=300)

        self.track_button.place(x=10,y=70)
        self.test_button.place(x=150,y=70)
        self.open_button.place(x=400,y=70)
        self.compute_button.place(x=20,y=390)
        self.clear_button.place(x=220,y=390)
        self.plot_button.place(x=430,y=390)

        self.test_entry.place(x=295,y=85)
        self.file_entry.place(x=10,y=150)
        self.number_entry.place(x=10,y=210)
        self.center_entry.place(x=10,y=270)
        self.edges_entry.place(x=10,y=330)
        self.results.place(x=20, y=450)
        for n, button in enumerate(self.feats_):
            self.feats_[button].configure(command=(self.select_feat, self.feats_[button]))
            self.feats_[button].place(x=10+ n * 170, y=360 )




    def track_function(self):
        number_variables = self.number_entry.get().split(',')
        file_variables = self.file_entry.get().split(',')
        if file_variables[0] == 'live':
            live_tracking.capture(str(file_variables[0]),int(file_variables[1]),file_variables[2],float(number_variables[0]),float(number_variables[1]))
        elif file_variables[0] == 'rec':
            live_tracking.capture(str(file_variables[0]),str(file_variables[1]),file_variables[2],float(number_variables[0]),float(number_variables[1]))

    def test_function(self):
        import cv2
        test_variables = self.test_entry.get()
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

    def open_function(self):
        self.filename = filedialog.askopenfilename(parent=self.app,
        initialdir=self.path
        ,title='Please select a file')

    
    def compute_selected(self):
        self.data = {}
        if any('Displacement' in feature for feature in self.selected_features):
            self.data['displacement'] = str(animals.displacement(self.filename))

        if any('Time on site' in feature for feature in self.selected_features):
            center_variables = self.center_entry.get().split(',')
            self.data['time on site'] = str(animals.time_center(float(center_variables[0]),
                                        float(center_variables[1]),float(center_variables[2])
                                        ,float(center_variables[3]),self.filename))

        if any('Time outside site' in feature for feature in self.selected_features):
            edges_variables = self.edges_entry.get().split(',')
            self.data['time outside site'] = str(animals.time_edges(float(edges_variables[0]),
                                            float(edges_variables[1]),float(edges_variables[2])
                                            ,float(edges_variables[3]),self.filename))
        
        self.results.delete(0, 'end')
        self.results.insert(0, ','.join(self.data.values()))

    def select_feat(self, button):
        if any(button.cget('text') in feature for feature in self.selected_features):
            self.selected_features.remove(button.cget('text'))
            button.deselect()
        else:
            self.selected_features.append(button.cget('text'))
            button.select()

    def clear_function(self):
        self.results.insert(0,'')        

    def plot_function(self):
        data = np.loadtxt(self.filename,delimiter=',')
        x = data[:,1]
        y = data[:,2]
        time = data[:,0]/60.0
        plt.figure(dpi=150)
        plt.subplot(121)
        points = np.array([x, y]).T.reshape(-1,1,2)
        segments = np.concatenate([points[:-2],points[1:-1], points[2:]], axis=1)
        lc = LineCollection(segments, cmap=cm.viridis, linewidth=3)
        lc.set_array(time)
        plt.gca().add_collection(lc)
        plt.gca().autoscale()
        cbar = plt.colorbar(lc,orientation="horizontal")
        cbar.set_label(r'$t~$[min]',fontsize=12)
        plt.xlabel(r'$x~$[cm',fontsize=12)
        plt.ylabel(r'$y~$[cm]',fontsize=12)
        

        plt.subplot(122)
        plt.hist2d(x, y, bins=25,cmap='Blues')
        plt.xlabel(r'$x~$[cm]',fontsize=12)
        plt.ylabel(r'$y~$[cm]',fontsize=12)
        cb = plt.colorbar(orientation="horizontal")
        cb.set_label('Number of occurrences')
        plt.tight_layout()
        plt.show()
    










if __name__ == '__main__':
    root = Tk()
    tj_AGui = trajpy_animals_gui(root)
    root.mainloop()