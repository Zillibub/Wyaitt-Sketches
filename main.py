from wyaitt_sketches.promt_strategy.hey_kiddo import HeyKiddoStrategy


def main():
    strategy = HeyKiddoStrategy()
    out = strategy.evaluate()
    print(out)


if __name__ == "__main__":
    main()
