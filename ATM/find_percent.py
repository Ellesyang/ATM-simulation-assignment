import os
import sys

def find_percent_space(directory):
    matches = []

    for root, dirs, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                    for lineno, line in enumerate(f, 1):
                        if '% ' in line:
                            matches.append((filepath, lineno, line.rstrip()))
            except Exception as e:
                print(f"Kon niet lezen: {filepath} ({e})")

    return matches


if __name__ == "__main__":
    directory = sys.argv[1] if len(sys.argv) > 1 else '.'

    if not os.path.isdir(directory):
        print(f"Fout: '{directory}' is geen geldige map.")
        sys.exit(1)

    print(f"Zoeken in: {os.path.abspath(directory)}\n")
    results = find_percent_space(directory)

    if not results:
        print("Geen '% ' gevonden.")
    else:
        print(f"{len(results)} treffer(s) gevonden:\n")
        for filepath, lineno, line in results:
            print(f"{filepath}:{lineno}")
            print(f"  {line}\n")

    input("Druk op Enter om af te sluiten...")
