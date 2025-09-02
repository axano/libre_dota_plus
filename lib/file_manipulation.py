import os


def retrieve_last_line(file):
    with open(file) as f:
        for line in f:
            pass
        last_line = line
    return last_line


def delete_last_line_of_file(file_path):
    with open(file_path, "r+", encoding="utf-8") as file:
        file.seek(0, os.SEEK_END)

        # This code means the following code skips the very last character in the file -
        # i.e. in the case the last line is null we delete the last line
        # and the penultimate one
        pos = file.tell() - 1

        # Read each character in the file one at a time from the penultimate
        # character going backwards, searching for a newline character
        # If we find a new line, exit the search
        while pos > 0 and file.read(1) != "\n":
            pos -= 1
            file.seek(pos, os.SEEK_SET)

        # So long as we're not at the start of the file, delete all the characters ahead
        if pos > 0:
            file.seek(pos, os.SEEK_SET)
            file.truncate()
            delete_trailing_newlines(file_path)


def delete_trailing_newlines(file_path):
    with open(file_path, 'r+') as f:
        f.seek(0, 2)  # navigates to the position at end of file
        f.seek(f.tell() - 1)  # navigates to the position of the penultimate char at end of file
        last_char = f.read()
        if last_char == '\n':
            f.truncate(f.tell() - 1)
