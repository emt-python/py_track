
"""Benchmark how quickly Python's regex implementation can compile regexes.

We bring in all the regexes used by the other regex benchmarks, capture them by
stubbing out the re module, then compile those regexes repeatedly. We muck with
the re module's caching to force it to recompile every regex we give it.
"""

# Python imports
import time
import re


def capture_regexes():
    regexes = [
        # Adding more complex and larger regex patterns
        # Email pattern
        (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', 0),
        (r'(https?://[^\s]+)', 0),  # URL pattern
        # Custom complex pattern mimicking serial numbers
        (r'(\d{2,4}-\d{2,4}-\d{2,4}-\d{2,4})', 0),
        ('.*?'.join(map(re.escape, 'abcdefghijklmnopqrstuvwxyz')),
         re.IGNORECASE),  # Pattern matching all letters in sequence
    ]

    real_compile = re.compile
    real_search = re.search
    real_sub = re.sub

    def capture_compile(regex, flags=0):
        regexes.append((regex, flags))
        return real_compile(regex, flags)

    def capture_search(regex, target, flags=0):
        regexes.append((regex, flags))
        return real_search(regex, target, flags)

    def capture_sub(regex, *args):
        regexes.append((regex, 0))
        return real_sub(regex, *args)

    re.compile = capture_compile
    re.search = capture_search
    re.sub = capture_sub
    # capture_search(r'(\w+)', "Some sample text to search through", 0)
    # capture_sub(r'(\s+)', "and replace spaces with hyphens in this text", "-", 0)
    re.compile = real_compile
    re.search = real_search
    re.sub = real_sub

    return regexes


def bench_regex_compile(loops, regexes):
    range_it = range(loops)
    large_text = " ".join(
        ["Sample text with various emails like example@example.com, URLs like https://example.com, and serial numbers like 1234-5678-9101-1121."]*10000)  # Large text

    for _ in range_it:
        for regex, flags in regexes:
            re.purge()
            compiled = re.compile(regex, flags)
            # Performing both search and substitution on a large text
            re.search(compiled, large_text)
            re.sub(compiled, 'REPLACED', large_text)


if __name__ == "__main__":

    regexes = capture_regexes()
    loops = 1
    start_time = time.time()
    print("start compile")
    bench_regex_compile(loops, regexes)
    elapsed_time = time.time() - start_time
    print(f"Compute time: {elapsed_time:.2f} seconds")
