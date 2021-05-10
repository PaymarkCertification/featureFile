import glob
import logging
import unittest
import os
from typing import TextIO

unittest.TestLoader.sortTestMethodsUsing = None
logging.basicConfig(level=logging.INFO, filename='myapp.log', format='%(asctime)s %(levelname)s:%(message)s')


def update_feature(file: str, find: str, add:str) -> TextIO:
    """Reads file into memory"""
    with open(file, 'r') as in_read:
        buffer = in_read.readlines()
        logging.info(f'{file} loaded into memory')

    """Trunc line after cond results to True"""
    with open(file, 'w') as out_file:
        for line in buffer:
            if line == f"{find}\n":
                line = line + f"{add}\n"
            out_file.write(line)
        logging.info(f'{file}: parsed')


def all_files(printer: int = 1) -> list:
    if printer:
        return [feature for feature in glob.glob("*.feature")]
    else:
        print(type([feature for feature in glob.glob("*.feature")]))


def create_feature(file: str):
    """creates a new feature file"""
    with open(file, 'w') as out_file:
        feature = """@PCASB @PCASB5 @PTS190 @MVP
Feature: PCASB5 T 91191202 ASB ATND PTS190
    In order to...
    As a...
    I want to...

Background:
  Given the following test configuration:
  | GroupName | ProfileName | Scheme | Terminal |
  | Sec_WFT_User | T 91191202 ASB ATND | PAYMARK.PTS.ISO.ACQUIRER | T 91191202 ASB ATND |


@FIN @PUR @CRD @MOB @CDCVM @REV @ReplaceCard
Scenario Outline: FIN PUR1 CRD MOB CDCVM REV
Given I select WebFT Transaction Set template 'FIN PUR1 CRD MOB CDCVM REV' under the configured LabelPath
    And I select card <CardName>
    And I override field '0004' with value <AmountTransaction>
When I run the Transaction Set
Then field '0039' in the Acquirer response on the 'first' transaction should be <ResponseCode>
    And field '0039' in the Issuer response on the 'first' transaction should be <ResponseCode>
Then field '0039' in the Acquirer response on the 'second' transaction should be <ResponseCode>
    And field '0039' in the Issuer response on the 'second' transaction should be <ResponseCode>
    And field '0052' in the Issuer 'request' on the 'second' transaction is not present
Examples:
  | CardName                      | AmountTransaction | ResponseCode |
#Not a top transaction, BIN was randomly selected, This card can be replaced
  | 461755_4742 ASB DUL EFTPOS PDASBx VISA     | 000000002100      |  00          |

  @FIN @PUR @CRD @MOB @SIGVF @REV @ReplaceCard
Scenario Outline: FIN PUR1 CRD MOB SIGVF REV
Given I select WebFT Transaction Set template 'FIN PUR1 CRD MOB SIGVF REV' under the configured LabelPath
    And I select card <CardName>
    And I override field '0004' with value <AmountTransaction>
When I run the Transaction Set
Then field '0039' in the Acquirer response on the 'first' transaction should be 08
    And field '0039' in the Issuer response on the 'first' transaction should be <ResponseCode>
Then field '0039' in the Acquirer response on the 'second' transaction should be 08
    And field '0039' in the Issuer response on the 'second' transaction should be <ResponseCode>
    And field '0052' in the Issuer 'request' on the 'second' transaction is not present
Examples:
  | CardName                      | AmountTransaction | ResponseCode |
#Not a top transaction, BIN was randomly selected, This card can be replaced
  | 461755_4742 ASB DUL EFTPOS PDASBx VISA     | 000000002400      |  00          |"""
        out_file.write(feature)
        

class TestFeatureUpdateMethod(unittest.TestCase):
    def test_create_feature(self):
        file_name = 'unit_test.feature'
        create_feature(file_name)
        assert(os.path.exists(file_name))

    
    def test_update_feature(self):
        a, b = "Then field '0039' in the Acquirer response on the 'first' transaction should be <ResponseCode>", "    And field '0025' in the Issuer 'request' matches <PosCondition>"
        file = 'example.feature'
        create_feature(file)
        update_feature(file, a, b)
        with open(file, 'r') as in_read:
            buff = in_read.readlines()
            assert f"{b}\n" in buff


    def test_neg_line_update_feature(self):
        a, b = "This line should not be present", "    And field '0025' in the Issuer 'request' matches <PosCondition>"
        file = 'example.feature'
        create_feature(file)
        update_feature(file, a, b)
        with open(file, 'r') as in_read:
            buff = in_read.readlines()
            assert f"{b}\n" not in buff

    def tearDown(self):
        directory = [feature for feature in glob.glob("*.feature")]
        for file in directory:
            if file in ('unit_test.feature', 'example.feature'):
                os.remove(file)


if __name__ == '__main__':
    print(all_files())
    unittest.main()
    


