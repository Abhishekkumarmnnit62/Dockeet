from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader


def load_pdf(pdf_path: str):

    if not Path(pdf_path).exists():
        raise FileNotFoundError(
            f"PDF not found: {pdf_path}"
        )

    loader = PyPDFLoader(pdf_path)

    return loader.load()


if __name__ == "__main__":

    pdf_path = input("Enter PDF path: ")

    documents = load_pdf(pdf_path)

    print(
        f"Loaded {len(documents)} pages"
    )

    print(documents[0].page_content[:200])
    print(documents[0].metadata)
    print(type(documents[0]))