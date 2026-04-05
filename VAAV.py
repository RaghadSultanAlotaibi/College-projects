import tkinter as tk
from tkinter import filedialog, messagebox
import hashlib
import json
import base64
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from PIL import Image, ImageTk


# File hashing 

def hash_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(4096):
            h.update(chunk)
    return h.hexdigest()



# Publisher Section

def generate_signature(video_path, result_label):
    if not video_path.get():
        messagebox.showerror("Error", "Please select a video file.")
        return

    key = RSA.generate(2048)
    private_key = key
    public_key = key.publickey()

    with open("public.pem", "wb") as f:
        f.write(public_key.export_key())

    vhash = hash_file(video_path.get())
    combined_hash = SHA256.new(vhash.encode())
    signature = pkcs1_15.new(private_key).sign(combined_hash)
    sig_b64 = base64.b64encode(signature).decode()

    record = {"video_hash": vhash, "signature": sig_b64}
    with open("signature_record.json", "w") as f:
        json.dump(record, f, indent=4)

    result_label.config(text=" Signature generated successfully",
                        bg="white", fg="#212121")



# Verify Section

def verify_signature(video_path, result_label):
    if not video_path.get():
        messagebox.showerror("Error", "Select a video file first.")
        return

    try:
        with open("public.pem", "rb") as f:
            public_key = RSA.import_key(f.read())

        with open("signature_record.json", "r") as f:
            record = json.load(f)

        recv_vhash = hash_file(video_path.get())
        combined_hash = SHA256.new(recv_vhash.encode())
        signature = base64.b64decode(record["signature"])

        pkcs1_15.new(public_key).verify(combined_hash, signature)

        result_label.config(text="✔ Video is ORIGINAL",
                            bg="white", fg="#212121")
    except:
        result_label.config(text="✖ Video has been MODIFIED",
                            bg="white", fg="#B71C1C")



# UI Interface

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Video & Audio Authenticity Verification")
        self.geometry("430x700")
        self.configure(bg="#ECEFF1")  

        self.container = tk.Frame(self, bg="#ECEFF1")
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (StartPage, PublisherPage, VerifyPage):
            frame = F(parent=self.container, controller=self)
            self.frames[F] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)

        self.show_frame(StartPage)

    def show_frame(self, page):
        self.frames[page].tkraise()



# Start Page

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#ECEFF1")

        header = tk.Frame(self, bg="white", height=200)  
        header.pack(fill="x")

        # Logo
        logo_img = Image.open("Logo.jpeg")
        logo_img = logo_img.resize((250, 250))
        self.logo = ImageTk.PhotoImage(logo_img)
        tk.Label(header, image=self.logo, bg="white").pack(pady=10)

        tk.Button(self, text="Start",
                  bg="#9E9E9E", fg="white",
                  font=("Helvetica", 16, "bold"),
                  width=15, height=2,
                  command=lambda: controller.show_frame(PublisherPage)
                  ).pack(pady=70)



# Page 2: Publisher page

class PublisherPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#ECEFF1")

        header = tk.Frame(self, bg="#CFD8DC", height=140)  
        header.pack(fill="x")
        tk.Label(header, text="📁 Publisher",
                 bg="#CFD8DC", font=("Helvetica", 22, "bold")).pack(pady=50)

        self.video_path = tk.StringVar()

        card1 = tk.Frame(self, bg="white", bd=1, relief="solid")  
        card1.place(relx=0.5, rely=0.32, anchor="center", width=330, height=130)

        tk.Label(card1, text="Choose Video File", bg="white",
                 font=("Helvetica", 12, "bold")).pack(pady=5)

        tk.Button(card1, text="Select Video",
                  bg="#90A4AE", fg="white", font=("Helvetica", 11, "bold"),
                  command=lambda: self.video_path.set(filedialog.askopenfilename())
                  ).pack(pady=8)

        tk.Label(card1, textvariable=self.video_path, bg="white", wraplength=260).pack()

        self.result_box = tk.Label(self, text="", bg="white", fg="black",
                                   font=("Helvetica", 13, "bold"),
                                   bd=2, relief="ridge", width=30, height=3)
        self.result_box.place(relx=0.5, rely=0.62, anchor="center")

        tk.Button(self, text="Generate Signature",
                  bg="#607D8B", fg="white",
                  font=("Helvetica", 14, "bold"),
                  command=lambda: generate_signature(self.video_path, self.result_box)
                  ).place(relx=0.5, rely=0.50, anchor="center")

        tk.Button(self, text="Back", bg="#B0BEC5",
                  command=lambda: controller.show_frame(StartPage)
                  ).place(x=20, y=650)

        tk.Button(self, text="Next", bg="#B0BEC5",
                  command=lambda: controller.show_frame(VerifyPage)
                  ).place(x=360, y=650)



# Page 3: Verify page

class VerifyPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#ECEFF1")

        header = tk.Frame(self, bg="#CFD8DC", height=140)
        header.pack(fill="x")
        tk.Label(header, text="🔐 Verify Video",
                 bg="#CFD8DC", font=("Helvetica", 22, "bold")).pack(pady=50)

        self.vpath = tk.StringVar()

        video_card = tk.Frame(self, bg="white", bd=1, relief="solid")  
        video_card.place(relx=0.5, rely=0.32, anchor="center", width=330, height=130)

        tk.Label(video_card, text="Select Video to Verify", bg="white",
                 font=("Helvetica", 12, "bold")).pack(pady=5)

        tk.Button(video_card, text="Choose Video",
                  bg="#90A4AE", fg="white", font=("Helvetica", 11, "bold"),
                  command=lambda: self.vpath.set(filedialog.askopenfilename())
                  ).pack(pady=8)

        tk.Label(video_card, textvariable=self.vpath, bg="white", wraplength=260).pack()

        self.result_box = tk.Label(self, text="", bg="white", fg="black",
                                   font=("Helvetica", 13, "bold"),
                                   bd=2, relief="ridge", width=30, height=3)
        self.result_box.place(relx=0.5, rely=0.65, anchor="center")

        tk.Button(self, text="Verify",
                  bg="#607D8B", fg="white",
                  font=("Helvetica", 14, "bold"),
                  command=lambda: verify_signature(self.vpath, self.result_box)
                  ).place(relx=0.5, rely=0.53, anchor="center")

        tk.Button(self, text="Back", bg="#B0BEC5",
                  command=lambda: controller.show_frame(PublisherPage)
                  ).place(x=20, y=650)

        tk.Button(self, text="Home", bg="#B0BEC5",
                  command=lambda: controller.show_frame(StartPage)
                  ).place(x=360, y=650)



# Run

app = App()
app.mainloop()
