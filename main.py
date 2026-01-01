#pylint: disable=E0401,E0611
"""Main app module"""

import streamlit as st
from burse import Exchange
from burse import Commodity

def _load_commodities():
    with open("config/commodities.csv", "r", encoding="utf8") as f:
        for line in f.readlines():
            name, buy, sell = line[:-1].split(",")
            st.session_state.exchange.add_commodity(Commodity(name, float(buy), float(sell)))

if "exchange" not in st.session_state:
    st.session_state.exchange = Exchange()
    _load_commodities()

st.set_page_config(
    page_title="Burse",
    page_icon="📈"
)

st.header("Burse menu")
st.sidebar.success("Select a page")


if __name__ == "__main__":
    pass
