from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String, Integer, Float, Column, create_engine
import streamlit as st

class BaseClass(DeclarativeBase):
    pass

class Products(BaseClass):
    __tablename__ = 'estoque_de_produtos'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    product_name = Column('product_name', String(40), nullable=False)
    quantity = Column('quantity', Integer, nullable=False)
    unit_value = Column('unit_value', Float)

class Vendas(BaseClass):
    __tablename__ = 'historico_de_vendas'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    coca = Column('coca_cola', Integer)
    agua = Column('agua', Integer)
    guarana = Column('guarana', Integer)
    ice_tea_pessego = Column('ice_tea_pessego', Integer)
    ice_tea_limao = Column('ice_tea_limao', Integer)
    suco = Column('suco', Integer)
    cerveja = Column('cerveja', Integer)
    guaravita = Column('guaravita', Integer)
    total_value = Column('total_value', Float)


BaseClass.metadata.create_all(create_engine(st.secrets['connections']['postgres']['url']))


