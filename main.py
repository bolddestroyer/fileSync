import ctypes
from tkinter import filedialog
import tkinter
import win32gui
from settings import set_window_size, center_window
from syncProcess import sync_process
from syncProcessCreator import sync_process_creator


def close_existing_window(window_title):
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd:
        ctypes.windll.user32.PostMessageW(hwnd, 0x0010, 0, 0)


def app_window():
    window_title = "fileSync"
    background_color = "#182b6b"
    close_existing_window(window_title)

    window = tkinter.Tk()
    window.title(window_title)
    window.resizable(False, False)
    window.configure(bg=background_color)
    window.attributes("-topmost", True)

    for i in range(6):
        if i < 2 or i == 4:
            window.grid_rowconfigure(i, weight=0)
        else:
            window.grid_rowconfigure(i, weight=1)

    for i in range(4):
        window.grid_columnconfigure(i, weight=1)

    def select_directory(button):
        selected_directory = filedialog.askdirectory()
        if selected_directory:
            button.config(text=selected_directory)
            return selected_directory

    label_btn_source_directory = tkinter.Label(
        window,
        text="I want to sync all files from this directory:",
        bg=background_color,
        fg="#FFFFFF",
        font=("Helvetica", 10, "bold"),
    )
    label_btn_source_directory.grid(row=1, column=1, columnspan=2)
    btn_source_directory = tkinter.Button(window, text="Browse", command=lambda: select_directory(btn_source_directory))
    btn_source_directory.grid(row=2, column=0, columnspan=4)

    label_btn_target_directory = tkinter.Label(
        window,
        text="to this directory:",
        bg=background_color,
        fg="#FFFFFF",
        font=("Helvetica", 10, "bold"),
    )
    label_btn_target_directory.grid(row=3, column=1, columnspan=2)
    btn_target_directory = tkinter.Button(
        window,
        text="Browse",
        command=lambda: select_directory(btn_target_directory),
    )
    btn_target_directory.grid(row=4, column=0, columnspan=4)

    btn_run_sync = tkinter.Button(
        window,
        text="Run sync",
        command=lambda: sync_process(btn_source_directory.cget("text"), btn_target_directory.cget("text")),
        width=20,
        height=1,
        background="#35baf6",
        fg="#FFFFFF",
        font=("Helvetica", 10, "bold"),
    )
    btn_run_sync.grid(row=5, column=0, columnspan=4, pady=(30, 10))

    label_creator = tkinter.Label(
        window,
        text="Creator option:",
        anchor="e",
        bg=background_color,
        fg="#FFFFFF",
        font=("Helvetica", 10, "bold"),
    )
    label_creator.grid(row=6, column=1, sticky="e", padx=10, pady=10)
    btn_creator = tkinter.Button(window, text="Special sync", command=lambda: sync_process_creator())
    btn_creator.grid(row=6, column=2, sticky="w")

    set_window_size(window)
    center_window(window)

    window.mainloop()
