import subprocess
import sys
import tkinter
from settings import *


def custom_messagebox(
    label_result,
    processing_duration,
    files_for_processing,
    stat_files_processed,
):
    try:
        window = tkinter.Tk()
        window.title("fileSync - processing finished")
        window.resizable(False, False)
        window.attributes("-topmost", True)

        log_label_result = tkinter.Label(window, text=label_result)
        log_label_result.grid(row=0, column=0, columnspan=2)

        lbl_proc_files = tkinter.Label(window, text=f"Processed files: {stat_files_processed}/{files_for_processing}")
        lbl_proc_files.grid(row=1, column=0, columnspan=2)

        lbl_processing_duration = tkinter.Label(window, text=f"Processing duration: {processing_duration:.2f} seconds")
        lbl_processing_duration.grid(row=2, column=0, columnspan=2)

        lbl_execution_timestamp = tkinter.Label(window, text=f"Synchronization run on {execution_timestamp}")
        lbl_execution_timestamp.grid(row=3, column=0, columnspan=2)

        btn_ok = tkinter.Button(window, text="OK", command=lambda: sys.exit())
        btn_ok.grid(row=4, column=0, padx=10, pady=10)

        btn_open_log_file = tkinter.Button(
            window,
            text="Open the log file",
            command=lambda: [subprocess.Popen(["start", log_file_directory], shell=True), sys.exit()],
        )
        btn_open_log_file.grid(row=4, column=1, padx=10, pady=10)

        center_window(window)

    except Exception as e:
        print(f"Error (method: custom_messagebox): {e}")
