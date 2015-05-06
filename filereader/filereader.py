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
        # TODO: comment and cleanup

        # Read file and convert to list
        file_content = self._read_file()

        # Replace whitespace with comma
        no_whitespace = file_content.replace(' ', ',')

        # print(no_whitespace)
        # Split the string into lines
        lines_separated = no_whitespace.splitlines()
        # print("split: ", lines_separated)

        # Convert from string list to int list
        properly_formatted = []
        for line in lines_separated:
            properly_formatted.append(list(eval(line)))
        # print(properly_formatted)

        # Extract first line of paramteres
        self.w = properly_formatted[0][0]
        self.h = properly_formatted[0][1]
        self.x = properly_formatted[0][2]
        self.y = properly_formatted[0][3]
        self.n = properly_formatted[0][4]

        # print(self.w)
        # print(self.h)
        # print(self.x)
        # print(self.y)
        # print(self.n)

        self.board = properly_formatted[1:]

    def _read_file(self):
        # If path is not provided, open filedialog. Return String in file

        if self.path is None:
            # Hide main window
            r = tkinter.Tk()
            r.withdraw()

            # Open filedialog
            self.path = tkinter.filedialog.askopenfilename(initialdir="C:\\Users\\Torgeir\\Dropbox\\AI-subsymbolsk\\project5\\Q-learning\\res")
        raw_content = None
        with open(self.path, 'r') as f:
            raw_content = f.read()
            # print(raw_content)
        return raw_content

# TODO: Remove testing
# Testing
# fr = FileReaderAndFormatter("C:\\Users\\Torgeir\\Dropbox\\AI-subsymbolsk\\project5\\Q-learning\\res\\1-simple.txt")
# fr = FileReaderAndFormatter()
# print(fr.w)
# print(fr.h)
# print(fr.x)
# print(fr.y)
# print(fr.n)
# print(fr.board)