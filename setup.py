from setuptools import setup, find_packages

setup(
    name='telegram_openai_assistant',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'python-telegram-bot==20.6',
        'openai==1.55.1',
        'python-dotenv==1.0.1',
        'gspread==6.1.4', 
        'requests==2.32.3',
        'oauth2client==4.1.3'
    ],
    entry_points={
        'console_scripts': [
            'chatbot = telegram_openai_assistant.bot:main',
        ],
    },
)
