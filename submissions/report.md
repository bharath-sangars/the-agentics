# CrewAI Project Update Report

## 1. What Was Changed?

The Writer agent's backstory was changed from writing for a skeptical finance director to explaining topics to a 10-year-old child.

The Writer now uses simple words, short sentences, and familiar examples to make difficult topics easier to understand. The writing task was also updated to guide the agent toward producing child-friendly content.

## 2. How Does It Work?

The project uses three AI agents that work together in sequence:

1. **Researcher:** Collects five important facts and identifies two open questions about the given topic.
2. **Writer:** Uses the research to create an approximately 250-word explanation suitable for a 10-year-old.
3. **Editor:** Improves the explanation, removes unnecessary words, and marks claims that need sources.

CrewAI manages the workflow and passes each task's output to the next agent.

## 3. Verification

To verify the change, I ran the program with a sample topic:

`uv run python main.py "how small teams can use AI agents in data science"`

I checked the final output to see whether the explanation used simple language, short sentences, and everyday examples. I also checked that the final result was printed in the terminal and saved to `output/explainer.md`.

The change is verified when the output follows the new child-friendly writing style and the three agents complete their tasks successfully.

## 4. How Was AI Used?

AI was used through CrewAI agents connected to a language model using the Groq API. The Researcher gathers information, the Writer explains the topic, and the Editor improves the final content.

The main change was made to the Writer's backstory and instructions. This demonstrates how changing an AI agent's role and audience can change the content it produces without redesigning the entire system.

## 5. Conclusion

This update demonstrates that an AI agent's backstory can influence its writing style and the way it explains information. The project still follows the same three-agent workflow, but the final explanation is now intended to be easier for children to understand.