# DICOM Processing Module

This Python module provides utilities for processing **DICOM** files and medical images. It allows you to extract metadata, convert images, anonymize patient data, capture frames from ultrasound machine, and compare images using SSIM.

## Features

- Extract and save metadata from DICOM files.
- Convert DICOM images to PNG, JPG, or GIF formats.
- Anonymize sensitive patient data.
- Capture frames from video devices (e.g., ultrasound).
- Compare images using **Structural Similarity Index (SSIM)**.
- Command-line interface using `argparse`.

## Installation

Make sure you have Python 3.10+ installed. Then install the package and its dependencies directly from the `pyproject.toml`:

```bash
pip install .
```

Or, if you want to install it in editable/development mode (useful for modifying the code):

```bash
python3 -m pip install -e .
```

# Usage

Run the script using the appropriate subcommands.

## 1. Process DICOM files

### The directory must follow this structure:
```bash
File_DICOM
       ├── Paziente1
       │   ├── 1-1.dcm
       │   ├── 1-2.dcm
       │   └── 1-6.dcm
       ├── Paziente2
       │   ├── 1-3.dcm
       │   ├── 1-4.dcm
       │   └── 1-8.dcm
```

Process all DICOM files in a directory, optionally anonymizing patient data:
```bash
dicom processing --dicom_dir path/to/dicom_folder --anonymous
```
- `dicom_dir`: Directory containing DICOM files.
- `anonymous`: Optional flag to anonymize patient information.

## 2. Acquire a frame from a device

Captures a frame from a video device (e.g., an ultrasound machine) and saves it as a PNG image. The program assumes that a video capture card is connected to the computer and that the device can be accessed through Linux operating system file descriptors (FDs)
```bash
dicom.py acquire --fd 0 --output frame.png
```
- `fd`: File descriptor of the device.
- `output`: Path to save the captured frame (default: frame_default.png).

## 3. Compare two images
Compare two images using the Structural Similarity Index (SSIM):
```bash
python dicom.py compare --image1 path1.png --image2 path.png
```
- `image1`: Path to the first image.
- `image2`: Path to the second image.

### Logging and Verbosity

Use the `--verbosity` flag to set the logging level:
```bash
dicom --verbosity DEBUG processing --dicom_dir path/to/dicom_folder 
```

Options:`NOTSET`, `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
Default: `INFO`


# Example Workflow
### 1: Process DICOM directory with anonymization:
```bash
dicom processing --dicom_dir data --anonymous
```

### 2: Capture a frame from device 0:
```bash
dicom acquire --fd 0 --output frame.png
```

```bash
dicom acquire --video <path_video> --output frame.png
```

### 3: Compare two images:
```bash
dicom compare --image1 frame1.png --image2 frame2.png
```

# Esecuzione con Docker
L’applicazione DICOM è containerizzata in un’immagine Docker.  
I dati possono essere condivisi con il container tramite 

```bash
docker container run -it -v $PWD/examples:/home/dicom dicom:isa bash
```