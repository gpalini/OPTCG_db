from tkinter import *
from PIL import ImageTk, Image


def handle_it(img_no):
    global label
    global button_forward
    global button_back
    global button_exit
    label.grid_forget()

    if img_no == len(List_images) - 2:
        button_forward = Button(root, text="Forward", state=DISABLED)
    else:
        button_forward = Button(root, text="Forward", command=lambda: handle_it(img_no + 1))

    if img_no == -1:
        button_back = Button(root, text="Back", state=DISABLED)
    else:
        button_back = Button(root, text="Back", command=lambda: handle_it(img_no - 1))

    label = Label(image=List_images[img_no + 1])
    label.grid(row=1, column=0, columnspan=3)

    button_back.grid(row=5, column=0)
    button_exit.grid(row=5, column=1)
    button_forward.grid(row=5, column=2)

# Calling the Tk (The initial constructor of tkinter)
root = Tk()

# We will make the title of our app as Image Viewer
root.title("Image Viewer")

# The geometry of the box which will be displayed
# on the screen
root.geometry("1200x800")

# Adding the images using the pillow module which
# has a class ImageTk We can directly add the
# photos in the tkinter folder or we have to
# give a proper path for the images
image_no_1 = ImageTk.PhotoImage(Image.open("Screenshot (2).png"))
image_no_2 = ImageTk.PhotoImage(Image.open("Screenshot (1).png"))
image_no_3 = ImageTk.PhotoImage(Image.open("Screenshot (2).png"))

# List of the images so that we traverse the list
List_images = [image_no_1, image_no_2, image_no_3]

label = Label(image=image_no_1)

# We have to show the box so this below line is needed
label.grid(row=1, column=0, columnspan=3)

# We will have three button back ,forward and exit
button_back = Button(root, text="Back", state=DISABLED)

# root.quit for closing the app
button_exit = Button(root, text="Exit",
                     command=root.quit)

button_forward = Button(root, text="Forward",
                        command=lambda: handle_it(0))

# grid function is for placing the buttons in the frame
button_back.grid(row=5, column=0)
button_exit.grid(row=5, column=1)
button_forward.grid(row=5, column=2)

root.mainloop()
