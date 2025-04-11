import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from datetime import datetime
from PIL import Image, ImageTk
import os

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="stefi",
    database="victoria_luxe"
)
cursor = db.cursor()

selected_branch = None
images = {}
logo_image = None  

def load_logo():
    global logo_image
    try:
        img = Image.open("logo.png").resize((150, 150), Image.LANCZOS)
        logo_image = ImageTk.PhotoImage(img)
    except Exception as e:
        messagebox.showerror("Logo Error", f"Failed to load logo: {e}")

def login():
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if username == "stefi" and password == "12345":
        messagebox.showinfo("Login Success", "Welcome to Victoria Luxe!")
        login_window.withdraw()
        open_branch_window()
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password")

def open_branch_window():
    global branch_window
    branch_window = tk.Toplevel(login_window)
    branch_window.title("Our Branches")
    branch_window.state('zoomed')
    branch_window.configure(bg="white")

    if logo_image:
        logo_label = tk.Label(branch_window, image=logo_image, bg="white")
        logo_label.place(relx=1.0, y=10, anchor="ne")
    tk.Label(branch_window, text="Select Your Branch", font=("Freestyle Script", 48, "bold"),
             fg="purple", bg="white").pack(pady=40)

    try:
        images["rome"] = ImageTk.PhotoImage(Image.open("black.jpeg").resize((350, 250), Image.LANCZOS))
        images["italy"] = ImageTk.PhotoImage(Image.open("white branch.jpeg").resize((350, 250), Image.LANCZOS))
    except Exception as e:
        messagebox.showerror("Error", f"Image loading failed: {e}")
        return

    branches_frame = tk.Frame(branch_window, bg="white")
    branches_frame.pack(pady=20)

    
    rome_frame = tk.Frame(branches_frame, bg="white", padx=50)
    rome_frame.grid(row=0, column=0, padx=20)
    tk.Label(rome_frame, text="Rome Branch", font=("Times New Roman", 24, "bold"), fg="purple", bg="white").pack()
    tk.Label(rome_frame, image=images["rome"], bg="white").pack(pady=10)
    tk.Label(rome_frame, text="Located in the heart of Rome, offering elegant gowns.", fg="purple", bg="white").pack()
    tk.Button(rome_frame, text="Select Rome", command=lambda: select_branch("Rome"),
              bg="purple", fg="white").pack(pady=10)

   
    italy_frame = tk.Frame(branches_frame, bg="white", padx=50)
    italy_frame.grid(row=0, column=1, padx=20)
    tk.Label(italy_frame, text="Italy Branch", font=("Times New Roman", 24, "bold"), fg="purple", bg="white").pack()
    tk.Label(italy_frame, image=images["italy"], bg="white").pack(pady=10)
    tk.Label(italy_frame, text="Exclusive boutique in Italy with luxury bridal collections.",
             fg="purple", bg="white").pack()
    tk.Button(italy_frame, text="Select Italy", command=lambda: select_branch("Italy"),
              bg="purple", fg="white").pack(pady=10)

def select_branch(branch):
    global selected_branch
    selected_branch = branch
    messagebox.showinfo("Branch Selected", f"You selected {branch} branch.")
    branch_window.destroy()
    open_booking_form()

def open_booking_form():
    global name_entry, contact_entry, date_entry, time_var, gown_var, message_box, booking_window

    booking_window = tk.Toplevel(login_window)
    booking_window.title(f"Victoria Luxe - {selected_branch} Booking")
    booking_window.state('zoomed')
    booking_window.configure(bg="white")

    if logo_image:
        logo_label = tk.Label(booking_window, image=logo_image, bg="white")
        logo_label.place(relx=1.0, y=10, anchor="ne")

    tk.Label(booking_window, text=f"VISIT US - {selected_branch} Branch", font=("Freestyle Script", 48, "bold"),
             fg="purple", bg="white").pack(pady=30)

    form_frame = tk.Frame(booking_window, bg="white")
    form_frame.pack(pady=20)

    def add_field(label_text, widget):
        tk.Label(form_frame, text=label_text, fg="purple", bg="white", font=("Arial", 14, "bold"),
                 anchor="w").pack(fill="x", padx=50, pady=(15, 5))
        widget.pack(padx=50, pady=(0, 10))

    name_entry = tk.Entry(form_frame, width=80)
    add_field("Name:", name_entry)

    contact_entry = tk.Entry(form_frame, width=80)
    add_field("Phone/Email:", contact_entry)

    date_entry = tk.Entry(form_frame, width=80)
    add_field("Date (YYYY-MM-DD):", date_entry)

    time_var = tk.StringVar(value="Select Time")
    time_options = ["10:00 AM", "11:00 AM", "12:00 PM", "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM"]
    time_dropdown = ttk.Combobox(form_frame, textvariable=time_var, values=time_options, width=77, state="readonly")
    add_field("Select Time:", time_dropdown)

    gown_var = tk.StringVar(value="Select Gown Type")
    gown_options = ["Wedding Gown", "Prom Gown", "Ball Gown", "Customized dress", "Kids Wear"]
    gown_dropdown = ttk.Combobox(form_frame, textvariable=gown_var, values=gown_options, width=77, state="readonly")
    add_field("Select Gown Type:", gown_dropdown)

    message_box = tk.Text(form_frame, width=60, height=4)
    add_field("Special Requests:", message_box)

    button_frame = tk.Frame(booking_window, bg="white")
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="BOOK NOW", command=book_now, bg="purple", fg="white", width=15,
          font=("Arial", 14, "bold")).grid(row=0, column=0, padx=10)

    tk.Button(button_frame, text="CLEAR ALL", command=clear_form, bg="gray", fg="white", width=15,
          font=("Arial", 14, "bold")).grid(row=0, column=1, padx=10)

