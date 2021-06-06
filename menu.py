import tkinter as tk
from random import randrange

def menu():
    results = {}
    window = tk.Tk()

    nameb = tk.Label(text="ALTAR options", font=(None, 17))
    nameb.pack()

    userl = tk.Label(text="Username:")
    userl.pack()

    usernamee = tk.Entry(text="Username")
    usernamee.pack()

    audiovar = tk.BooleanVar()
    audiob = tk.Checkbutton(text="Audio", variable=audiovar)
    audiob.pack()

    localvar = tk.BooleanVar()
    localb = tk.Checkbutton(text="Single player", variable=localvar)
    localb.pack()

    fullscreenvar = tk.BooleanVar()
    fullscreenb = tk.Checkbutton(text="Fullscreen", variable=fullscreenvar)
    fullscreenb.pack()

    adminvar = tk.BooleanVar()
    adminb = tk.Checkbutton(text="Admin", variable=adminvar)
    adminb.pack()


    def action():
        results["username"] = usernamee.get()
        if not results["username"]:
            results["username"] = str({randrange(0, 100000)})

        results["audio"] = audiovar.get()
        results["local"] = localvar.get()
        results["admin"] = adminvar.get()
        results["fullscreen"] = fullscreenvar.get()
        window.destroy()

    button = tk.Button(text="Begin", command=action)
    button.pack()

    window.mainloop()
    return results


