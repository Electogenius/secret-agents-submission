#!/usr/bin/env python
import sys
from text_response_automation.crew import TextResponseAutomationCrew

# This main file is intended to be a way for your to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run(inputs=None):
    """
    Run the crew.
    """
    inputs = {
        'user_text': inputs if inputs else 'message telling a user that no input was given to the API call yet the LLM was asked to respond to it'
    }
    x = TextResponseAutomationCrew().crew().kickoff(inputs=inputs)
    with open('hi.java', 'w') as f:
            f.write(x.raw)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'user_text': 'sample_value'
    }
    try:
        TextResponseAutomationCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        TextResponseAutomationCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'user_text': 'sample_value'
    }
    try:
        TextResponseAutomationCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: main.py <command> [<args>]")
        sys.exit(1)

    command = sys.argv[1]
    if command == "run":
        run()
    elif command == "train":
        train()
    elif command == "replay":
        replay()
    elif command == "test":
        test()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
