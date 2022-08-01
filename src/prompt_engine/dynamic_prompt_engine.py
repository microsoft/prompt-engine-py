### This is a pattern on top of prompt engine which can be used to dynamically generate prompts based on the user input.
### This patterns works by computing embeddings of previous examples that were provided to it and the current user input
### It retrieves the most relevant examples from the embedding space and uses them to generate a prompt
### This can help in generating prompts that are more relevant to the user input and result in a better output from the language model
### This can also help coax multiple behaviors from the language model and bypass the need for maintaining different prompts for each behavior

from prompt_engine.prompt_engine import PromptEngine, PromptEngineConfig
from prompt_engine.interaction import Interaction
from prompt_engine.prompt_engine import get_encoder
import openai
from pathlib import Path
from typing import List, Dict
from openai.embeddings_utils import (
    get_embedding,
    distances_from_embeddings,
    indices_of_nearest_neighbors_from_distances,
)
import os
import pandas as pd
import pickle
import string 

class OpenAIEmbedding:
    def __init__(self, cache_location: str = os.getcwd()):
        """
        This function initializes the OpenAI service
        """
        # load the cache if it exists, and save a copy to disk
        if (os.path.exists("cache") == False):
            os.mkdir("cache")

        self.cache_path = os.path.join(cache_location, "embeddings_cache.pkl")

        # load the cache if it exists
        try:
            self.embedding_cache = pd.read_pickle(self.cache_path)
        except FileNotFoundError:
            self.embedding_cache = {}

        # Store the embedding cache in a pickle file
        with open(self.cache_path, "wb") as embedding_cache_file:
            pickle.dump(self.embedding_cache, embedding_cache_file)
    
    def embedding_from_string(self, string: str, example: Interaction = None, engine: str = "text-similarity-davinci-001", embedding_cache=None, query = False):
        """Return embedding of given string, using a cache to avoid recomputing."""
        
        # Make a temp Interaction object to get its embedding while building a prompt
        if example is None:
            example = Interaction(input=string, response="")

        # If the embedding cache is not provided, use the default one
        if embedding_cache is None:
            embedding_cache = self.embedding_cache

        # if the embedding is already in the cache, return it, otherwise compute it
        if (string, engine) not in embedding_cache.keys() or (embedding_cache[(string, engine)][1].response == "" and query == False):
            print (f"Computing embedding for unseen interaction!")
            success, embedding = self.get_embedding_with_retries(string, engine)
            if success:
                embedding_cache[(string, engine)] = [embedding, example]
                with open(self.cache_path, "wb") as embedding_cache_file:
                    pickle.dump(embedding_cache, embedding_cache_file)

                return embedding_cache[(string, engine)]
            else:
                return None
        
        else:
            return embedding_cache[(string, engine)]

    def get_embedding_with_retries(self, text, engine, retries = 3):
        """
        This function is used to get the embedding of a string from OpenAI. It is used to handle the case where the API is rate limited.
        """
        try:
            if retries > 0:
                return True, get_embedding(text, engine)
        except openai.error.RateLimitError:
            if retries > 0:
                return self.get_embedding_with_retries(text, engine, retries - 1)
            else:
                print('\n\n# OpenAI API error: Rate limit exceeded, try later')
                return False, None
        except openai.error.APIConnectionError:
            if retries > 0:
                return self.get_embedding_with_retries(text, engine, retries - 1)
            else:
                print('\n\n# OpenAI API error: API connection error, are you connected to the internet?')
                return False, None
        except openai.error.InvalidRequestError as e:
            print('\n\n# OpenAI API error: Invalid request - ' + str(e))
            return False, None
        except Exception as e:
            print('\n\n# OpenAI API error: Unexpected exception - ' + str(e))
            return False, None

    def get_recommendations_from_strings(self, source_string: int, k_nearest_neighbors: int = 3, engine="text-similarity-davinci-001"):
        """Print out the k nearest neighbors of a given string."""

        all_embeddings_except_empty = [x for x in self.embedding_cache.values() if x[1].response != ""]

        # get embeddings for all strings
        embeddings:List[List] = [em[0] for em in all_embeddings_except_empty]

        # get the embedding of the source string
        query_embedding = self.embedding_from_string(source_string, Interaction(input=source_string, response=""), engine=engine, query=True)[0]
        if query_embedding is None:
            raise Exception("Could not get embedding for source string, please try again")

        # get distances between the source embedding and other embeddings (function from embeddings_utils.py)
        distances = distances_from_embeddings(query_embedding, embeddings, distance_metric="cosine")

        # get indices of nearest neighbors (function from embeddings_utils.py)
        indices_of_nearest_neighbors = indices_of_nearest_neighbors_from_distances(distances)

        return [all_embeddings_except_empty[i][1] for k, i in enumerate(indices_of_nearest_neighbors) if k<k_nearest_neighbors]


