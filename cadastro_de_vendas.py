import streamlit as st
from database import Products, Vendas
from sqlalchemy import select, update

st.set_page_config(page_title='Cadastrar Vendas', layout='wide')

conn = st.connection('postgres', type='sql')

if not 'client_order' in st.session_state:
    st.session_state['client_order'] = {'COCA-COLA': 0, 'ÁGUA':0, 'GUARANÁ': 0, 'ICE TEA PÊSSEGO': 0,'ICE TEA LIMÃO': 0, 'SUCO': 0, 'CERVEJA': 0, 'GUARAVITA': 0}


def get_unit_values(_conn):
    with _conn.session as session:
        product_data =  session.query(Products).all()
        st.session_state['product_unit_value'] = {product.product_name:product.unit_value for product in product_data}

if 'product_unit_value' in st.session_state:
    get_unit_values(conn)

def total_client_order():
    
    total_order_value = 0
    for item in st.session_state['product_unit_value'].items():
        total_order_value += item[1] * st.session_state['client_order'][item[0]]
    return total_order_value

with st.container(border=True):
    st.header('Cadastrar Vendas')


with st.container(border=True):

    add_buttons_column, delete_buttons_column, sumary_col = st.columns(3, vertical_alignment='center')
    add_coca = add_buttons_column.button('+1 COCA-COLA')
    add_agua = add_buttons_column.button('+1 ÁGUA')
    add_guarana = add_buttons_column.button('+1 GUARANÁ')
    add_ice_pessego = add_buttons_column.button('+1 ICE TEA PÊSSEGO')
    add_ice_limao = add_buttons_column.button('+1 ICE TEA LIMÃO')
    add_suco = add_buttons_column.button('+1 SUCO')
    add_cerveja = add_buttons_column.button('+1 CERVEJA')
    add_guaravita = add_buttons_column.button('+1 GUARAVITA')

    delete_coca = delete_buttons_column.button('-1 COCA-1COLA')
    delete_agua = delete_buttons_column.button('-1 ÁGUA')
    delete_guarana = delete_buttons_column.button('-1 GUARANÁ')
    delete_ice_pessego = delete_buttons_column.button('-1 ICE TEA PÊSSEGO')
    delete_ice_limao = delete_buttons_column.button('-1 ICE TEA LIMÃO')
    delete_suco = delete_buttons_column.button('-1 SUCO')
    delete_cerveja = delete_buttons_column.button('-1 CERVEJA')
    delete_guaravita = delete_buttons_column.button('-1 GUARAVITA')
    
    if add_coca:
        st.session_state['client_order']['COCA-COLA'] += 1
    
    if add_agua:
        st.session_state['client_order']['ÁGUA'] += 1
    
    if add_guarana:
        st.session_state['client_order']['GUARANÁ'] += 1
    
    if add_ice_pessego:
        st.session_state['client_order']['ICE TEA PÊSSEGO'] += 1

    if add_ice_limao:
        st.session_state['client_order']['ICE TEA LIMÃO'] += 1

    if add_suco:
        st.session_state['client_order']['SUCO'] += 1

    if add_cerveja:
        st.session_state['client_order']['CERVEJA'] += 1

    if add_guaravita:
        st.session_state['client_order']['GUARAVITA'] += 1

    if delete_coca:
        if st.session_state['client_order']['COCA-COLA'] > 0:
            st.session_state['client_order']['COCA-COLA'] -= 1
    
    if delete_agua:
        if st.session_state['client_order']['ÁGUA'] > 0:
            st.session_state['client_order']['ÁGUA'] -= 1
    
    if delete_guarana:
        if st.session_state['client_order']['GUARANÁ'] > 0:
            st.session_state['client_order']['GUARANÁ'] -= 1
    
    if delete_ice_pessego:
        if st.session_state['client_order']['ICE TEA PÊSSEGO'] > 0:
            st.session_state['client_order']['ICE TEA PÊSSEGO'] -= 1

    if delete_ice_limao:
        if st.session_state['client_order']['ICE TEA LIMÃO'] > 0:
            st.session_state['client_order']['ICE TEA LIMÃO'] -= 1

    if delete_suco:
        if st.session_state['client_order']['SUCO'] > 0:
            st.session_state['client_order']['SUCO'] -= 1

    if delete_cerveja:
        if st.session_state['client_order']['CERVEJA'] > 0:
            st.session_state['client_order']['CERVEJA'] -= 1

    if delete_guaravita:
        if st.session_state['client_order']['GUARAVITA'] > 0:
            st.session_state['client_order']['GUARAVITA'] -= 1

    sumary_col.subheader('Pedido Atual')
    for item, quantity in st.session_state['client_order'].items():
        sumary_col.write(f'{item} - {quantity}')

    total_order_value = total_client_order()
    sumary_col.subheader(f'Total da Venda: R${total_order_value:.2f}'.replace('.', ','))

    confirm_button = sumary_col.button('Concluir venda')

    if confirm_button:


        with conn.session as session:

            for item in st.session_state['client_order'].keys():
                if st.session_state['client_order'][item] != 0:
                    product_data = session.query(Products).filter(Products.product_name == item).scalar()
                    statement2 = update(Products).where(Products.product_name == item).values(quantity=product_data.quantity-st.session_state['client_order'][item])
                    session.execute(statement2)
                    session.commit()
            

            session.add(
                Vendas(
                    coca = st.session_state['client_order']['COCA-COLA'],
                    agua = st.session_state['client_order']['ÁGUA'],
                    guarana = st.session_state['client_order']['GUARANÁ'],
                    ice_tea_pessego = st.session_state['client_order']['ICE TEA PÊSSEGO'],
                    ice_tea_limao = st.session_state['client_order']['ICE TEA LIMÃO'],
                    suco = st.session_state['client_order']['SUCO'],
                    cerveja = st.session_state['client_order']['CERVEJA'],
                    guaravita = st.session_state['client_order']['GUARAVITA'],
                    total_value = total_order_value
                )
            )

            session.commit()

        st.session_state['client_order'] = {'COCA-COLA': 0, 'ÁGUA':0, 'GUARANÁ': 0, 'ICE TEA PÊSSEGO': 0,'ICE TEA LIMÃO': 0, 'SUCO': 0, 'CERVEJA': 0, 'GUARAVITA': 0}
        st.rerun()