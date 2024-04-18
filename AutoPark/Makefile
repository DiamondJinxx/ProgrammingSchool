deps:
	pip-compile requirements.in  dev-requirements.in --resolver=backtracking -o requirements.txt
	pip-sync

tests:
	cd src && pytest
