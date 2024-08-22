# Setup

1. **Create a `/docs` folder** at the root of this repository.
2. **Create a `.env` file** and add your `OPENAI_API_KEY` which you can get from [OpenAI's platform](https://platform.openai.com/).
3. **Set up a Python virtual environment:**
   - Run `python3 -m venv venvbot`.
   - Activate the virtual environment with `source venvbot/bin/activate`.
4. **Install dependencies:**
   - Run `pip install -r requirements.txt`.
5. **Copy directories and files for analysis** into the `/docs` folder.
   - ⚠️ **Important:** Only include relevant and in-scope `.sol` or `.rs` files. Test files and out of scope contracts should NOT be included.
6. **Start the analysis bot:**
   - For a Solana project, run `python3 sol_analyzer.py`.
   - For a Solidity project, run `python3 evm_analyzer.py`.
   - For a Move project, run `python3 move_analyzer.py`.
7. **Enter the project name when prompted:** Ensure you only type one word.
8. **Generated reports will be placed in `./reports` directory:**
   - A summary including the estimated number of weeks and the overall complexity of the project.
   - A complexity report with a file-by-file analysis, providing complexity scores and metrics for each file.
   - A suggested audit plan.
