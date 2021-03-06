import mythril.laser.ethereum.transaction as transaction
from mythril.ether import util
import mythril.laser.ethereum.svm as svm
from mythril.disassembler.disassembly import Disassembly
from datetime import datetime
from mythril.ether.soliditycontract import SolidityContract
import tests
from mythril.analysis.security import fire_lasers
from mythril.analysis.symbolic import SymExecWrapper


def test_create():
    contract = SolidityContract(str(tests.TESTDATA_INPUTS_CONTRACTS / 'calls.sol'))

    laser_evm = svm.LaserEVM({})

    laser_evm.time = datetime.now()
    laser_evm.execute_contract_creation(contract.creation_code)

    resulting_final_state = laser_evm.open_states[0]

    for address, created_account in resulting_final_state.accounts.items():
        created_account_code = created_account.code
        actual_code = Disassembly(contract.code)

        for i in range(len(created_account_code.instruction_list)):
            found_instruction = created_account_code.instruction_list[i]
            actual_instruction = actual_code.instruction_list[i]

            assert found_instruction['opcode'] == actual_instruction['opcode']

def test_sym_exec():
    contract = SolidityContract(str(tests.TESTDATA_INPUTS_CONTRACTS / 'calls.sol'))

    sym = SymExecWrapper(contract, address=(util.get_indexed_address(0)), strategy="dfs")
    issues = fire_lasers(sym)

    assert len(issues) != 0
