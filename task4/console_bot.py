"""
Консольный REPL-интерфейс для RAG-бота.

Использование:
    export OPENAI_API_KEY=sk-...
    python task4/console_bot.py
"""

from rag_chain import RAGBot


def main():
    bot = RAGBot()
    print("\n" + "=" * 60)
    print("Veylarian Chronicles RAG Bot (console)")
    print("Введите вопрос или 'quit' для выхода.")
    print("=" * 60 + "\n")

    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not question:
            continue
        if question.lower() in ("quit", "exit", "q"):
            print("Bye!")
            break

        result = bot.ask_with_sources(question)
        print(f"\nBot: {result['answer']}")
        print(f"\n  Sources: {', '.join(s['file'] for s in result['sources'])}")
        print()


if __name__ == "__main__":
    main()
