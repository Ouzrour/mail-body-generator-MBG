"""
    Done by : Ouzrour
    Start : 25.3.23
"""
# For imagekitio
from imagekitio import ImageKit
# for Control Files / Directory
import os
# For imagekit
import base64
# To name the output file
from datetime import datetime
# Load dotenv
from dotenv import load_dotenv
# for removing file
import shutil
# Decoration for the title
import pyfiglet
# COPY to clipboard
import pyperclip

"""
    Connect to The ImageKit Server
"""


class Body_GENERATOR:
    def __init__(self, in_choice="in", out_choice="out"):
        # load Variables from .env
        load_dotenv()
        # Setup Settings from .env
        self.PRIVATE_KEY = os.getenv("IMAGEKIT_PRIVATE_KEY")
        self.PUBLIC_KEY = os.getenv("IMAGEKIT_PUBLIC_KEY")
        self.URL_ENDPOINT = os.getenv("URL_ENDPOINT")
        self.list_files = []
        self.in_choice = in_choice
        self.out_choice = out_choice
        self.dir_root = os.path.dirname(os.path.realpath(__file__))
        self.dir_in = os.path.join(self.dir_root, self.in_choice)
        self.dir_out = os.path.join(self.dir_root, self.out_choice)
        self.imagekit = None
        self.nb_choice = 0
        self.link = ""
        self.encoded = "n"
        # FUNCTIONS
        self.detect_file()
        if len(self.list_files) != 0:
            self.choice()
            self.connect()
            if self.nb_choice == 0:
                self.replace_image_in_html(self.list_files)
            else:
                self.replace_image_in_html([self.list_files[self.nb_choice - 1]])

    # TITLE
    def nice_tile(self):
        os.system('cls')
        title = pyfiglet.figlet_format("Ouzrour")
        print(title, end="")
        print("MAIL BODY GENERATOR V 1.0.0")
        print("==============================")

    # CONNECT TO IMAGEKIT API
    def connect(self):
        imagekit = ImageKit(
            private_key=self.PRIVATE_KEY,
            public_key=self.PUBLIC_KEY,
            url_endpoint=self.URL_ENDPOINT
        )
        self.imagekit = imagekit

    # DETECT FILE IN FOLDER IN and List them
    def detect_file(self):
        list_file = os.listdir(self.dir_in)
        for i in range(len(list_file)):
            if list_file[i].endswith(".htm"):
                self.list_files.append(list_file[i].replace(".htm", ""))

    # DETECT THE CHOICE OF THE USER ( 0 = ALL ) and ( i = CHOICE i )
    def choice(self):
        if (len(self.list_files) > 1):
            self.nice_tile()
            print("List of Choice : ")
            print("0 . ALL ( YOU MUST INJECT LINKS MANUALLY ) ")
            for (index, choice) in enumerate(self.list_files):
                print(str(index + 1) + " . " + choice)
            print("==============================")
            self.nb_choice = int(input("Select From The list : "))
        if (len(self.list_files) == 1):
            self.nb_choice = 1
        self.nice_tile()
        # IN CASE : ALL is not selected !
        if self.nb_choice != 0:
            print("SELECTED PROJECT : ", self.nb_choice, " . ", self.list_files[self.nb_choice - 1])
            print("==============================")
            self.link = input("ENTER THE LINK TO BE INJECTED : ")
        self.nice_tile()
        # IN CASE : ALL is not selected !
        if self.nb_choice != 0:
            print("SELECTED PROJECT : ", self.nb_choice, " . ", self.list_files[self.nb_choice - 1])
            print("SELECTED LINK : ", self.link)
            print("==============================")
            self.encoded = input("ENCODED ( y / n )  : ")

    # REMOVE FOLDER / FILE based ON a PATH !
    def remove(self, path):
        """ param <path> could either be relative or absolute. """
        if os.path.isfile(path) or os.path.islink(path):
            os.remove(path)  # remove the file
        elif os.path.isdir(path):
            shutil.rmtree(path)  # remove dir and all contains
        else:
            raise ValueError("file {} is not a file or dir.".format(path))

    # MOVE THE FILE AFTER RENAME IT (date) to the FOLDER "out"
    # + DELETE the folder that contain images
    def move_delete_cache(self, name_of_file):
        # MOVE + RENAME THE .HTM file
        os.replace(os.path.join(self.dir_in, name_of_file + ".htm"),
                   self.dir_out + '/' + str(datetime.now()).replace(":", "-") + '.htm')
        # DELETE THE FOLDER
        self.remove(os.path.join(self.dir_in, name_of_file + "_files"))

    # UPLOAD THE IMAGE TO IMAGEKIT
    # + REPLACE LINKS IN THE HTM FILE
    def replace_image_in_html(self, list_of_project):
        self.nice_tile()
        # Parse ALL the .htm file name
        for name in list_of_project:
            print("=====> " + name + " ......... ", end="")
            in_image_folder = os.path.join(self.dir_in, name + "_files")
            images = os.listdir(in_image_folder)
            for img in images:
                path_img = os.path.join(in_image_folder, img)
                with open(path_img, "rb") as img_byte:
                    img_to_base64 = base64.b64encode(img_byte.read())
                    upload = self.imagekit.upload_file(file=img_to_base64,  # required
                                                       file_name=img)
                with open(self.dir_in + '/' + name + ".htm", "r", encoding="utf-8") as htm_in:
                    # Read in the file
                    data = htm_in.read()
                    # Replace the target string
                    data = data.replace('./' + name + '_files/' + img, upload.response_metadata.raw["url"])
                    # Replace link if ALL is not selected
                    if self.nb_choice != 0:
                        data = data.replace('http://www.mysite.com/', self.link)
                    # Write the file out again
                with open(self.dir_in + '/' + name + ".htm", "w", encoding="utf-8") as htm_out:
                    htm_out.write(data)
            with open(self.dir_in + '/' + name + ".htm", "r", encoding="utf-8") as htm_in:
                data = htm_in.read()
                if (self.encoded == "y") and (self.nb_choice != 0):
                    data = base64.b64encode(bytes(data, 'utf-8'))
                pyperclip.copy(data)
            self.move_delete_cache(name)
            print(" DONE !")


if __name__ == "__main__":
    Body_GENERATOR()
