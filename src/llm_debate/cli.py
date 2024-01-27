import click

from llm_debate.debate import LLMAgent
from llm_debate.utils.files import load_config


@click.command()
@click.option(
    "--config_path",
    default=None,
    help=(
        "path to config file, e.g. "
        "/home/USER/code/llm-debate/configs/default_config.toml. "
        "Uses default config if left empty"
    ),
)
@click.option("--query", prompt="Your Query:", help="A question for the agent")
def cli(config_path, query):
    """An AI agent that uses tools to answer your questions"""
    if config_path is not None:
        cfg = load_config(config_path)
    else:
        cfg = None
    agent = LLMAgent(cfg)
    response = agent.answer(query)
    click.echo(response)


if __name__ == "__main__":
    cli()
