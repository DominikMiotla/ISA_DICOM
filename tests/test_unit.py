import numpy as np
import pytest
from pathlib import Path
import dicom.dicom as dicom
import hashlib
from unittest.mock import MagicMock
from PIL import Image
from unittest.mock import patch, MagicMock

def hash_file_txt(path, algo="md5"):
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def hash_file_img(path, algo="md5"):
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

class TestClass:
    def test_dicom_to_jpg_0(self):
        input_dir = Path("tests/Data/DICOM_1/DICOM")
        output_jpg = "tests/Data/DICOM_1/DICOM/OUTPUT/1-1.jpg"
        correct_jpg = "tests/Data/DICOM_1/SOL/1-1.jpg"
        processing_dicom = dicom.DICOM(path = input_dir, anonymous = False)
        processing_dicom.processing()
        hash_input = hash_file_img(output_jpg)
        hash_correct = hash_file_img(correct_jpg)
        assert hash_input == hash_correct

    @pytest.mark.parametrize("input, output, correct",[("tests/Data/DICOM_2/DICOM","tests/Data/DICOM_2/DICOM/OUTPUT/1-2.jpg","tests/Data/DICOM_2/SOL/1-2.jpg"), ("tests/Data/DICOM_3/DICOM","tests/Data/DICOM_3/DICOM/OUTPUT/1-3.jpg","tests/Data/DICOM_3/SOL/1-3.jpg")])
    def test_dicom_to_jpg_1(self,input,output,correct):
        input_dir = Path(input)
        processing_dicom = dicom.DICOM(path = input_dir, anonymous = False)
        processing_dicom.processing()
        hash_input = hash_file_img(output)
        hash_correct = hash_file_img(correct)
        assert hash_input == hash_correct

    def test_dicom_to_png_0(self):
        input_dir = Path("tests/Data/DICOM_1/DICOM")
        output_jpg = "tests/Data/DICOM_1/DICOM/OUTPUT/1-1.png"
        correct_jpg = "tests/Data/DICOM_1/SOL/1-1.png"
        processing_dicom = dicom.DICOM(path = input_dir, anonymous = False)
        processing_dicom.processing()
        hash_input = hash_file_img(output_jpg)
        hash_correct = hash_file_img(correct_jpg)
        assert hash_input == hash_correct
    
    @pytest.mark.parametrize("input, output, correct",[("tests/Data/DICOM_2/DICOM","tests/Data/DICOM_2/DICOM/OUTPUT/1-2.png","tests/Data/DICOM_2/SOL/1-2.png"), ("tests/Data/DICOM_3/DICOM","tests/Data/DICOM_3/DICOM/OUTPUT/1-3.png","tests/Data/DICOM_3/SOL/1-3.png")])
    def test_dicom_to_png_1(self,input,output,correct):
        input_dir = Path(input)
        processing_dicom = dicom.DICOM(path = input_dir, anonymous = False)
        processing_dicom.processing()
        hash_input = hash_file_img(output)
        hash_correct = hash_file_img(correct)
        assert hash_input == hash_correct

    def test_txt_0(self):
        input_dir = Path("tests/Data/DICOM_1/DICOM")
        output_txt = "tests/Data/DICOM_1/DICOM/OUTPUT/1-1.txt"
        correct_txt = "tests/Data/DICOM_1/SOL/1-1.txt"
        processing_dicom = dicom.DICOM(path = input_dir, anonymous = False)
        processing_dicom.processing()
        hash_input = hash_file_txt(output_txt)
        hash_correct = hash_file_txt(correct_txt)
        assert hash_input == hash_correct

    @pytest.mark.parametrize("input, output, correct",[("tests/Data/DICOM_2/DICOM","tests/Data/DICOM_2/DICOM/OUTPUT/1-2.txt","tests/Data/DICOM_2/SOL/1-2.txt"), ("tests/Data/DICOM_3/DICOM","tests/Data/DICOM_3/DICOM/OUTPUT/1-3.txt","tests/Data/DICOM_3/SOL/1-3.txt")])
    def test_txt_1(self,input,output,correct):
        input_dir = Path(input)
        processing_dicom = dicom.DICOM(path = input_dir, anonymous = False)
        processing_dicom.processing()
        hash_input = hash_file_txt(output)
        hash_correct = hash_file_txt(correct)
        assert hash_input == hash_correct

    def test_anonymous(self):
        input_dir = Path("tests/Data/DICOM_4/DICOM")
        output_txt = "tests/Data/DICOM_4/DICOM/OUTPUT/1-4.txt"
        correct_txt = "tests/Data/DICOM_4/SOL/ANONYMUS_1-4.txt"
        processing_dicom = dicom.DICOM(path = input_dir, anonymous = True)
        processing_dicom.processing()
        hash_input = hash_file_txt(output_txt)
        hash_correct = hash_file_txt(correct_txt)
        assert hash_input == hash_correct

    @pytest.mark.parametrize("img1, img2, score",[("tests/Data/Compare/1-1.jpg","tests/Data/Compare/1-1.jpg","1.0000"), ("tests/Data/Compare/1-1.jpg","tests/Data/Compare/1-2.jpg","0.7098")])
    def test_compare(self,img1,img2,score):
        image1 = Path(img1)
        image2 = Path(img2)
        res = dicom.compare_image(image1,image2)
        assert res == pytest.approx(float(score), rel=1e-4)

    def test_acquire(self):
        source = "tests/Data/Acquire/Image1.wmv"
        expected = "tests/Data/Acquire/expected.png"
        output = Path("tests/Data/Acquire/frame.png")
        dicom.acquire(source=source,frame_name=output)
        h_expected = hash_file_img(expected)
        h_output = hash_file_img(output)
        assert h_expected == h_output


    def test_processing_crea_gif(self):
        tmp_path = Path("tests/Data/GIF")
        dcm_file = tmp_path / "test.dcm"
        dcm_file.write_text("FAKE DICOM CONTENT")

        fake_ds = MagicMock()
        n_frames = 3
        fake_ds.pixel_array = np.random.randint(0, 255, size=(n_frames, 120, 120), dtype=np.uint8)
        fake_ds.__getitem__.side_effect = lambda tag: (
            MagicMock(value=100) if tag == (0x0018, 0x1063) else MagicMock()
        )
        def contains(tag):
            return tag == (0x0028, 0x0008)
        fake_ds.__contains__.side_effect = contains

        with patch("dicom.dicom.pydicom.dcmread", return_value=fake_ds):
            dcm = dicom.DICOM(tmp_path, anonymous=False)
            dcm.processing()

        output_gif = tmp_path / "OUTPUT" / "test.gif"
        assert output_gif.exists()

        with Image.open(output_gif) as img:
            assert img.format == "GIF"
            frames = 0
            try:
                while True:
                    img.seek(frames)
                    frames += 1
            except EOFError:
                pass
            assert frames == n_frames
