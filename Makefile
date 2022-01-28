flake8:
	@echo "Running flake8"
	@flake8 .

install-pyvista-for-python3.10-linux:
	@pip install https://github.com/pyvista/pyvista-wheels/raw/main/vtk-9.1.0.dev0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl

install-pyvista-for-python3.10-windows:
	@pip install https://github.com/pyvista/pyvista-wheels/raw/main/vtk-9.1.0.dev0-cp310-cp310-win_amd64.whl

install:
	@pip install grpc/ansys-api-fluent-v0-0.0.1.tar.gz
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
