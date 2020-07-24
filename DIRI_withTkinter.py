import tkinter as tk
from tkinter import *
import os
from wikiapi import Wikipedia, Wolframalpha


root = tk.Tk()
root.configure(bg="white")
root.geometry("650x400")
root.resizable(False, False)

wiki = Wikipedia(lang='en')

def onClickPlaceholder(event):
    userCommand.configure(state=NORMAL)
    userCommand.delete(0, END)
    userCommand.unbind('<Button-1>', on_click_id)

def onClickSearch():
	print(wiki.search())
	label = tk.Label(root, text='')
	label.pack()

userCommandBorder = tk.Frame(root, background = 'orange')
userCommandPadding = tk.Frame(userCommandBorder, background = 'white')

userCommand = tk.Entry(userCommandPadding, width=55, font='Arial 12', bd=0)
userCommand.insert(0, "Enter what do you want to know about")
userCommand.configure(state=DISABLED)
on_click_id = userCommand.bind('<Button-1>', onClickPlaceholder)

userCommandPadding.pack(padx=4, pady=4)
userCommandBorder.pack(pady=60)
userCommand.pack(fill="both", expand=True, padx=12, pady=7, side=LEFT)

photo = PhotoImage(file = "next (2).png")
goToResult = tk.Button(userCommandPadding, text="Search", image=photo, width=25, height=25, command=onClickSearch, bd=0, bg='white')
goToResult.pack(side=RIGHT, padx=5)


root.mainloop()
