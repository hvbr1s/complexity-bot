.PHONY: evm sol move

evm:
	python3 evm_analyzer.py

sol:
	python3 sol_analyzer.py

move:
	python3 move_analyzer.py
