import sys
import requests

URL = "http://127.0.0.1:5000/search"

print(r"""
          _       __ _       _ _       _                     _
         | |     / _(_)     (_) |     | |                   | |
       __| | ___| |_ _ _ __  _| |_ ___| |_   _   _ __   ___ | |_
      / _` |/ _ \  _| | '_ \| | __/ _ \ | | | | | '_ \ / _ \| __|
     | (_| |  __/ | | | | | | | ||  __/ | |_| | | | | | (_) | |_
      \__,_|\___|_| |_|_| |_|_|\__\___|_|\__, | |_| |_|\___/ \__|
                                          __/ |
                        _____  ____   ___|___/____ _      ______
                       / ____|/ __ \ / __ \ / ____| |    |  ____|
                      | |  __| |  | | |  | | |  __| |    | |__
                      | | |_ | |  | | |  | | | |_ | |    |  __|
                      | |__| | |__| | |__| | |__| | |____| |____
                       \_____|\____/ \____/ \_____|______|______|


""")

while True:
    try:
        q = input("\nSearch: ")
        k = input("Top-K (default: 10): ")

        if not k.strip():
            k = 10

        if type(k) == "str" and not k.isnumeric():
            print("Invalid Top-K value.")
            continue

        try:
            r = requests.get(url=URL, json={"q": q, "k": int(k)})
            data = r.json()

            print("\n" + "-"*50)

            print(f"Result for query '{q}':")

            if data["corrected_q"]:
                print(f"\nSuggested query: '{data['corrected_q']}'")

            if not len(data["result"]):
                print(f"\nYour search - '{q}' - did not match any documents.")
                continue

            for i, [score, doc] in enumerate(data["result"]):
                print()
                print(f"{i+1}. {doc['title']}")
                print(f"URL: {doc['url']}")
                print(f"Parent URL: {doc['parent']}")
                print(f"Summary: {doc['summary']}")
                print(f"Score: {score}")

            print("-"*50)

        except Exception as e:
            print("\n[error] Cannot fetch data from the backend.")
            print(e)
            print("-"*50)
            continue

    except KeyboardInterrupt:
        print("\n\nExiting dfng. Thank you for searching!")
        sys.exit(0)
