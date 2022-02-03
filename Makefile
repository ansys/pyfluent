flake8:
	@echo "Running flake8"
	@flake8 .

install:
	@pip install -r requirements_build.txt
	@python setup.py sdist
	@python setup.py bdist_wheel
	@pip install dist/*.whl

test-import:
	@python -c "import ansys.fluent.solver as pyfluent"

unittest:
	@echo "Running unittest"
	@pip install -r requirements_test.txt
	@pytest -v
