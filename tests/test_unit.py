import pytest
from pathlib import Path
import dicom.dicom as dicom

import hashlib

def hash_file_txt(path, algo="md5"):
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def hash_file_dicom(path, algo="md5"):
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

class TestClass:
    def test_dicom_to_jpg_0(self):
        input_dir = Path("Data/DICOM_1/DICOM")
        output_jpg = "Data/DICOM_1/DICOM/OUTPUT/1-1.jpg"
        correct_jpg = "Data/DICOM_1/SOL/1-1.jpg"
        processing_dicom = dicom.DICOM(path = input_dir, anonymous = False)
        processing_dicom.processing()
        hash_input = hash_file_dicom(output_jpg)
        hash_correct = hash_file_dicom(correct_jpg)
        assert hash_input == hash_correct

    @pytest.mark.parametrize("input, output, correct",[("Data/DICOM_2/DICOM","Data/DICOM_2/DICOM/OUTPUT/1-2.jpg","Data/DICOM_2/SOL/1-2.jpg"), ("Data/DICOM_3/DICOM","Data/DICOM_3/DICOM/OUTPUT/1-3.jpg","Data/DICOM_3/SOL/1-3.jpg")])
    def test_dicom_to_jpg_1(self,input,output,correct):
        input_dir = Path(input)
        processing_dicom = dicom.DICOM(path = input_dir, anonymous = False)
        processing_dicom.processing()
        hash_input = hash_file_dicom(output)
        hash_correct = hash_file_dicom(correct)
        assert hash_input == hash_correct
    

    def test_dicom_to_png_0(self):
        input_dir = Path("Data/DICOM_1/DICOM")
        output_jpg = "Data/DICOM_1/DICOM/OUTPUT/1-1.png"
        correct_jpg = "Data/DICOM_1/SOL/1-1.png"
        processing_dicom = dicom.DICOM(path = input_dir, anonymous = False)
        processing_dicom.processing()
        hash_input = hash_file_dicom(output_jpg)
        hash_correct = hash_file_dicom(correct_jpg)
        assert hash_input == hash_correct
    
    @pytest.mark.parametrize("input, output, correct",[("Data/DICOM_2/DICOM","Data/DICOM_2/DICOM/OUTPUT/1-2.png","Data/DICOM_2/SOL/1-2.png"), ("Data/DICOM_3/DICOM","Data/DICOM_3/DICOM/OUTPUT/1-3.png","Data/DICOM_3/SOL/1-3.png")])
    def test_dicom_to_png_1(self,input,output,correct):
        input_dir = Path(input)
        processing_dicom = dicom.DICOM(path = input_dir, anonymous = False)
        processing_dicom.processing()
        hash_input = hash_file_dicom(output)
        hash_correct = hash_file_dicom(correct)
        assert hash_input == hash_correct
    
    def test_txt_0(self):
        input_dir = Path("Data/DICOM_1/DICOM")
        output_txt = "Data/DICOM_1/DICOM/OUTPUT/1-1.txt"
        correct_txt = "Data/DICOM_1/SOL/1-1.txt"
        processing_dicom = dicom.DICOM(path = input_dir, anonymous = False)
        processing_dicom.processing()
        hash_input = hash_file_txt(output_txt)
        hash_correct = hash_file_txt(correct_txt)
        assert hash_input == hash_correct
    
    @pytest.mark.parametrize("input, output, correct",[("Data/DICOM_2/DICOM","Data/DICOM_2/DICOM/OUTPUT/1-2.txt","Data/DICOM_2/SOL/1-2.txt"), ("Data/DICOM_3/DICOM","Data/DICOM_3/DICOM/OUTPUT/1-3.txt","Data/DICOM_3/SOL/1-3.txt")])
    def test_txt_1(self,input,output,correct):
        input_dir = Path(input)
        processing_dicom = dicom.DICOM(path = input_dir, anonymous = False)
        processing_dicom.processing()
        hash_input = hash_file_txt(output)
        hash_correct = hash_file_txt(correct)
        assert hash_input == hash_correct
    
    def test_anonymous(self):
        input_dir = Path("Data/DICOM_4/DICOM")
        output_txt = "Data/DICOM_4/DICOM/OUTPUT/1-4.txt"
        correct_txt = "Data/DICOM_4/SOL/1-4.txt"
        processing_dicom = dicom.DICOM(path = input_dir, anonymous = True)
        processing_dicom.processing()
        hash_input = hash_file_txt(output_txt)
        hash_correct = hash_file_txt(correct_txt)
        assert hash_input == hash_correct