import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='cushead',  
    version='2.2.0',
    scripts=['cushead.py'],
    author="Lucas Vazquez",
    author_email="lucas5zvazquez@gmail.com",
    description="Improves your SEO and the UX generating custom head elements.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lucasvazq/cushead.py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
