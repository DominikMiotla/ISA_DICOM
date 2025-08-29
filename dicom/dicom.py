import argparse
import logging
from pathlib import Path

class DICOM():
    def __init__(self, path:Path, anonymous:bool) -> None:
        self.path = path
        self.anonymous = anonymous

        if not self._is_consistent():
            raise ValueError("Invalid path: expected a directory.")
    
    def _is_consistent(self) -> bool:
        return self.path.is_dir()

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
        # Qui va la logica reale del processing
        processing_dicom = DICOM(arguments.dicom_dir, arguments.anonymous)

    elif arguments.action == "acquire":
        logging.debug("FD: %s",arguments.fd)
        logging.debug("Output: %s", arguments.output)
        # Qui va la logica reale dell'acquisizione

    elif arguments.action == "compare":
        logging.debug("Image1: %s", arguments.image1)
        logging.debug("Image2: %s",arguments.image2)
        # Qui va la logica reale della comparazione

    else:
        raise ValueError(f"Unknown action {arguments.action}")


if __name__ == "__main__":
    main(setup_parser())
