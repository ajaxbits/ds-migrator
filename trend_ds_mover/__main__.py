from prompt_toolkit import prompt


def main():
    answer = prompt("Give me some input: ")
    print("You said: %s" % answer)


if __name__ == "__main__":
    main()
