from tkinter import Tk, Label, Message
from PIL import Image, ImageTk

def message_to_display(response: str, image_str: bool):
    root = Tk()
    root.geometry("800x400")
    root.configure(background="#F9E8C9")
    root.iconbitmap("resources/favicon.ico")
    root.title('Haibo Assistant')

    title_label = Label(root, text='Haibo', font=("Helvetica", 40), background="#F9E8C9", fg="#201658")
    title_label.pack(pady=10)

    if image_str:
        msg = Message(root, text=response, font=("Helvetica", 16), width=250, borderwidth=16, fg="#201658")
        msg.pack(side="left", padx=10, pady=10)
        img = ImageTk.PhotoImage(Image.open("./resources/Image_to_analyze.jpg"))
        panel = Label(root, image=img, width=550)
        panel.image = img  # Keep a reference to the image to prevent garbage collection
        panel.pack(side="right", padx=10, pady=10)
    else:
        msg = Message(root, text=response, font=("Helvetica", 16), width=600, borderwidth=16, fg="#201658")
        msg.pack(fill="both", padx=50, pady=50)

    root.mainloop()
