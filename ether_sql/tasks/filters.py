import logging
from celery.utils.log import get_task_logger
from web3.utils.encoding import to_int
from ether_sql.globals import get_current_session
from ether_sql.tasks.worker import app
from ether_sql.tasks.scrapper import add_block_number
from ether_sql.models.block_task_meta import BlockTaskMeta


logger = get_task_logger(__name__)


@app.task()
def new_blocks():
    """
    Celery beat task which runs every second to get new blocks.

    :param block_filter: block filter as described in session.py
    """
    current_session = get_current_session()
    block_hashes = current_session.block_filter.get_new_entries()
    for block_hash in block_hashes:
        block_data = current_session.w3.eth.getBlock(block_hash)
        block_number = to_int(block_data['number'])

        BlockTaskMeta.get_tasks_from_block_number(block_number)

        r = add_block_number.delay(block_number)
        BlockTaskMeta.add_block_task_pending(r.id, block_number)
    logger.info(block_hashes)
