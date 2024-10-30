import pandas
import streamlit as st
import os
import data
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Epitope Analisys")
st.write("Tool used to comapre similarities in epitopes of biomarkers with different species origin")

st.header("Data selection")


def file_selector1(folder_path='human'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select first file', filenames)
    return os.path.join(folder_path, selected_filename)

def file_selector2(folder_path='mouse'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select second file', filenames)
    return os.path.join(folder_path, selected_filename)

filename1 = file_selector1()
st.write('You selected `%s`' % filename1)

filename2 = file_selector2()
st.write('You selected `%s`' % filename2)

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
    comparisons = pandas.DataFrame(st.session_state.comparison)
    comparisons.columns = ['similarity', 'seq1', 'seq2']
    # Count occurrences of each similarity
    similarity_counts = comparisons['similarity'].value_counts().reset_index()
    similarity_counts.columns = ['similarity', 'count']

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='similarity', y='count', data=similarity_counts, ax=ax)
    ax.set_xlabel('Similarity')
    ax.set_ylabel('Number of Occurrences')
    ax.set_title('Box Plot of Similarity vs. Number of Occurrences')
    st.pyplot(fig)