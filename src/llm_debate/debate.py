import datetime
import re
import typing

from llm_debate.llms import GPT4All_LLM


def get_default_cfg() -> dict:
    return {}


# https://github.com/langchain-ai/langchain/blob/master/cookbook/multiagent_authoritarian.ipynb # noqa


class LLMDebate:
    def __init__(
        self,
        cfg: typing.Union[None, dict] = None,
    ):
        cfg = cfg or get_default_cfg()
        # system prompt, num rounds etc
        for k, v in cfg["debate_config"].items():
            setattr(self, k, v)

        # init the agents ( in a name to agent instance dict)
        print("initialising the agents")
        self.agents = self._setup_agents(cfg["agent_configs"])
        self.num_agents = len(self.agents)
        self.agent_names = ", ".join(
            [agent.name for agent in self.agents.values()]
        )
        print("done!")

    def debate(self):
        # launch debate
        # every agent receives the system prompt + their prompt template,
        # followed by the chat history
        prompt_history = []
        n_iter = 0
        while n_iter < self.max_iter:
            for agent in self.agents.values():
                system_prompt = self.system_prompt.format(
                    today=datetime.date.today(),
                    agent_specific_prompt=agent.prompt_template,
                    prompt_history="{prompt_history}",
                )

                this_prompt = system_prompt.format(
                    prompt_history="\n".join(prompt_history)
                )
                if self.verbose:
                    print(this_prompt)
                response = agent.query(this_prompt)
                # the agents sometimes hallucinate the responses from
                # other agents. let's cut them out
                hallucinated_chat = re.findall("\w+:", response)
                if len(hallucinated_chat) > 1:
                    response = response.split(hallucinated_chat[1])[0]
                response = f"[{agent.name}]:{response}"
                print(response)
                prompt_history.append(response)
            n_iter += 1

    def _setup_agents(self, agent_configs: dict) -> dict:
        return {
            agent_name: DebatingAgent(**agent_cfg)
            for agent_name, agent_cfg in agent_configs.items()
        }


class DebatingAgent:
    def __init__(self, general_config: dict, llm_config: dict):
        # name, sys prompt etc
        self.name = general_config["agent_name"]
        self.stance = general_config["stance"]
        self._prompt_template = general_config["prompt_template"]
        # llm instance
        print(
            f"initialising agent {self.name} with {llm_config['model_name']}"
        )
        self.llm = GPT4All_LLM(**llm_config)

    def query(self, prompt: str) -> str:
        return self.llm.generate(prompt)

    @property
    def prompt_template(self) -> str:
        return self._prompt_template.format(name=self.name, stance=self.stance)


def answer(self, prompt: str) -> str:
    self._start_docker_container()
    prompt_history = []

    system_prompt = self.system_prompt.format(
        today=datetime.date.today(),
        tool_description=self._tool_usage,
        tool_names=self._tool_names,
        question=prompt,
        previous_responses="{previous_responses}",
    )
    if self.verbose:
        print(system_prompt.format(previous_responses=""))
    n_iter = 0
    while n_iter < self.max_iter:
        n_iter += 1
        this_prompt = system_prompt.format(
            previous_responses="\n".join(prompt_history)
        )
        response = self.llm.generate(this_prompt)
        try:
            action, action_value = self._parse_response(response)
        except ValueError:
            self._stop_docker_container()
            return response
        if action == "Final Answer:":
            self._stop_docker_container()
            return response
        assert action in list(
            self.tools.keys()
        ), f"LLM requested tool that is not available: {action}"
        if self.tools[action].confirm_action:
            print(
                f"Agent is attempting to call {action}"
                f" with the following input: {action_value}"
            )
            confirmation = input("Do you want to proceed? (y/[n])")
            if confirmation.lower() in ["y", "yes"]:
                pass
            elif confirmation.lower() in ["n", "no", ""]:
                self._stop_docker_container()
                return "Mission aborted."
            else:
                raise ValueError

        # consult tool:
        result = self.tools[action](action_value)
        response += f"\nObservation: {result}\nThought:"
        print(response)
        prompt_history.append(response)
    # shutdown and remove containers
    self._stop_docker_container()
    return response


def _parse_response(self, response: str) -> typing.Tuple[str, str]:
    if "Final Answer:" in response:
        return "Final Answer:", response.split("Final Answer:")[-1].strip()
    match = re.search(
        r"Action: [\[]?(.*?)[\]]?[\n]*Action Input:[\s]*(.*)",
        response,
        re.DOTALL,
    )
    if not match:
        raise ValueError(f"Can't interpret LLM's response: {response}")
    action = match.group(1).strip()
    action_value = match.group(2)
    return action, action_value.strip(" ").strip('"').replace("`", "")


def _start_docker_container(self):
    for tool in self.tools.values():
        if isinstance(getattr(tool, "backend", None), DockerInterface):
            tool.backend.start()


def _stop_docker_container(self):
    for tool in self.tools.values():
        if isinstance(getattr(tool, "backend", None), DockerInterface):
            tool.backend.stop()
