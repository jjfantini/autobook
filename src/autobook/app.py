import streamlit as st
from autobook.libgen import Libgen  # Replace with your actual import


def autobook():
    # Initialize session state
    if "libgen_instance" not in st.session_state:
        st.session_state.libgen_instance = None
    if "search_results" not in st.session_state:
        st.session_state.search_results = None
    if "filtered_results" not in st.session_state:
        st.session_state.filtered_results = None

    st.header("🤖AutoBook📖")
    st.write("Generate an audio book from any book or PDF.")

    # Search query input
    query = st.text_input("Search Query", placeholder="Search Query")

    # Search button
    if st.button("Search"):
        st.session_state.libgen_instance = Libgen(q=query)
        st.session_state.libgen_instance.search()
        st.session_state.search_results = (
            st.session_state.libgen_instance.get_results()
        )

    # Always display search results if they are available
    if st.session_state.search_results is not None:
        st.dataframe(st.session_state.search_results)

    # Select row and Download button
    if st.session_state.filtered_results is not None:
        selected_row_index = st.selectbox(
            "Select a row to download:",
            range(len(st.session_state.filtered_results)),
        )
        if st.button("Download"):
            download_message = st.session_state.libgen_instance.download_file(
                selected_row_index
            )
            st.write(download_message)


if __name__ == "__main__":
    autobook()
