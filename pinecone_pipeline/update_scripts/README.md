#### Parsing and updating Certora documentation

1. From `pinecone_pipeline/update_scripts/github_docs/`, clone the latest version of `https://github.com/Certora/Documentation`
2. `cd` into `update_scripts`
3. Run `scraper.py` to convert all the docs to .html files
4. Run `parser.py` to output AI-friendly markdown docs (this can take a while)
5. Run `semantic_chunker.py` to chunk each doc
6. Run `semantic_updater.py` to upload all the chunks into Pinecone.