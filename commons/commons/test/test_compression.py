import unittest

from assertpy import assert_that

from commons.models.feature import CompressionType
from commons.services.compression import compress, decompress


class CompressionTest(unittest.TestCase):
    def setUp(self):
        self.example_data = {"key_1": "text_value_with_śćłąęó",
                             "key_2": 1.0, "key_3": 14,
                             "key_4": [1., 2, "text"],
                             "key_5": {"sub_key_1": 1},
                             "key_6": None}

    def test_should_compress_and_decompress_with_none_compression(self):
        compressed = compress(CompressionType.none, self.example_data)
        assert_that(compressed).is_instance_of(bytes)

        decompressed = decompress(CompressionType.none, compressed)
        assert_that(decompressed).is_equal_to(self.example_data)

    def test_should_compress_and_decompress_with_gzip(self):
        compressed = compress(CompressionType.gzip, self.example_data)
        assert_that(compressed).is_instance_of(bytes)

        decompressed = decompress(CompressionType.gzip, compressed)
        assert_that(decompressed).is_equal_to(self.example_data)

    def test_should_compress_and_decompress_with_lzma(self):
        compressed = compress(CompressionType.lzma, self.example_data)
        assert_that(compressed).is_instance_of(bytes)

        decompressed = decompress(CompressionType.lzma, compressed)
        assert_that(decompressed).is_equal_to(self.example_data)
