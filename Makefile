.PHONY: evm sol move go app

evm:
	python3 evm_analyzer.py

sol:
	python3 sol_analyzer.py

move:
	python3 move_analyzer.py
	
go:
	python3 go_analyzer.py

app: 
	python3 app.py
