#/bin/env python3
"""
My solution to the "Python Poetry" puzzle:
    http://puzzles.bostonpython.com/poetry.html

Written 2014-06-24.
"""

import string

poem = '''a narrow fellow in the grass
occasionally rides;
you may have met him, did you not,
his notice sudden is.

the grass divides as with a comb,
a spotted shaft is seen;
and then it closes at your feet
and opens further on.

he likes a boggy acre,
a floor too cool for corn.
yet when a child, and barefoot,
i more than once, at morn,

have passed, i thought, a whip-lash
unbraiding in the sun,
when, stooping to secure it,
it wrinkled, and was gone.

several of nature's people
i know, and they know me;
i feel for them a transport
of cordiality;

but never met this fellow,
attended or alone,
without a tighter breathing,
and zero at the bone.'''


def main():
    say([56,38,44,56,29])

def say(numbers):
    freq_to_letter = get_freq_to_letter(poem)
    for num in numbers:
        print(freq_to_letter[num], end="")
    print()

def get_freq_to_letter(text):
    """Return a mapping of number (frequency in poem) to letter or None."""

    hist = make_histogram(text)

    # decoder: mapping from freq to letter, or to None if there are multiple
    # letters with the same fequency 
    decoder = {}

    for letter, freq in hist.items():
        if freq in decoder:
            decoder[freq] = None
        else:
            decoder[freq] = letter

    return decoder

def make_histogram(text):
    """Return a mapping of letter to frequency in poem."""

    freqs = {}

    for letter in poem:
        if letter in string.ascii_lowercase:
            if letter in freqs:
                freqs[letter] += 1
            else:
                freqs[letter] = 1

    return freqs
            

if __name__ == "__main__":
    main()
