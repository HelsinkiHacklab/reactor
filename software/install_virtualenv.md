# Create virtualenv with some reactor requirements

	curl -O https://raw.github.com/pypa/virtualenv/1.9.1/virtualenv.py
	python ./virtualenv.py virtualenv
	source virtualenv/bin/activate
	pip install -r pip-requirements.txt
