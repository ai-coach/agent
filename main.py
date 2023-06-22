from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from ensure_path import ensure_path_exists


class CoachBot:
    def __init__(self, temperature=0.5, model="gpt-3.5-turbo"):
        self.gpt3 = ChatOpenAI(temperature=temperature, model=model)
        self.notes_filename = "notebook/notes.txt"
        self.questions_filename = "notebook/questions.txt"
        ensure_path_exists(self.notes_filename)
        ensure_path_exists(self.questions_filename)

    def read_file(self, filename):
        with open(filename, "r") as f:
            return f.read()

    def append_to_file(self, filename, content):
        with open(filename, "a") as f:
            f.write("\n" + content)

    def overwrite_file(self, filename, content):
        with open(filename, "w") as f:
            f.write(content)

    def ask_question(self, notes, questions):
        if len(notes) == 0:
            question = self.gpt3([SystemMessage(
                content="You are a coach trying to understand your coachee main problem"), HumanMessage(content="Ask the first question:")]).content
        else:
            question = self.gpt3([SystemMessage(
                content=f"You are a coach of coaches. You teach coaches to intercalate broad and specific questions, while giving solutions or ideas. You have your student's (coach) session notes about his coachee:\n {notes}\n\n"), HumanMessage(content=f"The questions the coach had posted are:\n{questions}\n\nWrite the next thing that your student coach should ask to his coachee:")]).content

        self.append_to_file(self.questions_filename, question)
        return question

    def get_answer(self, question):
        print("\n")
        print(question)
        print("\n")
        return input("Answer: ")

    def append_notes(self, question, answer):
        notes = self.gpt3([SystemMessage(content="You are a coach writing his session notes. Write a brief annotation to remember the coachee answer"),
                          HumanMessage(content=f"Question: {question}\n\nAnswer: {answer}")]).content

        self.append_to_file(self.notes_filename, notes)

    def summarize_notes(self, notes):
        if len(notes) > 600:
            summary = self.gpt3([SystemMessage(content=f"You are a coach reading your session notes, which are: {notes}"),
                                HumanMessage(content=f"Summarize as much as you can without losing relevant details")]).content
            self.overwrite_file(self.notes_filename, summary)

    def loop(self):
        while True:
            notes = self.read_file(self.notes_filename)
            questions = self.read_file(self.questions_filename)

            question = self.ask_question(notes, questions)
            answer = self.get_answer(question)

            self.append_notes(question, answer)
            self.summarize_notes(notes)


if __name__ == "__main__":
    CoachBot().loop()