def clear_form():
    name_entry.delete(0, tk.END)
    contact_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    time_var.set("Select Time")
    gown_var.set("Select Gown Type")
    message_box.delete("1.0", tk.END)

gown_descriptions = {
    "Wedding Gown": "Elegant and luxurious, perfect for your special day.",
    "Prom Gown": "Stylish and glamorous, making you the star of the night.",
    "Ball Gown": "A classic, royal look for formal events.",
    "Customized dress": "Designed uniquely for you, tailored to your style.",
    "Kids Wear": "Adorable and fashionable outfits for children."
}

def book_now():
    name = name_entry.get().strip()
    contact = contact_entry.get().strip()
    date = date_entry.get().strip()
    time_12hr = time_var.get()
    gown_type = gown_var.get()
    message = message_box.get("1.0", tk.END).strip()

    if not name or not contact or not date or time_12hr == "Select Time" or gown_type == "Select Gown Type":
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD.")
        return

    gown_popup = tk.Toplevel(booking_window)
    gown_popup.title("Gown Preview")
    gown_popup.state('zoomed')
    gown_popup.configure(bg="white")

    if logo_image:
        logo_label = tk.Label(gown_popup, image=logo_image, bg="white")
        logo_label.place(relx=1.0, y=10, anchor="ne")


    tk.Label(gown_popup, text=f"You selected: {gown_type}", font=("Times New Roman", 28, "bold"),
             fg="purple", bg="white").pack(pady=20)

    tk.Label(gown_popup, text=gown_descriptions[gown_type], font=("Times New Roman", 20),
             fg="purple", bg="white", wraplength=600).pack(pady=10)

    image_paths = {
        "Wedding Gown": "bridal.webp",
        "Prom Gown": "prom.webp",
        "Ball Gown": "ball.jpg",
        "Customized dress": "customized.webp",
        "Kids Wear": "kids.jpg"
    }

    if gown_type in image_paths and os.path.exists(image_paths[gown_type]):
        img = Image.open(image_paths[gown_type]).resize((400, 550), Image.LANCZOS)
        gown_img = ImageTk.PhotoImage(img)
        img_label = tk.Label(gown_popup, image=gown_img, bg="white")
        img_label.image = gown_img
        img_label.pack(pady=10)

    tk.Button(gown_popup, text="OK", command=lambda: confirm_booking(
        gown_popup, name, contact, date, time_12hr, gown_type, message
    ), bg="purple", fg="white", font=("Arial", 14, "bold")).pack(pady=10)

def confirm_booking(popup, name, contact, date, time_12hr, gown_type, message):
    popup.destroy()
    try:
        time_24hr = datetime.strptime(time_12hr, "%I:%M %p").strftime("%H:%M:%S")
        cursor.execute(
            "INSERT INTO customer_details (name, contact, date, time, gown_type, message) VALUES (%s, %s, %s, %s, %s, %s)",
            (name, contact, date, time_24hr, gown_type, message)
        )
        db.commit()
        messagebox.showinfo("Success", "Booking Confirmed!")
        clear_form()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

login_window = tk.Tk()
login_window.title("Login")
login_window.state('zoomed')
login_window.configure(bg="white")

load_logo()

if logo_image:
    logo_label = tk.Label(login_window, image=logo_image, bg="white")
    logo_label.place(relx=1.0, y=10, anchor="ne")

tk.Label(login_window, text="Victoria Luxe Booking System", font=("Freestyle Script", 48, "bold"),
         fg="purple", bg="white").pack(pady=30)

login_frame = tk.Frame(login_window, bg="white")
login_frame.pack()

tk.Label(login_frame, text="Username:", fg="purple", bg="white", font=("Arial", 14, "bold")).pack(pady=10)
username_entry = tk.Entry(login_frame, width=30)
username_entry.pack(pady=5)

tk.Label(login_frame, text="Password:", fg="purple", bg="white", font=("Arial", 14, "bold")).pack(pady=10)
password_entry = tk.Entry(login_frame, width=30, show="*")
password_entry.pack(pady=5)

tk.Button(login_window, text="Login", command=login, bg="purple", fg="white", width=15,
          font=("Arial", 14, "bold")).pack(pady=40)

login_window.mainloop()
