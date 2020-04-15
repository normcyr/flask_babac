from flask import render_template, request, flash, url_for

from flask_babac import app, settings
from recherche_babac2 import recherche_babac2 as rb2

from wtforms import Form
from wtforms import StringField
from wtforms import validators


class SearchBabacForm(Form):
    search_text = StringField(
        "Type the name of a part, or a product number, in order to obtain its price and availability: ",
        validators=[
            validators.DataRequired(message="Please enter something."),
            validators.Regexp(r"^[\w0-9 -]+$", message="Invalid characters.",),
        ],
        render_kw={"placeholder": "e.g. training wheels or 22-168"},
    )


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def search_babac():
    form = SearchBabacForm(request.form)

    if request.method == "GET":
        return render_template("index.html", form=form)

    if request.method == "POST":
        search_text = request.form["search_text"]

        if form.validate():
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
                        return render_template(
                            "index.html",
                            form=form,
                            list_products=list_products,
                            search_text=search_text,
                            item_page_url=item_page_url,
                            multiple_pages=multiple_pages,
                        )
                    else:
                        flash("No product found.")
                        return render_template("index.html", form=form)
                else:
                    flash("Incorrect username and/or password.")
                    return render_template("index.html", form=form)

            else:
                flash(
                    "Please specify the username and password in the configuration file."
                )
                return render_template("index.html", form=form)

        else:
            flash(form.errors["search_text"][0])
            return render_template("index.html", form=form)
