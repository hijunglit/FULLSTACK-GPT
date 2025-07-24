from langchain.document_loaders import SitemapLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import streamlit as st

splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=1000,
    chunk_overlap=200,
)


def page_parse(soup):
    header = soup.find("header")
    footer = soup.find("footer")
    if header:
        header.decompose()
    if footer:
        footer.decompose()
    return str(soup.get_text()).replace("\n", " ").replace("\xa0", " ")


@st.cache_data(show_spinner="Loading Website...")
def load_websites(docs):
    loader = SitemapLoader(
        url, filter_urls=[r"^(.*\/blog\/).*"], parsing_function=page_parse)
    loader.requests_per_second = 5
    docs = loader.load()
    return docs


st.set_page_config(
    page_title="SiteGPT",
    page_icon="🖥️",
)

st.markdown(
    """
    # SiteGPT
            
    Ask questions about the content of a website.
            
    Start by writing the URL of the website on the sidebar.
"""
)

with st.sidebar:
    url = st.text_input(
        "Write down a URL",
        placeholder="hppts://example.com"
    )

if url:
    if "xml" not in url:
        with st.sidebar:
            st.error("Please write down a sitemap URL")
    else:
        docs = load_websites(url)
        st.write(docs)
