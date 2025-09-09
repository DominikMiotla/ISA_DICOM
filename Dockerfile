# NO multi-stage Docker build:
FROM python

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
 && rm -rf /var/lib/apt/lists/*


WORKDIR /home/dicom

COPY dist/dicom-0.0.1-py3-none-any.whl .

RUN ["python", "-m", "pip", "install", "dicom-0.0.1-py3-none-any.whl"]