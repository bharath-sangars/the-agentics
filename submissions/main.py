"""
CrewAI starter: a three-agent crew (researcher -> writer -> editor).

Run: uv run python main.py "your topic here"
"""

import os
import sys
from pathlib import Path

from crewai import LLM, Agent, Crew, Process, Task
from dotenv import load_dotenv

load_dotenv()

# --- 1. The model --------------------------------------------------------
# CrewAI uses the OpenAI-compatible client to connect to Groq.
MODEL = os.getenv("GROQ_MODEL", "gpt-oss-120b")

llm = LLM(
    model=f"openai/{MODEL}",
    base_url=os.getenv(
        "GROQ_BASE_URL",
        "https://api.groq.com/openai/v1"
    ),
    api_key=os.environ["GROQ_API_KEY"],
    temperature=0.3,
)

# --- 2. The agents: WHO is on the team -----------------------------------

researcher = Agent(
    role="Research Analyst",
    goal="Collect the key facts and tensions about {topic}",
    backstory=(
        "You are a careful analyst who separates evidence from hype "
        "and says plainly when you are unsure."
    ),
    llm=llm,
    allow_delegation=False,
)

# CHANGE: The Writer now explains topics to a 10-year-old audience.
writer = Agent(
    role="Technical Writer",
    goal="Explain {topic} to a 10-year-old using simple language",
    backstory=(
        "You are a friendly teacher who explains difficult ideas to "
        "10-year-old children. You use simple words, short sentences, "
        "fun and familiar examples, and comparisons to everyday life. "
        "You avoid complicated technical terms and explain any necessary "
        "new words clearly. Your goal is to make every reader feel that "
        "they can understand the topic."
    ),
    llm=llm,
    allow_delegation=False,
)

editor = Agent(
    role="Editor",
    goal="Tighten the draft and flag any claim that needs a source",
    backstory=(
        "You cut filler, fix unclear sentences, and never let an "
        "unsupported claim through unmarked."
    ),
    llm=llm,
    allow_delegation=False,
)

# --- 3. The tasks: WHAT each person owns ---------------------------------

research_task = Task(
    description="Research {topic}. List 5 key facts and 2 open questions.",
    expected_output="A bulleted research brief: 5 facts, 2 open questions.",
    agent=researcher,
)

writing_task = Task(
    description=(
        "Using the research brief, write a 250-word explainer on {topic}. "
        "Explain it to a 10-year-old using simple language and relatable "
        "everyday examples."
    ),
    expected_output="A 250-word explainer suitable for a 10-year-old.",
    agent=writer,
)

editing_task = Task(
    description=(
        "Edit the explainer. Keep the language simple and child-friendly. "
        "Tighten the writing and mark any claim needing a source."
    ),
    expected_output="The final edited explainer, with [source needed] flags.",
    agent=editor,
)

# --- 4. The crew: HOW they work together ---------------------------------

crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, writing_task, editing_task],
    process=Process.sequential,
    verbose=True,
)

if __name__ == "__main__":
    topic = (
        " ".join(sys.argv[1:])
        or "how small teams can use AI agents in data science"
    )

    result = crew.kickoff(inputs={"topic": topic})

    out = Path("output")
    out.mkdir(exist_ok=True)

    (out / "explainer.md").write_text(result.raw, encoding="utf-8")

    print("\n=== FINAL OUTPUT (also saved to output/explainer.md) ===\n")
    print(result.raw)