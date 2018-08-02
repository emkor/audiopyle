import unittest

from assertpy import assert_that

from audiopyle.lib.models.compressed_feature import CompressionType
from audiopyle.lib.services.compression import compress_model, decompress_model


class CompressionTest(unittest.TestCase):
    def setUp(self):
        self.example_data = {"key_1": "text_value_with_śćłąęó",
                             "key_2": 1.0, "key_3": 14,
                             "key_4": [1., 2, "text"],
                             "key_5": {"sub_key_1": 1},
                             "key_6": None}

    def test_should_compress_and_decompress_with_none_compression(self):
        compressed = compress_model(CompressionType.none, self.example_data)
        assert_that(compressed).is_instance_of(bytes)

        decompressed = decompress_model(CompressionType.none, compressed)
        assert_that(decompressed).is_equal_to(self.example_data)

    def test_should_compress_and_decompress_with_gzip(self):
        compressed = compress_model(CompressionType.gzip, self.example_data)
        assert_that(compressed).is_instance_of(bytes)

        decompressed = decompress_model(CompressionType.gzip, compressed)
        assert_that(decompressed).is_equal_to(self.example_data)

    def test_should_compress_and_decompress_with_lzma(self):
        compressed = compress_model(CompressionType.lzma, self.example_data)
        assert_that(compressed).is_instance_of(bytes)

        decompressed = decompress_model(CompressionType.lzma, compressed)
        assert_that(decompressed).is_equal_to(self.example_data)
