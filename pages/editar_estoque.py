import streamlit as st
from database import Products
from sqlalchemy import update

conn = st.connection('postgres', type='sql')
col1, col2 = st.columns(2)

with col1.form(key='create_form', border=True, clear_on_submit=True) as form:
    st.subheader('Criar novo produto')
    product_name = st.text_input('Nome do Produto')
    quantity = st.number_input('Quantidade em estoque', min_value=0)
    unit_value = st.number_input('Valor Unitário', min_value=0.0)

    submit_button = st.form_submit_button('Cadastrar')

    if submit_button:
        with conn.session as session:
            session.add(Products(
                product_name=product_name,
                quantity = quantity,
                unit_value = unit_value
            ))
            session.commit()

with col2.form(key='editing_form', border=True, clear_on_submit=True):
    with conn.session as session:
        all_products = session.query(Products).all()

    st.subheader('Editar Produto no Estoque')
    format_func = lambda x: 'Nome do Produto' if x == 'product_name' else 'Quantidade em Estoque' if x == 'quantity' else 'Valor Unitário'
    product_to_be_edited = st.selectbox('Produto a ser Editado:', options=[product_.product_name for product_ in all_products])
    selected_field = st.selectbox('Coluna a ser editada:', options=['product_name', 'quantity', 'unit_value'], format_func=format_func)
    new_value = st.text_input('Novo Valor')
    
    submit_button = st.form_submit_button('Editar')

    if submit_button:
        with conn.session as session:
            if selected_field == 'product_name':
                statement = update(Products).where(Products.product_name == product_to_be_edited).values(product_name=new_value)
            elif selected_field == 'quantity':
                statement = update(Products).where(Products.product_name == product_to_be_edited).values(quantity=new_value)
            else:
                statement = update(Products).where(Products.product_name == product_to_be_edited).values(unit_value=new_value)
                
            session.execute(statement)
            session.commit()
