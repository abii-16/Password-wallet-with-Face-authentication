# Password Wallet with Face Authentication
# Requirements: tkinter, cv2, face_recognition, mysql.connector, numpy
# Ensure MySQL server is running and a folder named 'faces' exists with images

import tkinter, cv2, os, face_recognition, mysql.connector as s, face_recognition as fr, random
from tkinter import messagebox
from tkinter import ttk
import numpy as np

# Flags and global variables
l = 0
s1 = 0
c_l = []

def main():
    def get_encoded_faces():
        encoded = {}
        for dirpath, dnames, fnames in os.walk("./faces"):
            for f in fnames:
                if f.endswith(".jpg") or f.endswith(".png") or f.endswith(".jpeg"):
                    face = fr.load_image_file("faces/" + f)
                    encoding = fr.face_encodings(face)[0]
                    encoded[f.split(".")[0]] = encoding
        return encoded

    def classify_face(im):
        global name
        faces = get_encoded_faces()
        f_encoded = list(faces.values())
        known_face_names = list(faces.keys())
        img = cv2.imread(im, 1)
        face_locations = face_recognition.face_locations(img)
        unknown_face_encodings = face_recognition.face_encodings(img, face_locations)
        face_names = []
        name = ''
        for f_encoding in unknown_face_encodings:
            matches = face_recognition.compare_faces(f_encoded, f_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(f_encoded, f_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            face_names.append(name)

    # Main welcome window
    win_wel = tkinter.Tk()
    win_wel.title("Welcome Page")
    win_wel.geometry("500x500")
    win_wel.configure(bg='turquoise2')

    # MySQL connection
    mc = s.connect(host='localhost', user='root', passwd='')
    cr = mc.cursor()
    cr.execute("create database if not exists password_wallet")
    cr.execute("use password_wallet")
    cr.execute("create table if not exists user_info(username varchar(15) primary key, password varchar(15) binary not null, save char(3))")
    cr.execute("create table if not exists password (passd varchar(50));")

    def login():
        global win_login, e_login1, e_login2
        win_login = tkinter.Tk()
        win_login.title("Login")
        win_login.geometry("300x349")
        win_login.configure(bg="turquoise2")
        tkinter.Label(win_login, text='LOGIN', font=('Georgia', 12), bg='turquoise2').place(x=120, y=10)
        tkinter.Label(win_login, text='Username', font=('Georgia', 12), bg='turquoise2').place(x=115, y=80)
        e_login1 = tkinter.Entry(win_login, width=30, bg='white')
        e_login1.place(x=65, y=105)
        tkinter.Label(win_login, text='Password', font=('Georgia', 12), bg='turquoise2').place(x=115, y=140)
        e_login2 = tkinter.Entry(win_login, width=30, bg='white', show='*')
        e_login2.place(x=65, y=165)
        tkinter.Button(win_login, text='Login', width=10, bg='antiquewhite4', font=('Georgia', 12), command=save_login).place(x=100, y=235)
        tkinter.Button(win_login, text='Back', height=1, width=7, bg='antiquewhite4', font=('Georgia', 12), command=main).place(x=2, y=3)

    def save_login():
        global e_signin1, e_login1
        try:
            cr.execute("select username from user_info where username='{}'".format(e_login1.get()))
            un = cr.fetchall()
            cr.execute("select password from user_info where username='{}'".format(e_login1.get()))
            p_list = cr.fetchall()
            passwd = ''.join([j for i in p_list for j in i])
            cr.execute("select save from user_info where username='{}'".format(e_login1.get()))
            s_list = cr.fetchall()
            save = ''.join([j for i in s_list for j in i])
            if un == [] and e_login1.get() != '':
                messagebox.showwarning("Invalid", 'Username not found. Please try again.')
                mc.close()
            elif save.lower() == 'yes':
                take_photoL = messagebox.askokcancel("Taking Photo", 'Select OK to continue...')
                if take_photoL:
                    cam = cv2.VideoCapture(0)
                    result, image = cam.read()
                    if result:
                        cv2.imwrite('test.png', image)
                        classify_face("test.png")
                        if name == "Unknown":
                            messagebox.showinfo("Face Recognition", "Face not recognised. Try again later.")
                        elif name == e_login1.get():
                            e_login2.delete(0, tkinter.END)
                            e_login2.insert(0, passwd)
                            messagebox.showinfo("Autofill", "Password autofilled!")
                    else:
                        messagebox.showinfo("Error", "Photo not taken.")
        except:
            messagebox.showwarning("Invalid", "Username not found")

    def signin():
        global e_signin1, e_signin2, e_signin3
        win_signin = tkinter.Tk()
        win_signin.title("Register")
        win_signin.geometry("300x349")
        win_signin.configure(bg='turquoise2')
        tkinter.Label(win_signin, text='REGISTER', font=('Georgia', 12), bg='turquoise2').place(x=120, y=10)
        tkinter.Label(win_signin, text='Username', font=('Georgia', 12), bg='turquoise2').place(x=115, y=60)
        e_signin1 = tkinter.Entry(win_signin, width=30, bg='white')
        e_signin1.place(x=65, y=84)
        tkinter.Label(win_signin, text='Password', font=('Georgia', 12), bg='turquoise2').place(x=115, y=106)
        e_signin2 = tkinter.Entry(win_signin, width=30, bg='white', show='*')
        e_signin2.place(x=65, y=128)
        tkinter.Label(win_signin, text='Confirm Password', font=('Georgia', 12), bg='turquoise2').place(x=100, y=152)
        e_signin3 = tkinter.Entry(win_signin, width=30, bg='white', show='*')
        e_signin3.place(x=65, y=174)
        tkinter.Button(win_signin, text='Register', width=10, bg='antiquewhite4', font=('Georgia', 12), command=save_signin).place(x=97, y=270)
        tkinter.Button(win_signin, text='Back', width=7, bg='antiquewhite4', font=('Georgia', 12), command=main).place(x=2, y=3)

    def save_signin():
        if e_signin2.get() != e_signin3.get():
            messagebox.showwarning("Invalid", "Password confirmation failed.")
        else:
            take_photoS = messagebox.askokcancel("Taking Photo", "Press OK to continue")
            if take_photoS:
                cr.execute("insert into user_info values('{}','{}','{}')".format(e_signin1.get(), e_signin3.get(), 'yes'))
                mc.commit()
                cam = cv2.VideoCapture(0)
                result, image = cam.read()
                if result:
                    cv2.imwrite('faces/{}.png'.format(e_signin1.get()), image)
                    messagebox.showinfo("Success", "Photo saved and registered.")
            else:
                messagebox.showinfo("Info", "Photo not taken.")

    tkinter.Label(win_wel, text="Password Wallet with Face Authentication", font=('Georgia', 13), bg='turquoise2').place(x=55, y=20)
    tkinter.Button(win_wel, text='Login', height=2, width=14, command=login, font=('Georgia', 12), bg='antiquewhite4').place(x=176, y=80)
    tkinter.Button(win_wel, text='Register', height=2, width=14, command=signin, font=('Georgia', 12), bg='antiquewhite4').place(x=176, y=140)

    tkinter.mainloop()

main()
