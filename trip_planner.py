# ensure environment variables from .env are loaded (e.g. OPENAI_API_KEY)
# python-dotenv is installed in the workspace; this will silently do nothing if
# no .env file is present.
from dotenv import load_dotenv
load_dotenv()

from agents import Agent, ItemHelpers, MessageOutputItem, Runner, trace

# when running in a notebook the helper agents are created in __main__;
# if this module is executed as a standalone script the import will fail,
# so we perform it inside main and provide an explanatory error.

# wrap execution in an async function so the module can be run as a script
async def main(msg: str = "4 day trip to Malaysia with a budget of $400, give me a day by day breakdown?"):
    # the planner agents might live in the notebook globals (__main__);
    # import them here so the module can be run as a script.
    try:
        from __main__ import planner_agent, budget_agent, local_guide_agent, travel_agent
    except ImportError:
        # if the agents haven't been set up (e.g. running as a standalone script),
        # create minimal stub agents so the orchestrator can still execute.
        # These won't provide real travel advice but they let the module run without
        # requiring external dependencies.
        def make_stub(name):
            return Agent(
                name=name,
                model="gpt-4.1-mini",
                instructions=(
                    f"You are a placeholder {name}. ``planner_agent`` was not defined."
                    " You should replace this with a real agent when using trip_planner.py."
                ),
            )

        planner_agent = make_stub("planner agent")
        budget_agent = make_stub("budget agent")
        local_guide_agent = make_stub("local guide agent")
        travel_agent = make_stub("travel agent")

    orchestrator_agent = Agent(
        name="travel planner orchestrator",
        model="gpt-4.1-mini",
        instructions=(
            """You are a helpful orchestrator agent. Your role is to analyze the user's question and determine which specialist
         travel agent (planner, budget, local guide, or travel) is best equipped to provide an answer.
         You must use the appropriate tool to ask the relevant travel agent. If the question does not fit into these categories,
         provide a general helpful response. You should always aim to use one of the travel agent tools if applicable."""
        ),
        tools=[
            planner_agent.as_tool(
                tool_name="ask_planner_agent",
                tool_description=planner_agent.handoff_description,
            ),
            budget_agent.as_tool(
                tool_name="ask_budget_agent",
                tool_description=budget_agent.handoff_description,
            ),
            local_guide_agent.as_tool(
                tool_name="ask_local_guide_agent",
                tool_description=local_guide_agent.handoff_description,
            ),
            travel_agent.as_tool(
                tool_name="ask_travel_agent",
                tool_description=travel_agent.handoff_description,
            ),
        ],
    )
    orchestrator_result = await Runner.run(orchestrator_agent, msg)
    print(f"\n\nFinal response:\n{orchestrator_result.final_output}")
    return orchestrator_result.final_output


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())