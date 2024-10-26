# fileSync
Program for uploading files from local drive and Dropbox to a USB

Process:
1. User executes the program.
2. Window is displayed.
3. User selects between sychronization and analysis.
4. Procesing starts.
5. All directories and files in Dropbox are looped through, apart for those excluded.
6. Synchronization only: files in Dropbox that do not exist in USB, or are newer than in USB (based on the last modified date), are copied to/replaced in the USB.
7. All directories and files in VSC are looped through, apart for those excluded.
8. Synchronization only: files in VSC that do not exist in USB, or are newer than in USB (based on the last modified date), are copied to/replaced in the USB.
9. All directories and files in USB are looped through, apart for those excluded.
10. Files in VSC that do not exist in Dropbox or VSC, are added to a list.
11. List of all excluded USB directories are looped through to check if they still exist. If they dont, they are added to a list.
12. Processing is over.
13. Log file is created.
14. Message box is displayed.
15. User chooses to open a log file.
16. Log file is opened, program is stopped.