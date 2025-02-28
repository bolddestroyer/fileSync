# fileSync

The fileSync is a Python application that synchronizes files between a source directory and a target directory. It provides options to exclude specific files and directories from the synchronization process.

## Key Features:

- **GUI Interface**: User-friendly interface to select source and target directories.
- **File Synchronization**: Synchronizes files between the selected directories.
- **Logging**: Logs the synchronization process to a file.
- **Custom Message Box**: Displays a custom message box with the synchronization results.
- **Exclusion Rules**: Allows specifying directories and files to exclude from synchronization.

## Installation:

#### 1. Open the command prompt (CMD)

#### 2. Check if you have Python installed

Execute the following command in CMD:

```sh
python --version
```

If the output is `Python X.XX.X` (where X.XX.X are substituted by numbers indicating version, e.g. 3.13.2), then Python is installed on your machine.
Check if you have the newest available version.

```sh
winget search --id Python.Python
```

If a newer version is available, update using the following command (however, this is not mandatory):

```sh
winget install --id Python.Python.X.XX --source winget --upgrade
```

:grey_exclamation: (substitute `X.XX` by version, e.g. 3.13)

If the output does not indicate the version, then Python is not installed.
Install Python using the following command:

```sh
winget install Python.Python.X.XX --source winget
```

:grey_exclamation: (substitute `X.XX` by version, e.g. 3.13)

#### 3. Navigate to the Documents directory:

```sh
cd C:\Users\<your_user_name>\Documents
```

#### 4. Clone the repository:

```sh
git clone https://github.com/yourusername/fileSync.git
```

#### 5. Navigate to the directory where the repository is located:

```sh
cd fileSync
```

#### 6. Install dependencies:

```sh
pip install -r requirements.txt
```

## Execution:

1. Run the **fileSync.py** file:
   ```sh
   python fileSync.py
   ```
2. Use the `Browse` buttons to select the source and target directories.
3. Click the `Run sync` button to start the synchronization process.
