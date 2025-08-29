# Standard library
import argparse
import logging
import os
from pathlib import Path

# Third-party packages
import pydicom
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# pylint: disable=too-few-public-methods
class DICOM():
    """
    Classe per l’elaborazione di file DICOM.

    Permette di:
    - Estrarre e salvare informazioni testuali sui file DICOM.
    - Convertire immagini DICOM in PNG, JPG o GIF.
    - Anonimizzare i dati sensibili.

    Parameters
    ----------
    path : Path
        Directory contenente i file DICOM.
    anonymous : bool
        Se True, i file vengono anonimizzati.
    """
    def __init__(self, path:Path, anonymous:bool) -> None:
        self.path = path
        self.anonymous = anonymous

        if not self._is_consistent():
            raise ValueError("Invalid path: expected a directory.")

    def _is_consistent(self) -> bool:
        return self.path.is_dir()

    def _print_info(self, dicom, file_name):
        """
        Salva le informazioni di un file DICOM in un file di testo.
        """
        with open(file_name, "w", encoding="utf-8") as f:
            print(dicom, file=f)

    def _dicom_to_graphic(self,dicom,file_name):
        """
        Defines a function that saves the plot as a PNG file.
        """
        plt.imshow(dicom.pixel_array, cmap="gray")
        plt.savefig(file_name)

    def _dicom_to_jpg(self,ds,file_name):
        """
        Defines a function that saves the file in JPG format.
        """
        im = ds.pixel_array.astype(float)
        rescaled_image =(np.maximum(im,0)/im.max())*255 #float pixels
        final_image = np.uint8(rescaled_image) #integers pixels
        final_image = Image.fromarray(final_image)
        final_image.save(file_name)

    def _dicom_to_gif(self,ds,file_name):
        """
        Defines a function that saves the file in GIF format.
        """
        time_frame = ds[0x0018,0x1063].value
        imgs = ds.pixel_array.astype(float)
        rescaled_images =(np.maximum(imgs,0)/imgs.max())*255 #float pixels
        final_images = np.uint8(rescaled_images) #integers pixels
        imgs = [Image.fromarray(img) for img in final_images]
        imgs[0].save(file_name, save_all=True, append_images=imgs[1:], duration=time_frame, loop=0)

    def _make_anonymus_dicom(self,dicom,file_name):
        """
        Defines a function that anonymizes a DICOM file.
        """
        dicom[0x0010, 0x0010].value = "Anonymous"
        dicom[0x0010, 0x0020].value = "Anonymous"
        dicom[0x0010, 0x0030].value = ""
        dicom[0x0010, 0x0040].value = ""
        dicom[0x0012, 0x0062].value = "YES"
        dicom.save_as(file_name)

    def processing(self) -> None:
        """
        Processes a DICOM file.
        This function takes a DICOM file as input and performs the necessary
        operations to extract, modify, or analyze its data.
        """
        dir_path = self.path
        flag_anonymous = self.anonymous

        for cartella,sottocartelle,files in os.walk(dir_path):
            print(f"Ci troviamo nella cartella: '{cartella}'")
            print(f"Le sottocartelle presenti sono: '{sottocartelle}'")
            print(f"I file presenti sono: '{files}'")

            #Parameter indicating whether DICOM files exist in the folder
            dicom_exists = 0

            #I create the output_directory to save the result
            output_directory = cartella + "/OUTPUT"
            os.mkdir(output_directory)

            for file in files:
                if file.endswith(".dcm"):
                    dicom_exists = 1

                    #File paths
                    name_file = file[:-4] #I remove .dcm from the name
                    file_paths = {
                        "dicom": f"{cartella}/{file}",
                        "info": f"{output_directory}/{name_file}.txt",
                        "png": f"{output_directory}/{name_file}.png",
                        "jpg": f"{output_directory}/{name_file}.jpg",
                        "gif": f"{output_directory}/{name_file}.gif",
                        "anon": f"{output_directory}/ANONYMUS_{file}"
                        }

                    ds = pydicom.dcmread(file_paths["dicom"])

                    if flag_anonymous == "YES":
                        print("---Rendo il file: " + file + " anonimo")
                        self._make_anonymus_dicom(ds,file_paths["anon"])

                    if (0x0028, 0x0008) in ds:  # Number of Frames
                        print(f"--Il file: {file} è multi-frame")
                        self._dicom_to_gif(ds, file_paths["gif"])
                    else:
                        print(f"--Il file: {file} è single-frame")
                        self._dicom_to_jpg(ds, file_paths["jpg"])
                        self._dicom_to_graphic(ds, file_paths["png"])

                    self._print_info(ds,file_paths["info"])
        #I delete the output_directory if there are no DICOM files in the folder
        if dicom_exists == 0:
            os.rmdir(output_directory)