class PromptBank:
    """
    This class provides a bank of prompts for the Chat Engine
    """
    def __init__(self):
        # Examples is a list of interactions
        self.openaiservice = OpenAIEmbedding()

    # Returns a list of interactions that are similar to the given interaction
    def retrieve_matched_prompts(self, query: str, limit: int = 5):
        """
        This function retrieves the prompts that match the query
        """

        relevantExamples = self.openaiservice.get_recommendations_from_strings(source_string = query, k_nearest_neighbors = limit)
        return relevantExamples


class DynamicPromptEngine(PromptEngine):
    """
    Chat Engine provides a PromptEngine to construct chat-like prompts for large scale language model inference
    """

    def __init__(self, openai_key: str, config: PromptEngineConfig = PromptEngineConfig(), description: str = "", examples: list = [], flow_reset_text = "", dialog: list = [], prompt_bank: PromptBank = PromptBank()):
        """
        Initializes the Dynamic Prompt Engine
        """
        self.config = config
        self.description = description
        self.examples = examples
        self.flow_reset_text = flow_reset_text
        self.dialog = dialog
        self.context: str = ""
        
        # Set the auth key for the OpenAI service
        openai.api_key = openai_key

        # Initialize the prompt bank
        self.prompt_bank = prompt_bank

        # If there are examples, add them to the embedding cache
        if (self.examples != []):
            self.__add_examples_to_embedding_cache(self.examples, self.description)

        self.encoder = get_encoder()
    
    # Overriding the _insert_examples function from the PromptEngine class to achieve the dynamic prompt engine behavior
    def _insert_examples(self, context: str = "", user_input: str = ""):
        """
        Inserts the examples into the context
        """
        temp_examples_text = ""
        if user_input == "":
            examples = self.examples
        else:
            processed_embedding_query_text = self.preprocess_for_embedding_computation(self.description, user_input)
            examples = self.prompt_bank.retrieve_matched_prompts(processed_embedding_query_text)
        if (examples != []):
            for example in examples:
                temp_example_text = self.config.input_prefix + example.input + self.config.input_postfix + self.config.newline_operator
                temp_example_text += self.config.output_prefix +  example.response + self.config.output_postfix +  self.config.newline_operator*2
            
                if (self._assert_token_limit(context + temp_example_text, user_input, self.config.model_config.max_tokens)):
                    raise Exception("""Token limit exceeded, reduce the number of examples or size of description. Alternatively, you may increase the max_tokens in ModelConfig
                    It is highly recommended to lowering the number of examples to have more room for interactions""")
                else:
                    temp_examples_text += temp_example_text

            context += temp_examples_text
        return context
    
    def __add_examples_to_embedding_cache(self, examples: List[Interaction], description:str = ""):
        """
        This function adds the examples to the embedding cache
        """

        # Creating embeddings for each example using the OpenAI service
        # A single embedding is a combination of the main description of the task and the natural language input of the example
        for example in examples:
            processed_example = self.preprocess_for_embedding_computation(description, example.input)
            embedding = self.prompt_bank.openaiservice.embedding_from_string(processed_example, example, engine="text-similarity-davinci-001", embedding_cache=self.prompt_bank.openaiservice.embedding_cache)
            if embedding is None:
                raise Exception("Could not get embedding for example, please try again")

    def preprocess_for_embedding_computation(self, description, user_input):
        """
        This function preprocesses the description and user input for embedding computation
        """
        # Normalize the description and user input by removing punctuation, lowercasing, and remove extra spaces
        description = description.lower().translate(str.maketrans('', '', string.punctuation)).strip()
        user_input = user_input.lower().translate(str.maketrans('', '', string.punctuation)).strip()

        if description != "":
            return description + "\t" + user_input
        else:
            return user_input