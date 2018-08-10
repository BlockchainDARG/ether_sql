import logging
from sqlalchemy import Column, String, Numeric, TIMESTAMP, Text, Integer
from sqlalchemy import func, and_
from web3.utils.encoding import (to_int, to_hex)
from eth_utils import to_checksum_address
from ether_sql.models import base
from ether_sql.globals import get_current_session
logger = logging.getLogger(__name__)

class BlockTaskMeta(base):
    """
    Class mapping success or failure of block scrapper tasks.

    """
    __tablename__ = 'block_task_meta'
    id = Column(Integer, primary_key=True)
    task_id = Column(Text, nullable=True)
    task_name = Column(Text, nullable=False)
    state = Column(Text, nullable=False)
    block_number = Column(Numeric, nullable=False)
    block_hash = Column(String(66), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'task_id': self.task_id,
            'task_name': self.task_name,
            'state': self.state,
            'block_number': self.block_number,
            'block_hash': self.block_hash,
            }

    @classmethod
    def add_block_task_meta(cls, block_number, task_name, state, task_id=None, block_hash=None):
        current_session = get_current_session()
        block_task_meta = cls(task_name=task_name,
                              state=state,
                              block_number=block_number,
                              block_hash=block_hash,
                              task_id=task_id)
        with current_session.db_session_scope():
            current_session.db_session.add(block_task_meta)

    @classmethod
    def get_block_task_meta_from_task_id(cls, task_id):
        current_session = get_current_session()
        with current_session.db_session_scope():
            return current_session.db_session.query(cls).\
                    filter_by(task_id=task_id).first()

    @classmethod
    def get_block_task_meta_from_block_number(cls, block_number):
        current_session = get_current_session()
        with current_session.db_session_scope():
            return current_session.db_session.query(cls).\
                    filter_by(block_number=block_number)

    @classmethod
    def update_block_task_meta_from_block_number(cls, block_number, **kwargs):
        current_session = get_current_session()
        with current_session.db_session_scope():
            block_task_meta = current_session.db_session.query(cls).\
                    filter_by(block_number=block_number)
            for i_block_task_meta in block_task_meta:
                i_block_task_meta.__dict__.update(kwargs)
                current_session.db_session.add(i_block_task_meta)

    @classmethod
    def get_blocks_to_be_pushed_in_queue(cls):
        current_session = get_current_session()
        current_eth_blocknumber = current_session.w3.eth.blockNumber
        block_lag = current_session.settings.BLOCK_LAG
        with current_session.db_session_scope():
            query = current_session.db_session.query(cls.block_number).filter(
                and_(cls.state=='WAITING',
                     cls.block_number < current_eth_blocknumber-block_lag))
            return query.from_self().distinct()
