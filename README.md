# Setup

1. **Create a `/files` folder** at the root of this repository.
2. **Create a `.env` file** and add your `ANTHROPIC_API_KEY` which you can get from [Anthropic's platform](https://console.anthropic.com/).
3. **Set up a Python virtual environment:**
   - Run `python3 -m venv venvbot`.
   - Activate the virtual environment with `source venvbot/bin/activate`.
4. **Install dependencies:**
   - Run `pip install -r requirements.txt`.
5. **Copy directories and files for analysis** into the `/docs` folder.
   - ⚠️ **Important:** Only include relevant and in-scope `.sol`, `.rs`, `.move`, `.ts` or `.go` files. Test files and out of scope contracts should NOT be included.
6. **Start the bot:**
   - Run `make app` to start the analysis.
7. **Enter the project name, language and chosen LLM model for analysis when prompted (we currently recommend CLAUDE):** 
   - Ensure you only type one word each time.
8. **Generated reports will be placed in `./reports` directory:**
   - A summary including the estimated number of weeks and the overall complexity of the project.
   - A complexity report with a file-by-file analysis, providing complexity scores and metrics for each file.
   - A suggested audit plan.
