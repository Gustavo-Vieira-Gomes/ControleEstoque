import streamlit as st
from database import Products, Vendas
import pandas as pd
from sqlalchemy import create_engine



conn = st.connection('postgres', type='sql')

with conn.session as session:
    products = session.query(Products).all()

num_products = len(products) if len(products) != 0 else 1

st.header('FEEDBACK DE VENDAS')

df_sales = pd.read_sql_table('historico_de_vendas', con=create_engine(st.secrets['connections']['postgres']['url']))

product_keys = {'COCA-COLA': 'coca_cola', 'ÁGUA': 'agua', 'GUARANÁ':'guarana', 'ICE TEA PÊSSEGO': 'ice_tea_pessego', 'ICE TEA LIMÃO': 'ice_tea_limao', 'SUCO': 'suco', 'CERVEJA': 'cerveja', 'GUARAVITA':'guaravita'}

with st.expander(expanded=True, label='Produtos em Estoque'):
    product_columns = st.columns(3, vertical_alignment='top') if num_products >= 3 else st.columns(num_products, vertical_alignment='center')
    for  index, product in enumerate(products):
        total_sales_units = df_sales[product_keys[product.product_name]].sum()
        total_sales_value = total_sales_units * product.unit_value
        with product_columns[index % 3].container(border=True):
            st.write(product.product_name)
            st.write(f'Em estoque: {product.quantity} unidades')
            st.write(f'Unidades Vendidas: {total_sales_units}')
            st.write(f'Valor Unitário: R${product.unit_value:.2f}'.replace('.', ','))
            st.write(f'Faturamento: R${total_sales_value:.2f}'.replace('.', ','))

with st.expander(expanded=True, label='Registro de Vendas'):
    total_sales_value = df_sales['total_value'].sum()
    with st.container(border=True):
        st.write('Faturamento Total')
        st.write(f'R${total_sales_value:.2f}'.replace('.', ','))
    df_sales.set_index('id', inplace=True)
    st.dataframe(df_sales, use_container_width=True, height=200,
                 column_config={
                     'id': st.column_config.NumberColumn('Nº da Venda'),
                     'coca_cola': st.column_config.NumberColumn('COCA-COLA'),
                     'agua': st.column_config.NumberColumn('ÁGUA'),
                     'guarana': st.column_config.NumberColumn('GUARANÁ'),
                     'ice_tea_pessego': st.column_config.NumberColumn('ICE TEA PÊSSEGO'),
                     'ice_tea_limao': st.column_config.NumberColumn('ICE TEA LIMÃO'),
                     'suco': st.column_config.NumberColumn('SUCO'),
                     'cerveja': st.column_config.NumberColumn('CERVEJA'),
                     'guaravita': st.column_config.NumberColumn('GUARAVITA'),
                     'total_value': st.column_config.NumberColumn('VALOR DA VENDA')
                 })
