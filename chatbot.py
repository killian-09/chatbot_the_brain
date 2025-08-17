"""Chatbot module for interacting with a simple Q&A brain stored in JSON."""
import json
from difflib import get_close_matches


def load_the_brain(file_path: str) -> dict:
    """Load the brain data from a JSON file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def save_the_brain(file_path: str, data: dict) -> None:
    """Save the brain data to a JSON file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2)


def find_best_match(user_question: str, questions: list[str]) -> str | None:
    """Find the best matching question from the brain."""
    matches = get_close_matches(
        user_question,
        questions,
        n=2,
        cutoff=0.6
    )
    if matches:
        return matches[0]
    return None


def get_answer_for_question(question: str, the_brain: dict) -> str | None:
    """Get the answer for a given question from the brain."""
    for q in the_brain['questions']:
        if q['question'] == question:
            return q['answer']
    return None


def chatbot():
    """Main chatbot loop for user interaction."""
    the_brain: dict = load_the_brain('the_brain.json')

    while True:
        user_input: str = input('You: ')

        if user_input.lower() in [
            'exit',
            'quit'
        ]:
            print("Goodbye!")
            break

        best_match: str | None = find_best_match(
            user_input,
            [
                q['question']
                for q in the_brain['questions']
            ]
        )

        if best_match:
            answer: str = get_answer_for_question(
                best_match,
                the_brain
            )
            print(
                f'The Brain:{answer}'
            )
        else:
            print(
                "The Brain: I don't know the answer to that question.\n"
                "Can you teach me?"
            )
            new_answer: str = input(
                'type "skip" to skip: '
            )

            if new_answer.lower() != 'skip':
                the_brain['questions'].append(
                    {
                        "question": user_input,
                        "answer": new_answer
                    }
                )
                save_the_brain(
                    'the_brain.json',
                    the_brain
                )
                print(
                    "The Brain: Thank you for teaching me something new!"
                )


if __name__ == "__main__":
    chatbot()
