from setuptools import setup


def readme():
    with open("README.md", "r") as f:
        return f.read()


version = {}
with open("flask_babac/_version.py", "r") as fp:
    exec(fp.read(), version)


setup(
    name="Flask Babac",
    version=version["__version__"],
    description="A Python3 Flask front-end application to search the Cycle Babac catalogue and return description, price and availability.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Topic :: Office/Business :: Financial",
    ],
    keywords="bicycle babac parts repair diy",
    url="http://github.com/normcyr/flask_babac",
    author="Normand Cyr",
    author_email="norm@normandcyr.com",
    license="GNU GPLv3",
    packages=["flask_babac"],
    entry_points={"console_scripts": ["flask_babac=flask_babac.flask_babac:main"],},
    install_requires=["flask", "recherche_babac2", "python-dotenv", "flask-wtf",],
    zip_safe=False,
    include_package_data=True,
    python_requires=">=3.5",
)
