# Setup

1. Create a `/docs` folder at the root of this repo.
2. Create a `.env` file and add the `OPENAI_API_KEY` key.
3. Create a Python virtual environment by running `python3 -m venv venvbot`.
4. Run `source venvbot/bin/activate` to activate the environment.
5. Run `pip install -r requirements.txt` to install all the dependencies.
6. Copy directories and files to analyze into `/docs`.  
   ⚠️ Make sure to ONLY copy relevant and in-scope `.sol` or `.rs` files into the `/docs` folder. Test files should NOT be included.
7. Run `python3 sol_analyzer.py` OR `python3 evm_analyzer.py` to start the bot.
