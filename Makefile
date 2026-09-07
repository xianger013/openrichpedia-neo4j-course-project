.PHONY: test demo validate fetch preprocess verify

test:
	PYTHONPATH=src pytest -q

demo:
	PYTHONPATH=src python scripts/preprocess.py --raw-dir tests/fixtures --output-dir data/demo
	PYTHONPATH=src python scripts/validate_processed.py --processed-dir data/demo

fetch:
	python scripts/fetch_openrichpedia.py

preprocess:
	PYTHONPATH=src python scripts/preprocess.py

validate:
	PYTHONPATH=src python scripts/validate_processed.py

verify:
	PYTHONPATH=src pytest -q
	python -m compileall -q src scripts
	PYTHONPATH=src python scripts/preprocess.py --raw-dir tests/fixtures --output-dir data/demo
	PYTHONPATH=src python scripts/validate_processed.py --processed-dir data/demo
