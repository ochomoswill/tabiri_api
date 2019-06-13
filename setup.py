import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tabiri_api",
    version="0.0.1",
    author="ochomoswill",
    author_email="ochomoswill@gmail.com",
    description="A Django Rest API with GIS capabilities.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ochomoswill/tabiri_api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['django', 'django-rest-framework'],
)