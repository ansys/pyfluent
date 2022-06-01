style:
	@echo "Running code style"
	@pre-commit run --all-files --show-diff-on-failure

install:
	@pip install -r requirements_build.txt
	@python setup.py sdist
	@python setup.py bdist_wheel
	@pip install dist/*.whl

version-info:
	@bash -c "date -u +'Build date: %B %d, %Y %H:%M UTC ShaID: <id>' | xargs -I date sed -i 's/_VERSION_INFO = .*/_VERSION_INFO = \"date\"/g' src/ansys/fluent/core/__init__.py"
	@bash -c "git --no-pager log -n 1 --format='%h' | xargs -I hash sed -i 's/<id>/hash/g' src/ansys/fluent/core/__init__.py"

install-post:
	@pip install -r requirements_build.txt
	@python setup.py sdist
	@python setup.py bdist_wheel
	@find dist -name "*.whl" -exec pip install {}[post] \;

install-pyvistaqt-requirements:
	@sudo apt update
	@sudo apt install libegl1 -y

docker-pull:
	@pip install docker
	@python .ci/pull_fluent_image.py

test-import:
	@python -c "import ansys.fluent.core as pyfluent"

unittest:
	@echo "Running unittest"
	@pip install -r requirements_test.txt
	@pytest -v --cov=ansys.fluent --cov-report html:cov_html --cov-config=.coveragerc

api-codegen:
	@echo "Running API codegen"
	@python -m venv env
	@. env/bin/activate
	@pip install -e .
	@python codegen/allapigen.py
	@rm -rf env

build-doc:
	@sudo rm -rf /home/ansys/.local/share/ansys_fluent_core/examples/*
	@pip install -r requirements_docs.txt
	@xvfb-run make -C doc html
	@touch doc/_build/html/.nojekyll
	@echo "$(DOCS_CNAME)" >> doc/_build/html/CNAME
