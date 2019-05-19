class FileReader:
    def __init__(self):
        return

    def file_to_string(self, filename):
        with open(filename, "r") as file:
            contents = file.read()

        return contents