def setup_parser() -> argparse.Namespace:
    """
    Configures and returns the command-line argument parser.

    Returns:
    argparse.Namespace: Namespace with the parsed arguments.
    """

    parser = argparse.ArgumentParser(prog="dicom", description="medical image processing")

    parser.add_argument("--verbosity",
                        type=str,
                        required=False,
                        help="Selected verbosity",
                        choices=["NOTSET","DEBUG","INFO","WARNING","ERROR","CRITICAL"],
                        default="ERROR")

    subparser = parser.add_subparsers(dest="action", required=True)

    #Action 1: Elaborate file in DICOM format
    parser_a1 = subparser.add_parser("processing",
                                     help=(
                                         "DICOM file processing requires two parameters: "
                                         "path and anonymous flag"
                                         )
                                    )
    parser_a1.add_argument("--dicom_dir",
                           type=Path,
                           required=True,
                           help="directory path")
    parser_a1.add_argument("--anonymous",
                           action="store_true",
                           help="If set, anonymize patient data")

    #Action 2: Frame acquisition from stdin (ultrasound device)
    parser_a2 = subparser.add_parser("acquire",
                                     help="Frame acquisition from stdin (ultrasound device)"
                                     )
    parser_a2.add_argument("--fd",
                           type=int,
                           required=True,
                           help="Specifies the STDIN associated with the acquisition card")
    parser_a2.add_argument("--output",
                           type=str,
                           required=False,
                           default="image",
                           help="Image name")

    #Action 3: Comparison between two images using Structural Similarity Index (SSIM)
    parser_a3 = subparser.add_parser("compare",
                                     help=(
                                         "Comparison between two images using "
                                         "Structural Similarity Index (SSIM)"
                                         )
                                     )
    parser_a3.add_argument("--image1",
                           type=Path,
                           required=True,
                           help="Path of the first image")
    parser_a3.add_argument("--image2",
                           type=Path,
                           required=True,
                           help="Path of the second image")
    return parser.parse_args()

def main(arguments: argparse.Namespace) -> None:
    """
    Main function
    """

    logging.basicConfig(level=getattr(logging, arguments.verbosity))

    logging.debug("Verbosity: %s", arguments.verbosity)
    logging.debug("Action: %s", arguments.action)

    if arguments.action == "processing":
        logging.debug("DICOM dir: %s",arguments.dicom_dir)
        logging.debug("Anonymous: %s",arguments.anonymous)
        #This is where the actual processing logic goes
        processing_dicom = DICOM(arguments.dicom_dir, arguments.anonymous)
        processing_dicom.processing()

    elif arguments.action == "acquire":
        logging.debug("FD: %s",arguments.fd)
        logging.debug("Output: %s", arguments.output)
        #This is where the actual acquisition logic goes

    elif arguments.action == "compare":
        logging.debug("Image1: %s", arguments.image1)
        logging.debug("Image2: %s",arguments.image2)
        #This is where the actual comparison logic goes

    else:
        raise ValueError(f"Unknown action {arguments.action}")


if __name__ == "__main__":
    main(setup_parser())
