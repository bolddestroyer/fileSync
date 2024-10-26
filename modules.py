#File with modules for the fileSynchronizer_main
import csv
import os
import re
from datetime import *
import subprocess
import sys
import tkinter


#Read excluded directories out of a CSV-file and pack them into a list
def read_csv_excl_dirs(csv_file_dir):
    
    #Variables - list of excluded directories from the CSV-file
    excl_dirs = []

    #Read the CSV-file
    with open(csv_file_dir, newline='', encoding='utf-8') as csv_file:
        file_excl_dirs = csv.reader(csv_file)       #Read all entries from the file, create a reader object
        next(file_excl_dirs, None)      #Skip the 1st line of the CSV-file
        #Iterate through all entries of the entries from the CSV-file
        for row in file_excl_dirs:
            excl_dirs.append(row[0])
   
    #Return the list of excluded directories
    return excl_dirs


#If a string does not already exist in the log_text, add it to the log_text
def add_if_logtxt_noex(log_text, string_val):
    
    #If the new log_text is not already present in the log_text string, add it
    if string_val not in log_text:
        log_text += f'{string_val}\n'
    
    return log_text


#Delete all JW Library saves from USB
def del_jwlib_saves_from_usb(usb_dir, excl_usb_dirs):
    
    #Variables - regexp for jwlibrary saves
    jwlib_save_regexp = re.compile('UserdataBackup.*.jwlibrary')

    #Loop: iterate through all directories, subdirectories (list) and files (list) from USB
    for dir_usb, sub_dirs_usb, files_usb in os.walk(usb_dir):
        #Iterate through the list of files from the USB directory
        for file_usb in files_usb:
            #If a USB file is a JWLibrary save and is not excluded
            if jwlib_save_regexp.search(file_usb) and dir_usb not in excl_usb_dirs:
                os.remove(os.path.join(dir_usb, file_usb))


#Log file
def log_file(dropbox_dir, vsc_dir, usb_dir, log_txt_proc_res, stat_total_files, stat_unchanged_files, stat_new_files, log_txt_new_files, stat_replaced_files, log_txt_replaced_files, log_txt_nonex_excldir, stat_nonex_insrc, log_txt_nonex_insrc, log_file_dir, log_file_rundate):
    #Composition of the log file
    with open(log_file_dir, 'w', encoding='utf-8') as log_file:
        log_file.write('\n-----------------------------THE FILE SYNCHRONIZER------------------------------\n\n')
        log_file.write(f'Dropbox directory: {dropbox_dir}\n')
        log_file.write(f'VSC directory: {vsc_dir}\n')
        log_file.write(f'USB directory: {usb_dir}\n')
        log_file.write('\n--------------------------------------------------------------------------------\n')
        log_file.write(f'Synchronization run on {log_file_rundate}\n')
        log_file.write(f'Result of the synchronization: {log_txt_proc_res}\n')
        log_file.write(f'\n-----------------------------------STATISTICS-----------------------------------\n')
        log_file.write(f'Total number of files: {stat_total_files}\n')
        log_file.write(f'Unchanged files: {stat_unchanged_files}\n\n')
        log_file.write(f'New files: {stat_new_files}\n')
        log_file.write(log_txt_new_files)
        log_file.write(f'\nReplaced files: {stat_replaced_files}\n')
        log_file.write(log_txt_replaced_files)
        
        log_file.write('\n------------------------OTHER SOURCE DESTINATION ANALYSIS------------------------\n')

        if log_txt_nonex_excldir != "":
            log_file.write(f'Non-existing excluded directories:\n{log_txt_nonex_excldir}')
        else:
            log_file.write(f'Non-existing excluded directories: None\n')

        if stat_nonex_insrc != 0:
            log_file.write(f'\nFiles missing in Dropbox and VSC: {stat_nonex_insrc}\n')
            log_file.write(log_txt_nonex_insrc)
        else:
            log_file.write(f'\nFiles missing in Dropbox and VSC: None')


def open_log_file(log_file_dir):
    subprocess.Popen([r"C:\Program Files\Notepad++\notepad++.exe", log_file_dir], shell=True)


#Custom message box with buttons to close and open the log file
def custom_messagebox(log_file_dir, log_txt_proc_res, log_file_rundate):
    #Top-level pop-up window
    msg_box = tkinter.Tk()
    msg_box.title('fileSynchronizer processing info')
    
    #Labels
    lbl_status = tkinter.Label(msg_box, text=log_txt_proc_res)
    lbl_status.grid(row=0, column=0, columnspan=2)
    lbl_runtime = tkinter.Label(msg_box, text=f'Synchronization run on {log_file_rundate}')
    lbl_runtime.grid(row=1, column=0, columnspan=2)

    #Button - close the message box and end the process
    btn_ok = tkinter.Button(msg_box, text="OK", command=lambda: sys.exit())
    btn_ok.grid(row=2, column=0, padx=10, pady=10)
    
    #Button - open the log file
    #Open the log file (subprocess - interact with OS and launch external process; Popen - create a new process; shell=True - run through cmd)
    btn_open_log = tkinter.Button(msg_box, text="Open the log file", command=lambda: [open_log_file(log_file_dir), sys.exit()])
    btn_open_log.grid(row=2, column=1, padx=10, pady=10)

    #Display the message box in the middle of the screen
    msg_box.update_idletasks()
    width = msg_box.winfo_width()
    height = msg_box.winfo_height()
    x = (msg_box.winfo_screenwidth() // 2) - (width // 2)
    y = (msg_box.winfo_screenheight() // 2) - (height // 2)
    msg_box.geometry(f'{width}x{height}+{x}+{y}')