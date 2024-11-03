import os
import re
from datetime import *
import subprocess
import sys
import tkinter


#If a string does not already exist in the log_lbl, add it to the log_lbl
def add_if_logtxt_noex(log_lbl, string_val):
    if string_val not in log_lbl:
        log_lbl += f'{string_val}\n'
    return log_lbl


#Delete all JW Library saves from target
def remove_jwlib_saves_from_usb(dir_trg):
    
    jwlibsave_regexp = re.compile('UserdataBackup.*.jwlibrary')

    #Iterate through all directories, subdirectories (list) and files (list) from target
    for dir_trg_dirs, dir_trg_subdir, dir_trg_files in os.walk(dir_trg):
        #Iterate through the list of target files
        for dir_trg_file in dir_trg_files:
            #Remove if files file is a JWLibrary save
            if jwlibsave_regexp.search(dir_trg_file):
                print(os.path.join(dir_trg, dir_trg_dirs, dir_trg_file))
                os.remove(os.path.join(dir_trg, dir_trg_dirs, dir_trg_file))


#Log file
def log_file(dir_src, dir_trg, log_lbl_processResult, stat_totalFiles, stat_unchangedFiles, stat_newFiles, log_lbl_newFiles, stat_replacedFiles, log_lbl_replacedFiles, stat_nonExistInSrc, log_lbl_nonExistInSrc, log_dir, log_rundate):

    with open(log_dir, 'w', encoding='utf-8') as log_file:
        log_file.write('-----------------------------THE FILE SYNCHRONIZER------------------------------\n')
        log_file.write(f'Source directory: {dir_src}\n')
        log_file.write(f'Target directory: {dir_trg}\n')
        log_file.write(f'Synchronization run on {log_rundate}\n')
        log_file.write(f'Result: {log_lbl_processResult}\n')
        log_file.write(f'\n-----------------------------------STATISTICS-----------------------------------\n')
        log_file.write(f'Total number of files: {stat_totalFiles}\n')
        log_file.write(f'Unchanged files: {stat_unchangedFiles}\n\n')
        log_file.write(f'New files: {stat_newFiles}\n')
        log_file.write(log_lbl_newFiles)
        log_file.write(f'\nReplaced files: {stat_replacedFiles}\n')
        log_file.write(log_lbl_replacedFiles)        
        log_file.write('\n------------------------OTHER SOURCE DESTINATION ANALYSIS------------------------\n')
        if stat_nonExistInSrc != 0:
            log_file.write(f'Files from target missing in source: {stat_nonExistInSrc}\n')
            log_file.write(log_lbl_nonExistInSrc)
        else:
            log_file.write(f'Files missing in source: None')


def open_log_file(log_dir):
    subprocess.Popen([r"C:\Program Files\Notepad++\notepad++.exe", log_dir], shell=True)


#Custom message box with buttons to close and open the log file
def custom_messagebox(log_dir, log_lbl_processResult, log_rundate):
    #Top-level pop-up window
    msg_box = tkinter.Tk()
    msg_box.title('fileSynchronizer processing info')
    
    #Labels
    lbl_status = tkinter.Label(msg_box, text=log_lbl_processResult)
    lbl_status.grid(row=0, column=0, columnspan=2)
    lbl_runtime = tkinter.Label(msg_box, text=f'Synchronization run on {log_rundate}')
    lbl_runtime.grid(row=1, column=0, columnspan=2)

    #Button - close the message box and end the process
    btn_ok = tkinter.Button(msg_box, text="OK", command=lambda: sys.exit())
    btn_ok.grid(row=2, column=0, padx=10, pady=10)
    
    #Button - open the log file
    #Open the log file (subprocess - interact with OS and launch external process; Popen - create a new process; shell=True - run through cmd)
    btn_open_log = tkinter.Button(msg_box, text="Open the log file", command=lambda: [open_log_file(log_dir), sys.exit()])
    btn_open_log.grid(row=2, column=1, padx=10, pady=10)

    #Display the message box in the middle of the screen
    msg_box.update_idletasks()
    width = msg_box.winfo_width()
    height = msg_box.winfo_height()
    x = (msg_box.winfo_screenwidth() // 2) - (width // 2)
    y = (msg_box.winfo_screenheight() // 2) - (height // 2)
    msg_box.geometry(f'{width}x{height}+{x}+{y}')