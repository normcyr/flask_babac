from flask import abort, jsonify, render_template, request, flash, url_for

from flask_babac import app, settings
from recherche_babac2 import recherche_babac2 as rb2

from wtforms import Form
from wtforms import StringField
from wtforms import validators

import re


class SearchBabacForm(Form):
    q = StringField(
        "Type the name of a part, or a product number, in order to obtain its price and availability: ",
        validators=[
            validators.DataRequired(message="Please enter something."),
            validators.Regexp(
                r"^[\.\w0-9 -]+$",
                message="Invalid characters.",
            ),
        ],
        render_kw={"placeholder": "e.g. training wheels or 22-168"},
    )


@app.route("/api/v1/search", methods=["GET"])
def api_v1_search_query():

    form = SearchBabacForm(request.form)

    if "q" in request.args:
        search_text = request.args["q"]
    else:
        return "Error: No search term field provided. Please specify a search term."

    if "show_cost_price" in request.args:
        show_cost_price = True
    else:
        show_cost_price = False

    username_babac, password_babac = settings.read_config()

    if username_babac is not None and password_babac is not None:
        search = rb2.BabacSearch(username_babac, password_babac)
        (
            list_products,
            loggedin,
            multiple_pages,
            item_page_url,
        ) = search.do_the_search(search_text)

        if loggedin:

            if list_products is not None:
                if show_cost_price == False:
                    for product in list_products:
                        product["price"] = str(
                            "{:.2f}".format(float(product["price"]) * 2, 2)
                        )
                return jsonify(list_products)
            else:
                return "No product found."

        else:
            return "Incorrect username and/or password."

    else:
        return "Please specify the username and password in the configuration file."


@app.route("/search", methods=["GET"])
def search_query():

    form = SearchBabacForm(request.form)

    if "q" in request.args:
        search_text = request.args["q"]
    else:
        return "Error: No search term field provided. Please specify a search term."

    if "show_cost_price" in request.args:
        show_cost_price = True
    else:
        show_cost_price = False

    username_babac, password_babac = settings.read_config()

    if username_babac is not None and password_babac is not None:
        search = rb2.BabacSearch(username_babac, password_babac)
        list_products, loggedin, multiple_pages, item_page_url = search.do_the_search(
            search_text
        )

        if loggedin:

            if list_products is not None:
                display_logo = False
                return render_template(
                    "index.html",
                    form=form,
                    list_products=list_products,
                    q=search_text,
                    item_page_url=item_page_url,
                    multiple_pages=multiple_pages,
                    display_logo=display_logo,
                    show_cost_price=show_cost_price,
                )
            else:
                flash("No product found.")
                display_logo = True
                return render_template(
                    "index.html",
                    form=form,
                    q=search_text,
                    display_logo=display_logo,
                )
        else:
            flash("Incorrect username and/or password.")
            display_logo = True
            return render_template(
                "index.html",
                form=form,
                q=search_text,
                display_logo=display_logo,
            )
    else:
        display_logo = True
        flash("Please specify the username and password in the configuration file.")
        return render_template(
            "index.html",
            form=form,
            display_logo=display_logo,
        )


@app.route("/", methods=["GET"])
@app.route("/index", methods=["GET"])
def search_babac():
    form = SearchBabacForm(request.form)

    display_logo = True
    return render_template(
        "index.html",
        form=form,
        display_logo=display_logo,
    )


@app.route("/json/<sku>")
def search_one_sku_json(sku):
    # Only accept skus in the XX-XXX form.
    m = re.match(r"^\d\d-\d\d\d$", sku)
    if m is None:
        "Invalid SKU format", 404

    username_babac, password_babac = settings.read_config()
    if username_babac is None or password_babac is None:
        return (
            "Please specify the username and password in the configuration file.",
            500,
        )

    search = rb2.BabacSearch(username_babac, password_babac)
    list_products, loggedin, _, _ = search.do_the_search(sku)

    if not loggedin:
        return "Incorrect username and/or password", 500

    if list_products is None:
        return "Product not found", 404

    if len(list_products) != 1:
        return (
            "Unexpected number of products returned ({})".format(len(list_products)),
            500,
        )

    product = list_products[0]

    return jsonify(product)
