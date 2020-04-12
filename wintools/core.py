import logging


def foo() -> None:
    logging.info("foo!")


def hello(text: str) -> None:
    logging.info("hello! {}".format(text))
