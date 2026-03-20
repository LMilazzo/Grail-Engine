import os
from pathlib import Path
from datetime import datetime

DIR = Path("HISTORY/LOGS/")  # adjust if needed

def main():
    empty = []

    for file in DIR.glob("*.json*"):  # matches .json and .jsonl
        if file.is_file() and file.stat().st_size == 0:
            empty.append(file.name)
            os.remove(file)


    with open("HISTORY/log_edits.txt", "a") as f:
        for x in empty:
            f.write(f"{datetime.now().isoformat()} -  DELETE EMPTY LOG  -  {x} \n")

if __name__ == "__main__":
    main()