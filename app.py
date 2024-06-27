import streamlit as st
import os
import time
import data

st.title("Epitope Analisys")
st.text("Tool used to comapre similarities in epitopes of biomarkers of different species origin")

st.sidebar.header("Data selection")


def file_selector1(folder_path='human'):
    filenames = os.listdir(folder_path)
    selected_filename = st.sidebar.selectbox('Select first file', filenames)
    return os.path.join(folder_path, selected_filename)

def file_selector2(folder_path='mouse'):
    filenames = os.listdir(folder_path)
    selected_filename = st.sidebar.selectbox('Select second file', filenames)
    return os.path.join(folder_path, selected_filename)

filename1 = file_selector1()
st.sidebar.write('You selected `%s`' % filename1)

filename2 = file_selector2()
st.sidebar.write('You selected `%s`' % filename2)

def generateComaprison():
    with st.spinner('Wait for it...'):
        data_human = data.extract_sequences(data.load_json(filename1))
        data_mouse = data.extract_sequences(data.load_json(filename2))
        comparison = data.compare_sequences(data_human, data_mouse)
        st.success('Done!')
        return comparison

if 'comparison' not in st.session_state:
    st.session_state.comparison = None

if st.button("Generate Alignment"):
    st.session_state.comparison = generateComaprison()

if st.session_state.comparison is not None:
    st.dataframe(st.session_state.comparison)
    st.bar_chart(st.session_state.comparison, x ="0")