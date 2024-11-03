from tkinter import messagebox
from modules import *
from datetime import *
from fileSync_variables import *
import os
import shutil


def fileSync():

    log_lbl_newFiles = str()       #New files in target
    log_lbl_replacedFiles = str()        #Replaced files in target
    log_lbl_processResult = str()        #Final processing result
    log_lbl_nonExistInSrc = str()      #Files from target that do not exist in source

    stat_totalFiles = 0        #All processed files (non-excluded)
    stat_newFiles = 0      #New files in target
    stat_replacedFiles = 0       #Replaced files in target
    stat_unchangedFiles = 0      #Unchanged files in source
    stat_nonExistInSrc = 0      #Files from target that do not exist in source

    remove_jwlib_saves_from_usb(dir_trg)     #Nodules: delete all JW Library saves from target

    try:
        #Iterate through all directories, subdirectories (list) and files (list) from the source
        for dir_src_dir, dir_src_subdir, dir_src_files in os.walk(dir_src):
            for dir_src_file in dir_src_files:

                src_file = os.path.join(dir_src_dir, dir_src_file)     #Path of the current source file
                trg_curr_dir = os.path.join(dir_trg, dir_src_dir[len(dir_src):])       #Target directory equivalent to the current source directory
                trg_file = os.path.join(trg_curr_dir, dir_src_file)     #Path of the target file equivalent to the current source file

                if dir_src_file not in excl_dir_src_file and not excl_src_regexp.search(dir_src_dir):
                    #If target file corresponding to the current source file does not exist
                    if not os.path.exists(trg_file):
                        #Create the source directory with all parent directories in target; exist_ok=True - do not return an error if directory exists
                        os.makedirs(trg_curr_dir, exist_ok=True)
                        #Copy the file from source to target
                        shutil.copy(src_file, trg_curr_dir)
                        log_lbl_newFiles += f"The file '{dir_src_file}' was created in '{trg_curr_dir}'\n"
                        stat_totalFiles += 1
                        stat_newFiles += 1
                    #If source file exists in target and if file last modified date in source is more recent (newer version of a file in source)
                    elif os.path.exists(trg_file) and (datetime.fromtimestamp(os.stat(src_file).st_mtime) > datetime.fromtimestamp(os.stat(trg_file).st_mtime)):
                        #Overwrite/replace a target file by the same one from source
                        shutil.copy(src_file, trg_curr_dir)
                        log_lbl_replacedFiles += f"The file '{dir_src_file}' was replaced in '{trg_curr_dir}'\n"
                        stat_totalFiles += 1
                        stat_replacedFiles += 1
                    else:
                        stat_totalFiles += 1
                        stat_unchangedFiles += 1

        #Iterate through all directories, subdirectories (list) and files (list) from the target
        for dir_trg_dir, dir_trg_subdir, dir_trg_files in os.walk(dir_trg):
            for dir_trg_file in dir_trg_files:

                src_curr_dir = os.path.join(dir_src, dir_trg_dir[len(dir_trg):])      #Source directory equivalent to the current target directory
                src_file = os.path.join(dir_src, dir_trg_dir[len(dir_trg):], dir_trg_file)       #Path of the source file equivalent to the current target file

                #If target directory is not excluded
                if not excl_trg_regexp.search(dir_trg_dir):
                    #If target file does not exist in corresponding source directory
                    if not os.path.exists(src_file) and dir_trg_file not in {'INVITATION GERMAN.pdf', 'Notfallliste Predigtdienstgruppen ab dem 22.01.2024.xlsx'}:
                        log_lbl_nonExistInSrc += f'The file "{dir_trg_file}" does not exist in "{src_curr_dir}".\n'
                        stat_nonExistInSrc += 1

    #Exceptions - in case of OSErrors (input directory not found) and PermissionError (insufficient permissions to perform requested action)
    except (OSError, PermissionError) as e:
        log_lbl_processResult = f"ERROR: {str(e)}.\n"
        messagebox.showerror("fileSynchronizer: Error", f"{str(e)}")
        sys.exit()
    else:
        log_lbl_processResult = "File synchronization successful!"
    
    #Print out the processing result in the console
    print(log_lbl_processResult)

    #Create a log file
    log_file(dir_src, dir_trg, log_lbl_processResult, stat_totalFiles, stat_unchangedFiles, stat_newFiles, log_lbl_newFiles, stat_replacedFiles, log_lbl_replacedFiles, stat_nonExistInSrc, log_lbl_nonExistInSrc, log_dir, log_rundate)

    #Display the messagebox
    custom_messagebox(log_dir, log_lbl_processResult, log_rundate)


#Main window
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