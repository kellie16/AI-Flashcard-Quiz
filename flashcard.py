import random
from google import genai


API_KEY = "YOUR_API_KEY" #input your API key

client = genai.Client(api_key=API_KEY) if API_KEY else None


class FlashCard:
    def __init__(self):
        self.quiz = []
        if client:
            print("API key detected.\n")
        else:
            print("No API key detected.\n")

    
    #function to input user questions
    def inputQues(self):
        print("Enter 5 questions with their answers: \n")
        for i in range(5):
            q=input(f"Enter question {i+1}: ")
            ans=input("Enter the answer: ")
            self.quiz.append((q, ans.strip().lower()))
            print()

    #in case AI generated questions do not work or API Key not detected
    def generalQues(self):
        self.quiz=[
            ("Capital of France?", "paris"),
            ("Who wrote 'Hamlet'?", "shakespeare"),
            ("Largest planet in our solar system?", "jupiter"),
            ("What is the boiling point of water in Celsius?", "100"),
            ("Fastest land animal?", "cheetah")
        ]

    #generate AI questions here
    def AIQues(self):

        if not client:
            print("No API key found.\n")
            self.generalQues()
            return

        try:
            
            response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Generate exactly 5 easy general knowledge questions with their answers. Use topics like science, geography, and Indian history. Format the output exactly like this: Question:Answer. Do not add any extra lines, text, numbering, or explanations—only the questions and answers in that format."
            ) #in few cases the AI does not generate in the given format in such case refresh and try again

            text = response.text.strip()
            lines = text.split("\n")

            self.quiz = []
        #splits question and answer
            for line in lines:
                if ":" in line:
                    q, a = line.split(":", 1)
                    self.quiz.append((q.strip(), a.strip().lower()))

            if not self.quiz:
                print("No questions generated. Using offline questions.\n")
                self.generalQues()

        except Exception as e:
            print("❌ Error while calling API:", e)
            self.generalQues()

    def takeQuiz(self):
        print("\n--- Quiz Time ---\n")
        score=0

        random.shuffle(self.quiz)

        for i, (q,ans) in enumerate(self.quiz, start=1):
            user_ans=input(f"Q{i}. {q}\nYour answer: ").strip().lower()
            if user_ans==ans:
                print("Correct!")
                score+=1
            else:
                print(f"Wrong! Correct answer: {ans}\n")

        print(f"Your final score: {score}/{len(self.quiz)}")

if __name__ == "__main__":
    Quiz = FlashCard()

    print("Choose an option:")
    print("1. Take a general knowledge quiz")
    print("2. Enter your own questions")

    choice = input("Enter option: ")
    if choice == "1":
        Quiz.AIQues()
    elif choice == "2":
        Quiz.inputQues()
    else:
        print("Invalid choice!")
        exit()

    Quiz.takeQuiz()
