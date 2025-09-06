1# ui_rich.py
import random
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.align import Align
from rich.rule import Rule
from rich import box

# import your quiz logic (flashcard.py should define FlashCard)
from flashcard import FlashCard

console = Console()

def main():
    console.clear()
    console.print(Panel.fit("🧠  [bold cyan]AI Flashcard Quiz[/bold cyan]", border_style="cyan"))
    console.print(Rule())

    # create flashcard instance (it will check for API key etc.)
    quiz = FlashCard()

    console.print()  # small spacing
    choice = Prompt.ask(
        "[bold]Choose an option[/bold]\n1. Take a general knowledge quiz\n2. Enter your own questions\nEnter",
        choices=["1", "2"],
        default="1"
    )

    if choice == "1":
        # show spinner/status while AI generates questions (or fallback runs)
        with console.status("[bold green]Generating AI questions...[/bold green]", spinner="dots"):
            # this calls quiz.AIQues() which may call external API or fallback
            quiz.AIQues()
    else:
        quiz.inputQues()

    # if no questions loaded, make sure fallback is present
    if not quiz.quiz:
        console.print("[yellow]No questions available — loading offline questions.[/yellow]")
        quiz.generalQues()

    random.shuffle(quiz.quiz)

    # run the quiz
    score = 0
    total = len(quiz.quiz)
    console.print(Rule("[green]Begin Quiz[/green]"))

    for i, (q, ans) in enumerate(quiz.quiz, start=1):
        # show question in a panel (wraps automatically)
        console.print(Panel.fit(f"[bold yellow]Q{i}.[/bold yellow] {q}", border_style="yellow"))
        # get user answer (styled prompt)
        try:
            user_ans = Prompt.ask("Your answer").strip().lower()
        except KeyboardInterrupt:
            console.print("\n[red]Quiz aborted by user.[/red]")
            return

        if user_ans == ans:
            console.print("[green]✔ Correct![/green]\n")
            score += 1
        else:
            console.print(f"[red]✘ Wrong![/red] Correct answer: [bold]{ans}[/bold]\n")

    # results table
    table = Table(title="Quiz Results", box=box.ROUNDED, title_style="bold magenta")
    table.add_column("Total Questions", justify="center")
    table.add_column("Correct Answers", justify="center")
    table.add_column("Score", justify="center")
    table.add_row(str(total), str(score), f"{score}/{total}")

    console.print(Rule())
    console.print(table)
    console.print(Panel(Align.center(f"[bold cyan]Final Score: {score}/{total}[/bold cyan]"), border_style="green"))

if __name__ == "__main__":
    main()
