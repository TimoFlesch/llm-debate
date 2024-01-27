# Debating LLMs
This Python library is for studying debates between LLMs. I am interested in the effect of initial prompts on the persuasiveness of LLMs. Specifically, in an example project utilising this library, I study how two LLMs debate the [chicken or egg problem](https://en.wikipedia.org/wiki/Chicken_or_the_egg). In a follow-up experiment, I investigate how adding a third LLM as mediator could help to find a consensus.


### LLMs
The repository relies on [GPT4ALL](https://github.com/nomic-ai/gpt4all), a toolbox that allows you to run highly quantized LLMs locally on your CPU. I decided against implementing an openAI(or the like) API connection, as I wanted to be able to run everything locally and test the boundaries of publicly available models. 
By default, the toolbox uses `Mistral-7B-OpenOrca`, which can be downloaded from the following link: https://gpt4all.io/models/gguf/mistral-7b-openorca.Q4_0.gguf 

### How it works
All experimental parameters are specified in a `config.toml`. There, you can set the total number of rounds, the number of participating LLMs and their initial prompts as well as other hyperparameters. When a new debate is launched, all LLMs are provided with the system prompts defined in the config and then take turns in the debate. On every turn, an LLM receives the initial prompts together with the entire chat history as input. If all LLMs had their turn, a new round begins. The debate ends after a pre-specified number of rounds.


### Installation Instructions

2. Download Mistral-7B-OpenOrca from the following link https://gpt4all.io/models/gguf/mistral-7b-openorca.Q4_0.gguf and put it in the `./models/` subfolder
3. Make a copy of `configs/default_config.toml` and update the model_path so that it points to the folder containing Mistral-7B (e.g. `/home/USER/code/debating-llms/models`)
4. From within the project folder,  run `pip install -e .` to install the package
5. in your CLI, run `llm_debate --help` to make sure that everything works. You should see the following output:

```
Usage: llm_debate [OPTIONS]

  A debate between LLMs

Options:
  --config_path TEXT  path to config file, e.g. /home/USER/code/debating-
                      llms/configs/default_config.toml. Uses default config if
                      left empty
  --help              Show this message and exit.
  ```

### How to Use
Example usage is detailed in `notebooks/example.ipynb`. Alternatively, you can use the command-line interface as follows:

```
$ llm_debate --config_path ${PATH_TO_CONFIG_DIR}/default_config.toml

```

### Showcase
Results:



### TODO: Optional tool-use
In a future release, the LLMs can be given access to [DuckDuckGo Search](https://duckduckgo.com/) to search for information that might support their argument. This can be specified in the `config.toml`.