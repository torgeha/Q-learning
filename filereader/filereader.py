__author__ = 'Torgeir'

import tkinter
import tkinter.filedialog

class FileReaderAndFormatter:
    """
    Reads from specified file, extracts parameters and sets as fields.
    Works as a buffer.
    """

    def __init__(self, path=None):

        self.path = path
        self.width = None
        self.height = None
        self.x = None
        self.y = None
        self.n = None
        self.board = None

        self._read_and_format()

    def _read_and_format(self):
        # String of file content
        file_content = self._read_file()



    def _read_file(self):
        # If path is not provided, open filedialog. Return String in file

        if self.path is None:
            # Hide main window
            r = tkinter.Tk()
            r.withdraw()

            # Open filedialog
            path = tkinter.filedialog.askopenfilename(initialdir="C:\\Users\\Torgeir\\Dropbox\\AI-subsymbolsk\\project5\\Q-learning\\res")

        with open(self.path, 'r') as f:
            data = f.read()
            print(data)
            print(type(data))

# Testing
fr = FileReaderAndFormatter("C:\\Users\\Torgeir\\Dropbox\\AI-subsymbolsk\\project5\\Q-learning\\res\\1-simple.txt")

