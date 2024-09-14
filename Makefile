.PHONY: app, lookup, scrape, parse, chunk, update

app: 
	python3 app.py

lookup:
	python3 pinecone_pipeline/id_lookup/lookup.py

scrape:
	python3 pinecone_pipeline/update_scripts/scraper.py

parse:
	python3 pinecone_pipeline/update_scripts/parser.py

chunk:
	python3 pinecone_pipeline/update_scripts/semantic_chunker.py

update:
	python3 pinecone_pipeline/update_scripts/semantic_updater.py
	
