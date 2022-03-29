from search_query import SearchQuery

tests = {
    "compil*": ("TERM", "compil*"),
    "compiler": ("TERM", "compiler"),
    "NOT compiler": ("NOT", ("TERM", "compiler")),
    "not compiler": ("NOT", ("TERM", "compiler")),
    "compiler engineer": ("AND", ("TERM", "compiler"), ("TERM", "engineer")),
    "compiler AND engineer": ("AND", ("TERM", "compiler"), ("TERM", "engineer")),
    "compiler and engineer": ("AND", ("TERM", "compiler"), ("TERM", "engineer")),
    "compiler OR engineer": ("OR", ("TERM", "compiler"), ("TERM", "engineer")),
    "compiler or engineer": ("OR", ("TERM", "compiler"), ("TERM", "engineer")),
    "NOT compiler engineer": ("NOT", ("AND", ("TERM", "compiler"), ("TERM", "engineer"))),
    "not compiler engineer": ("NOT", ("AND", ("TERM", "compiler"), ("TERM", "engineer"))),
    "NOT compiler engineer AND engineer": ("AND", ("NOT", ("AND", ("TERM", "compiler"), ("TERM", "engineer"))), ("TERM", "engineer"))
}

if __name__ == "__main__":
    query_parser = SearchQuery()

    print("processor: running parser test")
    for test, result in tests.items():
        try:
            assert(query_parser.parse(test) == result)
            print(f"test: '{test}' - passed")
        except AssertionError:
            print(f"test: '{test}' - failed")
