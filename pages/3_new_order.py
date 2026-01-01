#pylint: disable=E0401,C0301,C0103
"""Page that allows user to create new order"""

from random import randint
import streamlit as st

st.set_page_config(
    page_title="Order",
    page_icon="🗒"
)

def _random_order_number(length: int = 10) -> str:
    num = "Q"
    for _ in range(length):
        num += str(randint(0, 9))
    return num

if "current_order" not in st.session_state:
    st.session_state.current_order = []
if "current_order_number" not in st.session_state:
    st.session_state.current_order_number = _random_order_number()

def _display_order_list(prices: dict):
    st.header(f"Order {st.session_state.current_order_number}")
    col1, col2, col3 = st.columns(3)
    total = 0
    with col1:
        st.subheader("Commodity")
    with col2:
        st.subheader("Amount")
    with col3:
        st.subheader("Price")
    for trade in st.session_state.current_order:
        com, am = trade
        with col1:
            st.write(com)
        with col2:
            st.write(am)
        with col3:
            price = am * (prices[com][0] if am < 0 else prices[com][1])
            st.write(f"{price:.2f}")
            total = total + price
    with col1:
        st.subheader("Total:")
    with col3:
        st.subheader(f"{total:.2f}")

def _trade_adder(prices: dict):
    col1, col2, col3 = st.columns(3)
    with col1:
        new_com = st.selectbox("Commodity", prices.keys())
    with col2:
        am = st.number_input("Amount", step=1)
    with col3:
        st.write(f"Price: {am * (prices[new_com][0] if am < 0 else prices[new_com][1]):.2f}")
    if st.button("Add trade"):
        st.session_state.current_order.append((new_com, am))
        st.rerun()


_display_order_list(st.session_state.exchange.current_prices)
_trade_adder(st.session_state.exchange.current_prices)
if st.button("Send Order"):
    for tr in st.session_state.current_order:
        commodity, amount = tr
        if amount < 0:
            st.session_state.exchange.add_trade(commodity, True, - 1 * amount)
        else:
            st.session_state.exchange.add_trade(commodity, False, -1 * amount)
    st.session_state.current_order = []
    st.session_state.current_order_number = _random_order_number()
    st.rerun()
