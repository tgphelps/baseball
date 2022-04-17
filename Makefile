
check:
	flake8
	mypy *.py

sql:
	psql -Utgphelps -dbaseball
