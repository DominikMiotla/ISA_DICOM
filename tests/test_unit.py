import numpy as np
import pytest
from pathlib import Path
import dicom.dicom as dicom
import hashlib
from unittest.mock import MagicMock, patch
from PIL import Image, ImageChops
import shutil
from skimage.metrics import structural_similarity as ssim

def images_are_similar(img1_path, img2_path, threshold=0.99):
    """
    Confronta due immagini usando l'ISS (Structural Similarity Index).

    Args:
        img1_path (str / Path): percorso della prima immagine
        img2_path (str / Path): percorso della seconda immagine
        threshold (float): soglia minima di similarità (0-1)

    Returns:
        bool: True se le immagini sono simili sopra la soglia, False altrimenti
    """
    img1 = np.array(Image.open(img1_path).convert("L"))  # converti in scala di grigi
    img2 = np.array(Image.open(img2_path).convert("L"))

    score, diff = ssim(img1, img2, full=True)
    return score >= threshold


def texts_are_equal(file1, file2, ignore_whitespace=True):
    """
    Confronta due file di testo carattere per carattere.
    
    Parametri:
    - ignore_whitespace: se True ignora spazi e newline extra
    """
    with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
        content1 = f1.read()
        content2 = f2.read()

        if ignore_whitespace:
            # rimuove tutti gli spazi e newline per un confronto "puro"
            content1 = ''.join(content1.split())
            content2 = ''.join(content2.split())

        if content1 == content2:
            return True
        else:
            # opzionale: mostra dove differiscono
            min_len = min(len(content1), len(content2))
            for i in range(min_len):
                if content1[i] != content2[i]:
                    print(f"Differenza al carattere {i}: '{content1[i]}' vs '{content2[i]}'")
                    break
            if len(content1) != len(content2):
                print(f"I file hanno lunghezze diverse: {len(content1)} vs {len(content2)}")
            return False



class TestClass:
    def test_dicom_to_jpg_0(self, tmp_path):
        dicom_file = Path("tests/Data/DICOM_1/DICOM/1-1.dcm")
        correct_jpg = "tests/Data/DICOM_1/SOL/1-1.jpg"
        output_jpg = tmp_path / "OUTPUT/1-1.jpg"
        shutil.copy(dicom_file, tmp_path)

        processing_dicom = dicom.DICOM(path=tmp_path, anonymous=False)
        processing_dicom.processing()
        assert images_are_similar(output_jpg, correct_jpg)

    @pytest.mark.parametrize(
        "input, output, correct",
        [
            ("tests/Data/DICOM_2/DICOM/1-2.dcm","OUTPUT/1-2.jpg","tests/Data/DICOM_2/SOL/1-2.jpg"),
            ("tests/Data/DICOM_3/DICOM/1-3.dcm","OUTPUT/1-3.jpg","tests/Data/DICOM_3/SOL/1-3.jpg")
        ]
    )
    def test_dicom_to_jpg_1(self,input,output,correct, tmp_path):
        shutil.copy(input, tmp_path)
        processing_dicom = dicom.DICOM(path=tmp_path, anonymous=False)
        processing_dicom.processing()
        assert images_are_similar(tmp_path / output, correct)

    def test_dicom_to_png_0(self,tmp_path):
        dicom_file = Path("tests/Data/DICOM_1/DICOM/1-1.dcm")
        correct_png = "tests/Data/DICOM_1/SOL/1-1.png"
        output_png = tmp_path / "OUTPUT/1-1.png"
        shutil.copy(dicom_file, tmp_path)

        processing_dicom = dicom.DICOM(path=tmp_path, anonymous=False)
        processing_dicom.processing()
        assert images_are_similar(output_png, correct_png)

    @pytest.mark.parametrize(
        "input, output, correct",
        [
            ("tests/Data/DICOM_2/DICOM/1-2.dcm","OUTPUT/1-2.png","tests/Data/DICOM_2/SOL/1-2.png"),
            ("tests/Data/DICOM_3/DICOM/1-3.dcm","OUTPUT/1-3.png","tests/Data/DICOM_3/SOL/1-3.png")
        ]
    )
    def test_dicom_to_png_1(self,input,output,correct,tmp_path):
        shutil.copy(input, tmp_path)
        processing_dicom = dicom.DICOM(path=tmp_path, anonymous=False)
        processing_dicom.processing()
        assert images_are_similar(tmp_path / output, correct)

    def test_txt_0(self,tmp_path):
        dicom_file = Path("tests/Data/DICOM_1/DICOM/1-1.dcm")
        correct_txt = "tests/Data/DICOM_1/SOL/1-1.txt"
        output_txt = tmp_path / "OUTPUT/1-1.txt"
        shutil.copy(dicom_file, tmp_path)

        processing_dicom = dicom.DICOM(path=tmp_path, anonymous=False)
        processing_dicom.processing()
        assert texts_are_equal(output_txt, correct_txt)

    @pytest.mark.parametrize(
        "input, output, correct",
        [
            ("tests/Data/DICOM_2/DICOM/1-2.dcm","OUTPUT/1-2.txt","tests/Data/DICOM_2/SOL/1-2.txt"),
            ("tests/Data/DICOM_3/DICOM/1-3.dcm","OUTPUT/1-3.txt","tests/Data/DICOM_3/SOL/1-3.txt")
        ]
    )
    def test_txt_1(self,input,output,correct,tmp_path):
        shutil.copy(input, tmp_path)
        processing_dicom = dicom.DICOM(path=tmp_path, anonymous=False)
        processing_dicom.processing()
        assert texts_are_equal(tmp_path / output, correct)

    def test_anonymous(self, tmp_path):
        dicom_file = Path("tests/Data/DICOM_4/DICOM/1-4.dcm")
        correct_txt = "tests/Data/DICOM_4/SOL/ANONYMUS_1-4.txt"
        output_txt = tmp_path / "OUTPUT/1-4.txt"
        shutil.copy(dicom_file, tmp_path)

        processing_dicom = dicom.DICOM(path=tmp_path, anonymous=True)
        processing_dicom.processing()
        assert texts_are_equal(output_txt, correct_txt)

    @pytest.mark.parametrize(
        "img1, img2, score",
        [
            ("tests/Data/Compare/1-1.jpg","tests/Data/Compare/1-1.jpg","1.0000"),
            ("tests/Data/Compare/1-1.jpg","tests/Data/Compare/1-2.jpg","0.7098")
        ]
    )
    def test_compare(self,img1,img2,score):
        image1 = Path(img1)
        image2 = Path(img2)
        res = dicom.compare_image(image1,image2)
        assert res == pytest.approx(float(score), rel=1e-3)  # tolleranza più alta per CI

    def test_acquire(self,tmp_path):
        source = "tests/Data/Acquire/Image1.wmv"
        expected = "tests/Data/Acquire/expected.png"
        output = tmp_path / "frame.png"

        dicom.acquire(source=source,frame_name=output)
        assert images_are_similar(output, expected)

    def test_processing_crea_gif(self, tmp_path):
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
