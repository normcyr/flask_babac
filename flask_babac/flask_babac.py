#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from recherche_babac2 import recherche_babac2 as rb2
from flask_babac import settings, _version
import argparse


def do_the_search(username_babac, password_babac, search_text):

    if username_babac != None or password_babac != None:
        recherche = rb2.BabacSearch(username_babac, password_babac)
        list_products, loggedin = recherche.do_the_search(search_text)

        if loggedin:
            return list_products
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
    print("Searching for: '{}'".format(search_text))

    username_babac, password_babac = settings.read_config()
    list_products = do_the_search(username_babac, password_babac, search_text)

    rb2.print_results(list_products)


if __name__ == "__main__":
    main()
