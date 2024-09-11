"""This module implements the map reduce chain."""
import langchain
from langchain.document_loaders import PyPDFLoader

from summarizer.chains.base_chain import BaseChain
from summarizer.models.base_model import BaseLLM
from summarizer.prompts.map_reduce_base import MapReduceBase


class MapReduceChain(BaseChain):
    """Map reduce chain."""

    prompt: MapReduceBase
    model: BaseLLM
    text_buffer: int = 1000

    def run_chain(self, pdf_url: str) -> str:
        """Return prediction from model."""
        docs = self.load_document_page(pdf_url)
        map_out = self.create_document_chunk(docs)
        reduce_out = self.run_reduce(map_out)
        map_out: str = self.run_map(reduce_out)
        return map_out

    def run_reduce(self, content: list[str]) -> list[str]:
        """Return prediction from model."""
        predictions = []
        for chunk in content:
            prompt = self.prompt.get_reduce(chunk)
            map_response = self.model.predict(prompt)
            predictions.append(map_response)
        return predictions

    def run_map(self, content: list[str]) -> str:
        """Return prediction from model."""
        prompt = self.prompt.get_map(content)
        map_response = self.model.predict(prompt)
        return map_response

    def load_document_page(self, document_url: str) -> list[langchain.schema.document.Document]:
        """Return document chunk."""
        loader = PyPDFLoader(document_url)
        return loader.load_and_split()

    def create_document_chunk(
        self, doc_content: list[langchain.schema.document.Document]
    ) -> list[str]:
        """Return document chunk."""
        chunk = []
        content = ""
        nb_token = 0
        for page in doc_content:
            nb_token_page = self.model.count_tokens(page.page_content)
            if nb_token + nb_token_page < self.model.max_token - self.text_buffer:
                content += "\n" + page.page_content
                nb_token += self.model.count_tokens(page.page_content)
            else:
                chunk.append(content)
                content = "\n" + page.page_content
                nb_token = nb_token_page
        chunk.append(content)
        return chunk
