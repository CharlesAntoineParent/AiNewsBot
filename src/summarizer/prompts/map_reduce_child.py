"""This module contains the map-reduce prompt for explain like i'm five."""

from summarizer.prompts.map_reduce_base import MapReduceBase


class MapReduceChild(MapReduceBase):
    """This class is the map-reduce prompt for explain like i'm five."""

    @staticmethod
    def get_reduce(content: str) -> list[dict[str, str]]:
        """Return reduce prompt."""
        system_role = "You are summarizing a popular paper randomly taken from the internet to a group of people intersted in AI. I want you to explain it to them as if they were five years old."
        user = f"Based on the following pages taken from a pdf, construct a summary of the paper. \n {content}"

        return [{"role": "system", "content": system_role}, {"role": "user", "content": user}]

    @staticmethod
    def get_map(summarized_content: list[str]) -> list[dict[str, str]]:
        """Return map prompt."""
        system_role = "You are given a list of summarization of multiple section of a AI paper. Create a summarization of the whole paper for a group of people intersted in AI. I want you to explain it to them as if they were five years old."

        user = "Here are the summarization of the different sections of the paper: \n" + "\n".join(
            summarized_content
        )
        return [{"role": "system", "content": system_role}, {"role": "user", "content": user}]
