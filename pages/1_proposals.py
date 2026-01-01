#pylint: disable=E0401,C0301,C0103
"""Page that displays all commodities current prices"""

import streamlit as st

st.set_page_config(
    page_title="Burse prices",
    page_icon="📈"
)

st.header("Proposals list")

def _add_commodity_prices(prices: dict):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Commodity")
    with col2:
        st.write("Buy price")
    with col3:
        st.write("Sell price")
    for com, pr in prices.items():
        with col1:
            st.write(com)
        with col2:
            st.write(f"{pr[0]:.2f}")
        with col3:
            st.write(f"{pr[1]:.2f}")


_add_commodity_prices(st.session_state.exchange.current_prices)
if st.button("shuffle"):
    st.session_state.exchange.random_price_movement_all()
