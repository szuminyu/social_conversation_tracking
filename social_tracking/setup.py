import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="social-conversation-pkg-szuminyu",
    version="0.0.1",
    author="Szu Min Yu",
    author_email="smy320@nyu.eud",
    description="A simple package to generate power-point deck for tracking social media conversation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/szuminyu/social_conversation_tracking",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)
