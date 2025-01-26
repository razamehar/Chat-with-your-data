import os
os.environ.setdefault("USER_AGENT", "ChatWithYourData/1.0")
from dotenv import load_dotenv
from util import initiate


def main() -> None:
    load_dotenv()
    os.getenv("OPENAI_API_KEY")

    initiate()


if __name__ == "__main__":
    main()
