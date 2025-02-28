import shutil
import sys
import time
from tkinter import messagebox
from settings import *
from writeLog import write_log
from customMessagebox import custom_messagebox


def sync_process(source_directory, target_directory):

    start_time = time.time()

    label_result = str()
    stat_files_total = 0
    stat_files_new = 0
    label_files_new = str()
    stat_files_replaced = 0
    label_files_replaced = str()
    stat_files_unchanged = 0
    stat_files_not_in_source = 0
    label_files_not_in_source = str()

    files_for_processing = 0

    if source_directory == "Browse" or target_directory == "Browse":
        messagebox.showerror("fileSync: Error", "Select both directories.")
        return

    try:
        for source_dir, source_subdir, source_files in os.walk(source_directory):
            for file in source_files:
                files_for_processing += 1

        stat_files_processed = 0

        for source_dir, source_subdir, source_files in os.walk(source_directory):
            for source_file in source_files:
                curr_source_file_dir = os.path.join(source_dir, source_file)
                curr_target_dir = os.path.join(target_directory, source_dir[len(source_directory) :])
                curr_target_file_dir = os.path.join(curr_target_dir, source_file)

                if not os.path.exists(curr_target_file_dir):
                    os.makedirs(curr_target_dir, exist_ok=True)
                    shutil.copy(curr_source_file_dir, curr_target_dir)
                    label_files_new += f"The file '{source_file}' was created in '{curr_target_dir}'\n"
                    stat_files_total += 1
                    stat_files_new += 1
                    stat_files_processed += 1
                elif os.path.exists(curr_target_file_dir) and (
                    datetime.fromtimestamp(os.stat(curr_source_file_dir).st_mtime)
                    > datetime.fromtimestamp(os.stat(curr_target_file_dir).st_mtime)
                ):
                    shutil.copy(curr_source_file_dir, curr_target_dir)
                    label_files_replaced += f"The file '{source_file}' was replaced in '{curr_target_dir}'\n"
                    stat_files_total += 1
                    stat_files_replaced += 1
                    stat_files_processed += 1
                else:
                    stat_files_total += 1
                    stat_files_unchanged += 1
                    stat_files_processed += 1

        for target_dir, target_subdir, target_files in os.walk(target_directory):
            for target_file in target_files:

                curr_source_dir = os.path.join(source_directory, target_dir[len(target_directory) :])
                curr_source_file_dir = os.path.join(source_directory, target_dir[len(target_directory) :], target_file)

                if not os.path.exists(curr_source_file_dir):
                    label_files_not_in_source += f'The file "{target_file}" does not exist in "{curr_source_dir}".\n'
                    stat_files_not_in_source += 1

        processing_duration = time.time() - start_time
        label_result = "File synchronization successful!"

    except (OSError, PermissionError, FileNotFoundError, Exception) as e:
        label_result = f"ERROR: {str(e)}.\n"
        messagebox.showerror("fileSynchronizer: Error", f"{str(e)}")
        sys.exit()

    write_log(
        source_directory,
        target_directory,
        label_result,
        stat_files_total,
        stat_files_unchanged,
        stat_files_new,
        label_files_new,
        stat_files_replaced,
        label_files_replaced,
        stat_files_not_in_source,
        label_files_not_in_source,
        processing_duration,
        files_for_processing,
        stat_files_processed,
    )

    custom_messagebox(
        label_result,
        processing_duration,
        files_for_processing,
        stat_files_processed,
    )
