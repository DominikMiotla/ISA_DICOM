"""
This module permited to create the package of the app dicom
"""

from . import dicom

def main():
    """
    This function mai call the dicom funztion main
    """
    dicom.main(dicom.setup_parser())
