from unittest import TestCase
from subprocess import check_output
from pathlib import Path

def output_of(command):
    return check_output(command, shell=True).decode("UTF-8")

class BaseTestCase(TestCase):
    def setUp(self):
        self.tests_dir = Path(__file__).parent
        self.myth = str(self.tests_dir.parent / "myth")

class CommandLineToolTestCase(BaseTestCase):

    def test_disassemble_code_correctly(self):
        command = "python3 {} self.myth -d -c 0x5050".format(self.myth)
        self.assertEqual('0 POP\n1 POP\n', output_of(command))

    def test_disassemble_solidity_file_correctly(self):
        solidity_file = str(self.tests_dir / 'testdata/metacoin.sol')
        command = "python3 {} -d {}".format(self.myth, solidity_file)
        self.assertIn('0 PUSH1 0x60\n2 PUSH1 0x40', output_of(command))

    def test_hash_a_function_correctly(self):
        command = "python3 {} --hash 'setOwner(address)'".format(self.myth)
        self.assertEqual('0x13af4035\n', output_of(command))

class TruffleTestCase(BaseTestCase):

    def test_analysis_truffle_project(self):
        truffle_project_root = str(self.tests_dir / "truffle_project")
        command = "cd {}; truffle compile; python3 {} --truffle".format(truffle_project_root, self.myth)
        self.assertIn("In the function 'withdrawfunds()' a non-zero amount of Ether is sent to msg.sender.", output_of(command))

class InfuraTestCase(BaseTestCase):

    def test_infura_mainnet(self):
        command = "python3 {} --rpc infura-mainnet -d -a 0x2a0c0dbecc7e4d658f48e01e3fa353f44050c208".format(self.myth)
        output = output_of(command)
        self.assertIn("0 PUSH1 0x60\n2 PUSH1 0x40\n4 MSTORE", output)
        self.assertIn("7278 POP\n7279 POP\n7280 JUMP\n7281 STOP", output)

    def test_infura_rinkeby(self):
        command = "python3 {} --rpc infura-rinkeby -d -a 0xB6f2bFED892a662bBF26258ceDD443f50Fa307F5".format(self.myth)
        output = output_of(command)
        self.assertIn("34 JUMPDEST\n35 CALLVALUE", output)

    def test_infura_kovan(self):
        command = "python3 {} --rpc infura-kovan -d -a 0xE6bBF9B5A3451242F82f8cd458675092617a1235".format(self.myth)
        output = output_of(command)
        self.assertIn("9999 PUSH1 0x00\n10001 NOT\n10002 AND\n10003 PUSH1 0x00", output)

    def test_infura_ropsten(self):
        command = "python3 {} --rpc infura-ropsten -d -a 0x6e0E0e02377Bc1d90E8a7c21f12BA385C2C35f78".format(self.myth)
        output = output_of(command)
        self.assertIn("1821 PUSH1 0x01\n1823 PUSH2 0x070c", output)
