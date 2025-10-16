# [file name]: setup.py
from setuptools import setup, find_packages

setup(
    name="whatsapp-business-api",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask>=2.0.0",
        "Flask-SQLAlchemy>=3.0.0",
        "Flask-JWT-Extended>=4.0.0",
        "Flask-CORS>=3.0.0",
        "Flask-Migrate>=3.0.0",
        "requests>=2.25.0",
        "phonenumbers>=8.12.0",
        "python-dotenv>=0.19.0",
        "PyJWT>=2.0.0"
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="WhatsApp Business API integration module with React.js support",
    keywords="whatsapp business api flask reactjs",
    python_requires=">=3.8",
)