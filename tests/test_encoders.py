import tempfile

from tests import fixtures
from dji_parse import encoders


class TestEncoders:
    def test_encoder_outputs(self):
        for encoder in encoders.EncoderType:
            with open(f"tests/fixtures/output.{encoder.value}") as ff:
                expected = ff.read()

            with tempfile.TemporaryFile(mode="r+") as tf:
                encoders.get_encoder(encoder)(tf, fixtures.EXPECTED_POSITIONS).write()

                tf.seek(0)
                actual = tf.read()

            assert expected == actual
