from datetime import datetime
import os


log_file_directory = os.path.join(os.path.expanduser("~"), r"Documents\fileSync_log.txt")
execution_timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")


def center_window(window):
    try:
        window.update_idletasks()
        window_width = window.winfo_width()
        window_height = window.winfo_height()
        screen_center_x = (window.winfo_screenwidth() // 2) - (window_width // 2)
        screen_center_y = (window.winfo_screenheight() // 2) - (window_height // 2)
        window.geometry(f"{window_width}x{window_height}+{screen_center_x}+{screen_center_y}")
    except Exception as e:
        print(f"Error (method: center_window): {e}")


def set_window_size(window, fraction=5):
    try:
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        window_width = screen_width // fraction
        window_height = screen_height // fraction
        window.geometry(f"{window_width}x{window_height}")
    except Exception as e:
        print(f"Error (method: set_window_size): {e}")
