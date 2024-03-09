import logging
from sqlalchemy import (
    Table, MetaData, Column, Integer, Float, String, Date, ForeignKey,
    event,
)
from sqlalchemy.orm import registry, mapper, relationship

from invoice.domain import model

logger = logging.getLogger(__name__)

metadata = MetaData()
mapper_registry = registry()

invoices = Table('invoices', metadata,
                 Column('id', Integer, primary_key=True, autoincrement=True),
                 Column('email', String(255)),
                 Column('amount', Float),
                 schema='public'          
)

def start_mappers():
    logger.info('Starting mappers')
    mapper_registry.map_imperatively(model.Invoice, invoices)