import cv2
import numpy as np
from pathlib import Path
from hypothesis import given
import hypothesis.strategies as st
import tempfile
import dicom.dicom as dicom

class TestProperty:
    @given(img1_color=st.integers(min_value=0, max_value=255), img2_color=st.integers(min_value=0, max_value=255))
    def test_compare_image_is_symmetric(self, img1_color, img2_color):
        """
        The comparison must be symmetric.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)

            # Crea due piccole immagini 10x10 pixel
            img1_array = np.full((10, 10, 3), img1_color, dtype=np.uint8)
            img2_array = np.full((10, 10, 3), img2_color, dtype=np.uint8)

            img1 = tmp_path / "img1.png"
            img2 = tmp_path / "img2.png"
            cv2.imwrite(str(img1), img1_array)
            cv2.imwrite(str(img2), img2_array)

            score1 = dicom.compare_image(img1, img2)
            score2 = dicom.compare_image(img2, img1)

            assert score1 == score2

    @given(img_content=st.integers(min_value=0, max_value=255))
    def test_compare_image_identity(self, img_content):
        """
        Comparing the same image should yield perfect similarity
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            img = tmp_path / "img.png"

            # Creazione immagine valida
            import cv2, numpy as np
            img_array = np.full((10, 10, 3), img_content, dtype=np.uint8)
            cv2.imwrite(str(img), img_array)

            score = dicom.compare_image(img, img)
            assert score == 1.0
