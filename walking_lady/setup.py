from setuptools import setup

setup(
    name="walkinglady",
    version="1.0.0",
    packages=["walkinglady"],
    entry_points={
        "console_scripts": [
            "walkinglady = walkinglady.__main__:main"
        ]
    },
    install_requires=["pygame"]
)
