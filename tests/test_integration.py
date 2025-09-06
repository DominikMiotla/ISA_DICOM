import pytest
import argparse
import dicom.dicom as dicom

#They ensure that dicom.main() calls the correct methods/functions
#with the correct parameters based on the arguments passed.


class TestIntegration:

    def test_processing_integration(self, monkeypatch):
        """
        Test that main calls DICOM.processing with the correct parameters
        """
        fake_args = argparse.Namespace(
            verbosity="CRITICAL",
            action="processing",
            dicom_dir="fake_dir",
            anonymous=True
            )

        called = {}

        class FakeDICOM:
            def __init__(self, path, anonymous):
                called["init"] = (path, anonymous)

            def processing(self):
                called["processing"] = True

        monkeypatch.setattr(dicom, "DICOM", FakeDICOM)
        dicom.main(fake_args)

        assert called["init"] == ("fake_dir", True)
        assert called["processing"] is True


    def test_acquire_integration(self, monkeypatch, tmp_path):
        """
        Confirms that main() correctly calls the acquire() function with the correct parameters.
        """
        fake_args = argparse.Namespace(
            verbosity="CRITICAL",
            action="acquire",
            fd=0,
            video=None,
            output=tmp_path / "frame.png"
        )

        called = {}
        def fake_acquire(source, output):
            called["source"] = source
            called["output"] = output

        monkeypatch.setattr(dicom, "acquire", fake_acquire)
        dicom.main(fake_args)

        assert called["source"] == 0
        assert called["output"] == tmp_path / "frame.png"


    def test_compare_integration(self, monkeypatch, tmp_path):
        """
        Test that main calls compare_image and logs the result
        """
        img1 = tmp_path / "img1.png"
        img2 = tmp_path / "img2.png"
        img1.write_text("fake1")
        img2.write_text("fake2")

        fake_args = argparse.Namespace(
            verbosity="CRITICAL",
            action="compare",
            image1=img1,
            image2=img2
        )

        called = {}
        def fake_compare(p1, p2):
            called["p1"] = p1
            called["p2"] = p2
            return 0.99

        monkeypatch.setattr(dicom, "compare_image", fake_compare)
        dicom.main(fake_args)

        assert called["p1"] == img1
        assert called["p2"] == img2