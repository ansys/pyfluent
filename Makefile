style:
	@echo "Running code style"
	@pre-commit run --all-files --show-diff-on-failure

install:
	@pip install -r requirements_build.txt
	@python setup.py sdist
	@python setup.py bdist_wheel
	@pip install dist/*.whl

last-commit-info:
	@bash -c "git --no-pager log -n 1 --format='%an <%ae> - %ad - %h' | xargs -I hash sed -i 's/LAST_COMMIT.*/LAST_COMMIT = \"hash\"/g' ansys/fluent/core/__init__.py"

install-post:
	@pip install -r requirements_build.txt
	@python setup.py sdist
	@python setup.py bdist_wheel
	@pip install dist/ansys_fluent_solver-0.2.dev0-py3-none-any.whl[post]

install-pyvistaqt-requirements:
	@sudo apt update
	@sudo apt install libegl1 -y

docker-pull:
	@docker pull ghcr.io/pyansys/pyfluent:latest

test-import:
	@python -c "import ansys.fluent.core as pyfluent"

unittest:
	@echo "Running unittest"
	@pip install -r requirements_test.txt
	@pytest -v --cov=ansys.fluent --cov-report=term
