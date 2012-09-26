from setuptools import setup, find_packages

setup(name="django-showmethemoney",
      version="0.1",
      description="a small wrapper around goddamned paypal. it works for me.",
      author="scb",
      author_email="scastb@gmail.com",
      packages=find_packages(),
      include_package_data=True,
)

