from pathlib import Path

location = Path(input(">>> "))

location.mkdir(exist_ok=True, parents=True)

