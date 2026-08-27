from setuptools import setup, find_packages

setup(
    name="aegisflow-sdk",
    version="2.4.0",
    packages=find_packages(),
    install_requires=["httpx>=0.25.0", "pydantic>=2.5.0"],
    description="Official Python SDK for AegisFlow Streaming AI Platform",
    author="AegisFlow Engineering",
)
