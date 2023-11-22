import streamlit as st
from autobook.core.helpers import dataframe_with_selections
from autobook.libgen import Libgen  # Replace with your actual import


def autobook():
    # Initialize session state
    if "libgen_instance" not in st.session_state:
        st.session_state.libgen_instance = None
    if "search_results_df" not in st.session_state:
        st.session_state.search_results_df = None
    if "filtered_results_df" not in st.session_state:
        st.session_state.filtered_results_df = None

    header_containter = st.container()
    with header_containter:
        st.header("🤖AutoBook📖")
        st.write("Generate an audio book from any book or PDF.")

    # Search query input and button on the same line
    container = st.container()
    with container:
        col1, col2 = st.columns(2)
        with col1:
            query = st.text_input("Find a Book", placeholder="Search Query")
        with col2:
            if st.button("Search🔮"):
                st.session_state.libgen_instance = Libgen(q=query)
                st.session_state.libgen_instance.search()
                st.session_state.search_results_df = (
                    st.session_state.libgen_instance.get_df()
                )

    # Always display search results if they are available
    if st.session_state.search_results_df is not None:
        with st.container():
            # Display the dataframe with selections
            selection = dataframe_with_selections(
                st.session_state.search_results_df
            )
            # Only show dataframe if there is a checkbox selected
            st.write("You selected the following book to download:")
            st.write(selection)


if __name__ == "__main__":
    autobook()
