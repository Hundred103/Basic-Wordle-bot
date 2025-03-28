import random
from collections import Counter


def load_words(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f]


def matches_pattern(word, pattern):
    if len(word) != len(pattern.replace("*", "").replace("+", "")):
        return False

    green_positions = {}
    yellow_letters = set()
    yellow_positions = {}
    gray_letters = set()
    letter_counts = {}

    word_index = 0
    pattern_index = 0

    while pattern_index < len(pattern):
        if word_index >= len(word):
            return False

        current_letter = pattern[pattern_index]

        if pattern_index + 1 < len(pattern) and pattern[pattern_index + 1] == "*":
            if word[word_index] != current_letter:
                return False
            green_positions[word_index] = current_letter
            pattern_index += 2
        elif pattern_index + 1 < len(pattern) and pattern[pattern_index + 1] == "+":
            if word[word_index] == current_letter:
                return False
            yellow_letters.add(current_letter)
            yellow_positions[word_index] = current_letter
            pattern_index += 2
        else:
            gray_letters.add(current_letter)
            pattern_index += 1

        letter_counts[word[word_index]] = letter_counts.get(word[word_index], 0) + 1
        word_index += 1

    for pos, letter in yellow_positions.items():
        if letter not in word or word[pos] == letter:
            return False

    word_letter_counts = {}
    for letter in word:
        word_letter_counts[letter] = word_letter_counts.get(letter, 0) + 1

    for letter in gray_letters:
        if letter in green_positions.values() or letter in yellow_letters:
            if word_letter_counts.get(letter, 0) > letter_counts.get(letter, 0):
                return False
        else:
            if word_letter_counts.get(letter, 0) > 0:
                return False

    return True


def best_next_word(words, filtered_words, used_letters):
    letter_counts = Counter()

    for word in filtered_words:
        letter_counts.update(set(word) - used_letters)

    return max(filtered_words, key=lambda w: sum(letter_counts[ch] for ch in set(w)), default=None)


def get_starter_word():
    common_starters = ["adieu", "tears", "lades", "crane", "slate", "roast", "trace", "slant", "crate"]
    return random.choice(common_starters)


def wordle_solver(filename, patterns):
    words = load_words(filename)
    used_letters = set()
    filtered_words = words

    for pattern in patterns:
        filtered_words = [word for word in filtered_words if matches_pattern(word, pattern)]
        used_letters.update(set(pattern.replace("*", "").replace("+", "")))

    return best_next_word(words, filtered_words, used_letters)


def main():
    filename = "list.txt"
    patterns = []

    print("Wordle Solver Bot")

    print(f"Starter word: {get_starter_word()}")

    while True:
        pattern = input("Enter pattern (or: 'exit' to quit, 'back' to go back to previous game state): ").strip()
        if pattern.lower() == "exit":
            break
        if pattern.lower() == "back":
            patterns.pop()
            continue
        patterns.append(pattern)
        best_word = wordle_solver(filename, patterns)
        if best_word:
            print(f"Best next word: {best_word}")
        else:
            print("No valid words found.")


if __name__ == "__main__":
    main()