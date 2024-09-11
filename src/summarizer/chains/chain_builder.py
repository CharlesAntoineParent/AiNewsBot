"""This module implements a builder for the chain."""
import os
from pathlib import Path
from typing import Any, ClassVar, Optional

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from omegaconf import OmegaConf

from summarizer.chains.base_chain import BaseChain
from summarizer.chains.map_reduce import MapReduceChain
from summarizer.models.gpt_models import GPT4oMini, GPTModel
from summarizer.prompts import MapReduceBase, MapReduceChild, MapReduceNormal


class ChainFactory:
    """Factory class for creating chains."""

    _chain_registry: ClassVar[dict[str, BaseChain]] = {MapReduceChain.__name__: MapReduceChain}
    _model_registry: ClassVar[dict[str, GPTModel]] = {GPT4oMini.name: GPT4oMini}
    _prompt_registry: ClassVar[dict[str, MapReduceBase]] = {
        MapReduceBase.__name__: MapReduceBase,
        MapReduceChild.__name__: MapReduceChild,
        MapReduceNormal.__name__: MapReduceNormal,
    }

    @classmethod
    def create_chain(cls, name: str, **kwargs) -> BaseChain:
        """Creates an instance of a chain based on the registered name.

        Args:
            name (str): The name of the chain class to create.
            **kwargs: Additional parameters to pass to the chain class constructor.

        Returns:
            BaseChain: An instance of the requested chain class.

        Raises:
            ValueError: If the chain class is not registered.
        """
        if name not in cls._chain_registry:
            msg = f"Chain class '{name}' is not registered."
            raise ValueError(msg)
        return cls._chain_registry[name](**kwargs)

    @classmethod
    def create_model(cls, name: str, **kwargs) -> GPTModel:
        """Creates an instance of a model based on the registered name.

        Args:
            name (str): The name of the model class to create.
            **kwargs: Additional parameters to pass to the model class constructor.

        Returns:
            GPTModel: An instance of the requested model class.

        Raises:
            ValueError: If the model class is not registered.
        """
        if name not in cls._model_registry:
            msg = f"Model class '{name}' is not registered."
            raise ValueError(msg)
        return cls._model_registry[name](**kwargs)

    @classmethod
    def create_prompt(cls, name: str, **kwargs) -> MapReduceBase:
        """Creates an instance of a prompt based on the registered name.

        Args:
            name (str): The name of the prompt class to create.
            **kwargs: Additional parameters to pass to the prompt class constructor.

        Returns:
            MapReduceBase: An instance of the requested prompt class.

        Raises:
            ValueError: If the prompt class is not registered.
        """
        if name not in cls._prompt_registry:
            msg = f"Prompt class '{name}' is not registered."
            raise ValueError(msg)
        return cls._prompt_registry[name](**kwargs)

    @classmethod
    def build_chain(cls, config_dict: dict[str, Any]) -> BaseChain:
        """Build the chain."""
        model_name = config_dict.get("model")
        model_params = config_dict.get("model-parameters")
        model = cls.create_model(model_name, **model_params)
        prompt_name = config_dict.get("prompt")
        prompt_params = config_dict.get("prompt-parameters")
        prompt = (
            cls.create_prompt(prompt_name, **prompt_params)
            if prompt_params
            else cls.create_prompt(prompt_name)
        )
        chain_name = config_dict.get("chain")
        chain_params = config_dict.get("chain-parameters")
        chain = (
            cls.create_chain(chain_name, model=model, prompt=prompt, **chain_params)
            if chain_params
            else cls.create_chain(chain_name, model=model, prompt=prompt)
        )
        return chain

    @classmethod
    def build_chain_from_yaml(cls, config_path: Path) -> BaseChain:
        """Build the chain from a YAML file.

        Args:
            config_path (Path): The path to the YAML configuration file.

        Returns:
            BaseChain: The chain instance.
        """
        config = OmegaConf.load(config_path)
        config_dict = OmegaConf.to_container(config, resolve=True)
        return cls.build_chain(config_dict)


class ChainBuilder:
    """This class builds the chain."""

    @staticmethod
    def build_chain(config_dict: dict[str, str]) -> BaseChain:
        """Build the chain."""
        api_key = ChainBuilder._get_api_key(config_dict)
        try:
            model_cls = config_dict.summarizer.get("model")
            model = model_cls(api_key=api_key)
        except KeyError as exc:
            msg = "Missing or bad model class in config."
            raise BadConfigError(msg) from exc
        try:
            prompt_cls = config_dict.summarizer.get("prompt")
            prompt = prompt_cls()
        except KeyError as exc:
            msg = "Missing or bad prompt class in config."
            raise BadConfigError(msg) from exc

        try:
            chain_cls = config_dict.summarizer.get("chain")
            chain = chain_cls(model=model, prompt=prompt)
        except KeyError as exc:
            msg = "Missing or bad chain class in config."
            raise BadConfigError(msg) from exc

        return chain

    @staticmethod
    def _get_api_key(self, config_dict: dict[str, str]) -> str:
        """Get the OpenAI API key."""
        openai_env_var_name = config_dict.secrets.get("env_var_openai_name")
        kv_url = config_dict.secrets.get("env_var_openai_name")
        kv_openai_secrets_name = config_dict.secrets.get("keyvault_openai_secret_name")
        api_key = None
        if openai_env_var_name is not None:
            api_key = os.getenv(openai_env_var_name)
        elif kv_url is not None and kv_openai_secrets_name is not None:
            api_key = ChainBuilder._get_secret_from_keyvault(kv_url, kv_openai_secrets_name)

        if api_key is None:
            msg = "API key not found in environment variables or keyvault."
            raise BadConfigError(msg)

        return api_key

    @staticmethod
    def _get_secret_from_keyvault(kv_url: str, secret_name: str) -> Optional[str]:
        """Return the OpenAI API key from azure vault.

        Args:
            kv_url (str): URI of the azure keyvault.
            secret_name (str): Name of the secret.

        Returns:
            str: secret value
        """
        credential = DefaultAzureCredential()
        secret_client = SecretClient(vault_url=kv_url, credential=credential)
        secret = secret_client.get_secret(secret_name)
        return secret.value


class BadConfigError(Exception):
    """Custom exception for ChainBuilder errors."""
