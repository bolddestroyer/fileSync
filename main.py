from tkinter import messagebox
from modules import *
from datetime import *
from user_variables import *
import os
import shutil
import re


#Variables - messages for the log file
log_txt_new_files = str()       #New files in USB
log_txt_replaced_files = str()        #Replaced USB files
log_txt_proc_res = str()        #Final result of the processing
log_txt_nonex_insrc = str()      #USB files that do not exist in Dropbox or VSC
log_txt_nonex_excldir = str()      #Non-existant directories listed as excluded

#Variables - statistics
stat_total_files = 0        #All processed files (non-excluded)
stat_new_files = 0      #New files in USB
stat_replaced_files = 0       #Replaced USB files
stat_unchanged_files = 0      #Unchanged Dropbox and VSC files
stat_nonex_insrc = 0      #USB files that do not exist in Dropbox or VSC


##############################
#Synchronization process
def fileSync():

    #Global variables
    global log_txt_new_files, log_txt_replaced_files, log_txt_proc_res, log_txt_nonex_insrc, log_txt_nonex_excldir, stat_total_files, stat_new_files, stat_replaced_files, stat_unchanged_files, stat_nonex_insrc

    print('Processing...')      #Message displayed in the console, indicating that processing has started

    del_jwlib_saves_from_usb(usb_dir, excl_usb_dirs)     #From 'modules': delete all JW Library saves from USB

    try:
        #Loop 1: iterate through all directories, subdirectories (list) and files (list) from Dropbox - synchronize between Dropbox and the USB
        for dir_dp, sub_dirs_dp, files_dp in os.walk(dropbox_dir):
            #Iterate through the list of files from the Dropbox directory
            for file_dp in files_dp:

                #Variables - directories
                dropbox_file_l1 = os.path.join(dir_dp, file_dp)     #Path of the current Dropbox file
                usb_dir_l1 = os.path.join(usb_dir, dir_dp[len(dropbox_dir):])       #USB directory corresponding to the current Dropbox directory
                usb_file_l1 = os.path.join(usb_dir_l1, file_dp)     #Path of the USB file corresponding to the current Dropbox file

                #If the Dropbox file is not excluded, or if the Dropbox directory is not excluded
                if file_dp not in {'.dropbox', 'desktop.ini', 'marker_file'} and not excl_dropbox_dirs_regexp.search(dir_dp):
                    #If the USB file corresponding to the current Dropbox file (same path) does not exist
                    if not os.path.exists(usb_file_l1):
                        #Create the Dropbox directory together with all it's parent directories in USB; exist_ok=True - do not return an error if a directory exists
                        os.makedirs(usb_dir_l1, exist_ok=True)
                        #Copy the file from Dropbox to USB
                        shutil.copy(dropbox_file_l1, usb_dir_l1)
                        log_txt_new_files += f"The file '{file_dp}' was created in '{usb_dir_l1}'\n"
                        stat_total_files += 1
                        stat_new_files += 1
                    #If a Dropbox file exists in USB and if file last modified date in Dropbox is more recent (newer version of a file in Dropbox)
                    elif os.path.exists(usb_file_l1) and (datetime.fromtimestamp(os.stat(dropbox_file_l1).st_mtime) > datetime.fromtimestamp(os.stat(usb_file_l1).st_mtime)):
                        #Overwrite/replace a USB file by the same one from Dropbox
                        shutil.copy(dropbox_file_l1, usb_dir_l1)
                        log_txt_replaced_files += f"The file '{file_dp}' was replaced in '{usb_dir_l1}'\n"
                        stat_total_files += 1
                        stat_replaced_files += 1
                    else:
                        stat_total_files += 1
                        stat_unchanged_files += 1
            
        #Loop 2: iterate through all directories, subdirectories (list) and files (list) from VSC - synchronize between VSC and the USB
        for dir_md, sub_dirs_md, files_md in os.walk(vsc_dir):
            #Iterate through the list of files from the VSC directory
            for file_md in files_md:

                #Variables - directories
                vsc_file_l2 = os.path.join(dir_md, file_md)      #Path of the current VSC file
                usb_dir_l2 = os.path.join(usb_dir, dir_md[len(vsc_dir):])       #USB directory corresponding to the current VSC directory
                usb_file_l2 = os.path.join(usb_dir_l2, file_md)     #Path of the USB file corresponding to the current VSC file

                #Variables - directories
                vsc_regexp_excl_l2 = re.compile('.*.git.*|.*__pycache__.*|.*_exe.*|.*_log.*|.*chromedriver-win64.*')      #Regexp for excluded VSC directories
                vsc_regexp_incl_l2 = re.compile('.*Virtual Studio Code.*')      #Regexp for the VSC directory

                #If a VSC file does not exist in USB and if a VSC directory is not excluded
                if not os.path.exists(usb_file_l2) and vsc_regexp_incl_l2.search(dir_md) and not vsc_regexp_excl_l2.search(dir_md):
                    #Create the VSC directory together with all it's parent directories in USB; exist_ok=True - do not return an error if a directory exists
                    os.makedirs(usb_dir_l2, exist_ok=True)
                    #Copy the file from VSC to USB
                    shutil.copy(vsc_file_l2, usb_dir_l2)
                    log_txt_new_files += f"The file '{file_md}' was created in '{usb_dir_l2}'\n"
                    stat_total_files += 1
                    stat_new_files += 1
                #If a VSC file does not exist in USB, if a VSC directory is not excluded, and if file last modified date in VSC is more recent (newer version of a file in VSC)
                elif os.path.exists(usb_file_l2) and vsc_regexp_incl_l2.search(dir_md) and not vsc_regexp_excl_l2.search(dir_md) and (datetime.fromtimestamp(os.stat(vsc_file_l2).st_mtime) > datetime.fromtimestamp(os.stat(usb_file_l2).st_mtime)):
                    #Overwrite/replace a USB file by the same one from VSC
                    shutil.copy(vsc_file_l2, usb_dir_l2)
                    log_txt_replaced_files += f"The file '{file_md}' was replaced in '{usb_dir_l2}'\n"
                    stat_total_files += 1
                    stat_replaced_files += 1
                else:
                    stat_total_files += 1
                    stat_unchanged_files += 1

        #Loop 3: iterate through all directories, subdirectories (list) and files (list) from USB - check if files from USB exist in Dropbox and VSC, apart for those excluded
        for dir_usb, sub_dirs_usb, files_usb in os.walk(usb_dir):
            #Iterate through the list of files from the USB directory
            for file_usb in files_usb:

                #Variables - directories
                drobpox_dir_l3 = os.path.join(dropbox_dir, dir_usb[len(usb_dir):])      #Dropbox directory corresponding to the current USB directory
                vsc_dir_l3 = os.path.join(vsc_dir, dir_usb[len(usb_dir):])      #VSC directory corresponding to the current USB directory
                dropbox_file_l3 = os.path.join(dropbox_dir, dir_usb[len(usb_dir):], file_usb)       #Dropbox file corresponding to the current USB file
                vsc_file_l3 = os.path.join(vsc_dir, dir_usb[len(usb_dir):], file_usb)       #VSC file corresponding to the current USB file

                #Variables - excluded directories
                vsc_regexp_excl_l3 = re.compile('.*Virtual Studio Code.*')      #Regexp for excluded VSC directories

                #If a USB directory is not excluded
                if dir_usb not in excl_usb_dirs and not excl_usb_dirs_regexp.search(dir_usb):
                    #If a USB file does not exist in Dropbox, if it is not a VSC directory and if a USB file is not excluded
                    if not os.path.exists(dropbox_file_l3) and not vsc_regexp_excl_l3.search(dir_usb) and file_usb not in {'INVITATION GERMAN.pdf', 'Notfallliste Predigtdienstgruppen ab dem 22.01.2024.xlsx'}:
                        log_txt_nonex_insrc += f'The file "{file_usb}" does not exist in "{drobpox_dir_l3}".\n'
                        stat_nonex_insrc += 1
                    #If a USB file does not exist in VSC and if it is a VSC directory
                    elif not os.path.exists(vsc_file_l3) and vsc_regexp_excl_l3.search(dir_usb):
                        log_txt_nonex_insrc += f'The file "{file_usb}" does not exist in "{vsc_dir_l3}".\n'
                        stat_nonex_insrc += 1

        #Iterate through a list of excluded USB directories
        for excl_usb_dir in excl_usb_dirs:
            #If an excluded USB directory does not exist
            if not os.path.exists(excl_usb_dir):
                #Add a string to the log text, provided that it does not already exist in the log text
                log_txt_nonex_excldir = add_if_logtxt_noex(log_txt_nonex_excldir, f'USB directory "{excl_usb_dir}" listed as excluded, does not exist.')

    #Exceptions - in case of OSErrors (input directory not found) and PermissionError (insufficient permissions to perform requested action)
    except (OSError, PermissionError) as e:
        log_txt_proc_res = f"ERROR: {str(e)}.\n"
        messagebox.showerror("fileSynchronizer: Error", f"{str(e)}")
        sys.exit()
    else:
        log_txt_proc_res = "File synchronization successful!"      #If processing is successful
    
    #Print out the processing result in the console
    print(log_txt_proc_res)

    #Create a log file
    log_file(dropbox_dir, vsc_dir, usb_dir, log_txt_proc_res, stat_total_files, stat_unchanged_files, stat_new_files, log_txt_new_files, stat_replaced_files, log_txt_replaced_files, log_txt_nonex_excldir, stat_nonex_insrc, log_txt_nonex_insrc, log_file_dir, log_file_rundate)

    #Display the messagebox
    custom_messagebox(log_file_dir, log_txt_proc_res, log_file_rundate)


##############################
#Main window, allows selecting between sychronization and analysis
def fileSync_window():
    window = tkinter.Tk()
    window.title("FileSync")

    btn_db_usb_vsc_sync = tkinter.Button(window, text="Run sychronization", command=lambda: fileSync())
    btn_db_usb_vsc_sync.grid(row=1, column=0, padx=10, pady=10)

    #Display the message box in the middle of the screen
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

    window.mainloop()