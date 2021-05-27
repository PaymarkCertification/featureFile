import feature
import unittest
import os
import glob

class TestFeatureUpdateMethod(unittest.TestCase):
    def test_create_feature(self):
        file_name = 'unit_test.feature'
        feature.create_feature(file_name)
        assert(os.path.exists(file_name))

    
    def test_update_feature(self):
        a, b = "Then field '0039' in the Acquirer response on the 'first' transaction should be <ResponseCode>", "    And field '0025' in the Issuer 'request' matches <PosCondition>"
        file = 'example.feature'
        feature.create_feature(file)
        feature.update_feature(file, a, b)
        with open(file, 'r') as in_read:
            buff = in_read.readlines()
            assert f"{b}\n" in buff


    def test_neg_line_update_feature(self):
        a, b = "This line should not be present", "    And field '0025' in the Issuer 'request' matches <PosCondition>"
        file = 'example.feature'
        feature.create_feature(file)
        feature.update_feature(file, a, b)
        with open(file, 'r') as in_read:
            buff = in_read.readlines()
            assert f"{b}\n" not in buff

    def tearDown(self):
        directory = [feature for feature in glob.glob("*.feature")]
        for file in directory:
            if file in ('unit_test.feature', 'example.feature'):
                os.remove(file)


if __name__ == '__main__':
    unittest.main()
