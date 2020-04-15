#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import argparse
from flask_babac import settings, _version
from recherche_babac2 import recherche_babac2 as rb2


sku_pattern = re.compile(
    r"\d{2}[-]?\d{3}$"
)  # accept 12-345 or 12345, but not 123456 or 1234
text_pattern = re.compile(
    r"[\w0-9 \-]+"
)  # accept text, numbers, but no special character except -
price_pattern = re.compile(r"\d*[.]\d{2}")


def do_the_search(username_babac, password_babac, search_text):

    if username_babac is not None or password_babac is not None:
        recherche = rb2.BabacSearch(username_babac, password_babac)
        (
            list_products,
            loggedin,
            multiple_pages,
            item_page_url,
        ) = recherche.do_the_search(search_text)

        if loggedin:
            return list_products, multiple_pages, item_page_url
        else:
            print(
                "The username and/or password is incorrect. Please verify your login information in the configuration file."
            )
            exit(0)

    else:
        print(
            "Please specify a username and a password for the Cycle Babac website in the configuration file."
        )
        exit(0)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "search_text",
        help="indicate which term(s) you are using to search in the Babac catalogue",
        default="",
        nargs="+",
    )
    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s " + _version.__version__
    )
    args = parser.parse_args()

    search_text = " ".join(args.search_text)

    if re.match(sku_pattern, search_text) or re.match(text_pattern, search_text):
        print("Searching for: '{}'".format(search_text))

        username_babac, password_babac = settings.read_config()
        recherche = rb2.BabacSearch(username_babac, password_babac)
        (
            list_products,
            loggedin,
            multiple_pages,
            item_page_url,
        ) = recherche.do_the_search(search_text)
        if loggedin:
            rb2.print_results(list_products, multiple_pages, item_page_url)
        else:
            print("Failed login.")
    else:
        print("Please avoid using special characters.")


if __name__ == "__main__":
    main()
