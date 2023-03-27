import logging
import datetime
from wyaitt_sketches.promt_strategy.hey_kiddo import HeyKiddoStrategy


def evaluate_one():
    strategy = HeyKiddoStrategy()
    out = strategy.evaluate(datetime.date.today())
    print(out)


def evaluate_history(depth):
    strategy = HeyKiddoStrategy()
    d = datetime.date.today() - datetime.timedelta(days=depth)
    for i in range(depth):
        try:
            out = strategy.evaluate(d)
            print(f"Evaluation for {d}")
            print(out.original_title)
            print()
            print(out.content_description)
            print(out.illustration_prompt)
            print("_" * 30)
            d += datetime.timedelta(days=1)
        except Exception as e:
            print(e)
            print("_" * 30)


def main():
    evaluate_history(20)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    main()
