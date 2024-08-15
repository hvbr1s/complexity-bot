# Setup

1. Create a `/docs` folder at the root of this repo.
2. Create `.env` file and add `OPENAI_API_KEY` key.
3. Create a Python virtual environment by running `python3 -m venv venvbot`
4. Run `source venvbot/bin/activate` to activate the environment.
5. Run `pip install -r requirements.txt` to install all the dependencies.
6. Place directories and files to analyze in `/docs`. 
7. Run `python3 sol_analyzer.py` or `python3 evm_analyzer` to start the bot.
