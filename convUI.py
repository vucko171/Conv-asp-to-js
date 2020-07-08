from tkinter import *
from conv import convert 
master = Tk()
frame = Frame(master)
frame.pack(padx=50, pady=20)

lbl1 = Label(frame, text="ASP to HTML", width=60)
lbl1.pack(side=TOP, padx=5, pady=5)

e = Text(frame, width=30, height=10)
e.pack(in_=frame, side=LEFT)

e.focus_set()

def callback():
    e2.configure(state='normal')
    
    e2.delete(1.0,"end")
    e2.insert(1.0,"".join(convert([temp+"\n" for temp in e.get(1.0,'end-1c').split("\n") if temp],[4],[])))
    e2.configure(state='disabled')

b = Button(frame, text = "OK", width=10, height=10, command = callback)
b.pack(in_=frame, side=LEFT)

e2 = Text(frame, width=30, height=10)
e2.pack(in_=frame, side=LEFT)
e2.configure(state='disabled')

frame2 = Frame(master)
frame2.pack(padx=20, pady=20)

lbl2 = Label(frame2, text="ASP to JS", width=60)
lbl2.pack(side=TOP, padx=5, pady=5)



def onChange(*args):
    if e3.get(1.0,'end-1c')=="":
        e3.insert(1.0,"<%\n\n%>")
e3 = Text(frame2, width=30, height=10)
e3.insert(1.0,"<%\n\n%>")
e3.pack(in_=frame2, side=LEFT)
e3.bind('<KeyRelease>', onChange)

def callback2():
    e4.configure(state='normal')
    e4.delete(1.0,"end")
    e4.insert(1.0,"".join(convert([temp+"\n" for temp in e3.get(1.0,'end-1c').split("\n") if temp],[0,1,2,3,6],[6])))
    e4.configure(state='disabled')

b2 = Button(frame2, text = "OK", width=10, height=10, command = callback2)
b2.pack(in_=frame2, side=LEFT)

e4 = Text(frame2, width=30, height=10)
e4.pack(in_=frame2, side=LEFT)
e4.configure(state='disabled')

mainloop()