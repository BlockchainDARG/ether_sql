from sqlalchemy import Column, String, Integer, ForeignKey, TIMESTAMP, Boolean
from ethereum import utils

from ether_sql.models import base
from ether_sql import constants


class Receipts(base):
    """
    Class defining a receipt in the ethereum blockchain, its properties are more
    clearly defined in the ethereum yellow paper https://github.com/ethereum/yellowpaper.

    :param str transaction_hash: The Keccak 256-bit hash of this transaction
    :param bool status: Success or failure of this transaction, included after the Byzantinium fork
    :param int gas_used: Amount of gas used by this specific transaction alone
    :param int cumulative_gas_used: Total amount of gas used after this transaction was included in the block
    :param str contract_address: Contract address create if transaction was a contract create transaction, else null
    :param int block_number: Number of the block containing this transaction
    :param int timestamp: Unix time at the at this transactions blocks
    :param int transaction_index: Position of this transaction in the transaction list of this block
    """
    __tablename__ = 'receipts'

    transaction_hash = Column(String(66),
                              ForeignKey('transactions.transaction_hash'),
                              primary_key=True, index=True)
    status = Column(Boolean, nullable=True)
    gas_used = Column(Integer, nullable=False)
    cumulative_gas_used = Column(Integer, nullable=False)
    contract_address = Column(String(42))
    block_number = Column(Integer, ForeignKey('blocks.block_number'))
    timestamp = Column(TIMESTAMP)
    transaction_index = Column(Integer, nullable=False)

    def to_dict(self):
        return {
            'transaction_hash': self.transaction_hash,
            'status': self.status,
            'gas_used': self.gas_used,
            'cumulative_gas_used': self.cumulative_gas_used,
            'contract_address': self.contract_address,
            'block_number': self.block_number,
            'timestamp': self.timestamp,
            'transaction_index': self.transaction_index
            }

    def __repr__(self):
        return "<Receipt {}>".format(self.transaction_hash)

    @classmethod
    def add_receipt(cls, receipt_data, block_number, timestamp):
        """
        Creates a new receipt object from data received from JSON-RPC call
        eth_getTransactionReceipt.

        :param dict receipt_data: receipt data received from JSON RPC callable
        :param int timestamp: timestamp of the block where this transaction was included
        """
        if block_number > constants.FORK_BLOCK_NUMBER['Byzantium']:
            status = bool(utils.parse_int_or_hex(receipt_data['status']))
        else:
            status = None

        receipt = cls(transaction_hash=receipt_data['transactionHash'],
                      status=status,
                      gas_used=int(utils.parse_int_or_hex(receipt_data['gasUsed'])),
                      cumulative_gas_used=int(utils.parse_int_or_hex(receipt_data['cumulativeGasUsed'])),
                      contract_address=receipt_data['contractAddress'],
                      block_number=block_number,
                      timestamp=timestamp,
                      transaction_index=int(utils.parse_int_or_hex(receipt_data['transactionIndex'])))

        return receipt
