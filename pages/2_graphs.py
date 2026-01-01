import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as md
import datetime as dt

if "plot_type" not in st.session_state:
    st.session_state.plot_type = ""
if "plot_commodity1" not in st.session_state:
    st.session_state.plot_commodity1 = ""
if "plot_commodity2" not in st.session_state:
    st.session_state.plot_commodity2 = ""
if "plot_price" not in st.session_state:
    st.session_state.plot_price = ""

def _choosers():
    st.session_state.plot_type = st.selectbox("Plot type:", ["Single price", "Both prices", "Commodity comparison"])

    if st.session_state.plot_type != "Both prices":
        st.session_state.plot_price = st.selectbox("Price type", ["Buy price", "Sell price"])

    st.session_state.plot_commodity1 = st.selectbox("Commodity:", st.session_state.exchange.commodity_names)

    if st.session_state.plot_type == "Commodity comparison":
        st.session_state.plot_commodity1 = st.selectbox("Second commodity:", st.session_state.exchange.commodity_names)

def _single_plot() -> plt.Figure:
    t = [dt.datetime.fromtimestamp(h["time"]) for h in st.session_state.exchange[st.session_state.plot_commodity1].history]
    p = [h["sell" if st.session_state.plot_price == "Sell price" else "buy"] for h in st.session_state.exchange[st.session_state.plot_commodity1].history]

    fig,ax = plt.subplots(figsize=(15,7))
    fig.autofmt_xdate(rotation=25)
    xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
    ax.xaxis.set_major_formatter(xfmt)
    ax.plot(t, p, label=st.session_state.plot_commodity1)
    ax.legend()
    return fig

_choosers()
st.pyplot(_single_plot())