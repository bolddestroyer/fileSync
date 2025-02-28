from settings import *


def write_log(
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
):
    try:
        with open(log_file_directory, "w", encoding="utf-8") as log_file:
            log_file.write("-----------------------------THE FILE SYNCHRONIZER------------------------------\n")
            log_file.write(f"Source directory: {source_directory}\n")
            log_file.write(f"Target directory: {target_directory}\n")
            log_file.write(f"Synchronization run on {execution_timestamp}\n")
            log_file.write(f"Processed files: {stat_files_processed}/{files_for_processing}\n")
            log_file.write(f"Processing duration: {processing_duration:.2f} seconds\n")
            log_file.write(f"Result: {label_result}\n")
            log_file.write(f"\n-----------------------------------STATISTICS-----------------------------------\n")
            log_file.write(f"Total number of files: {stat_files_total}\n")
            log_file.write(f"Unchanged files: {stat_files_unchanged}\n\n")
            log_file.write(f"New files: {stat_files_new}\n")
            log_file.write(label_files_new)
            log_file.write(f"\nReplaced files: {stat_files_replaced}\n")
            log_file.write(label_files_replaced)
            if stat_files_not_in_source != 0:
                log_file.write(f"\nFiles missing in the source directory: {stat_files_not_in_source}\n")
                log_file.write(label_files_not_in_source)
            else:
                log_file.write(f"\nFiles missing in the source directory: None")
    except Exception as e:
        print(f"Error (method: write_log): {e}")
