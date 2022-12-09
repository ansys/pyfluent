style:
	@echo "Running code style"
	@pre-commit run --all-files --show-diff-on-failure

install:
	@pip install -r requirements/requirements_build.txt
	@python -m build
	@pip install -q --force-reinstall dist/*.whl

version-info:
	@bash -c "date -u +'Build date: %B %d, %Y %H:%M UTC ShaID: <id>' | xargs -I date sed -i 's/_VERSION_INFO = .*/_VERSION_INFO = \"date\"/g' src/ansys/fluent/core/__init__.py"
	@bash -c "git --no-pager log -n 1 --format='%h' | xargs -I hash sed -i 's/<id>/hash/g' src/ansys/fluent/core/__init__.py"

docker-pull:
	@bash .ci/pull_fluent_image.sh

test-import:
	@python -c "import ansys.fluent.core as pyfluent"

unittest: unittest-dev-231

unittest-dev-222:
	@echo "Running unittests"
	@pip install -r requirements/requirements_tests.txt
	@python -m pytest -v -m "dev and not fluent_231 and not fluent_232" --cov=ansys.fluent --cov-report html:cov_html --cov-config=.coveragerc

unittest-dev-231:
	@echo "Running unittests"
	@pip install -r requirements/requirements_tests.txt
	@python -m pytest -v -m "dev and not fluent_222" --cov=ansys.fluent --cov-report html:cov_html --cov-config=.coveragerc

unittest-dev-232:
	@echo "Running unittests"
	@pip install -r requirements/requirements_tests.txt
	@python -m pytest -v -m "dev and not fluent_222 and not fluent_231" --cov=ansys.fluent --cov-report html:cov_html --cov-config=.coveragerc

unittest-all-222:
	@sudo rm -rf /home/ansys/.local/share/ansys_fluent_core/examples/*
	@echo "Running all unittests"
	@pip install -r requirements/requirements_tests.txt
	@python -m pytest -v -m "not fluent_231" --cov=ansys.fluent --cov-report html:cov_html --cov-config=.coveragerc --durations=0

unittest-all-231:
	@sudo rm -rf /home/ansys/.local/share/ansys_fluent_core/examples/*
	@echo "Running all unittests"
	@pip install -r requirements/requirements_tests.txt
	@python -m pytest -v -m "not fluent_222" --cov=ansys.fluent --cov-report html:cov_html --cov-config=.coveragerc --durations=0

unittest-all-232:
	@sudo rm -rf /home/ansys/.local/share/ansys_fluent_core/examples/*
	@echo "Running all unittests"
	@pip install -r requirements/requirements_tests.txt
	@python -m pytest -v -m "not fluent_222 and not fluent_231" --cov=ansys.fluent --cov-report html:cov_html --cov-config=.coveragerc --durations=0

api-codegen:
	@echo "Running API codegen"
	@python -m venv env
	@. env/bin/activate
	@pip install -q -e .
	@python codegen/allapigen.py
	@rm -rf env

build-doc:
	@sudo rm -rf /home/ansys/.local/share/ansys_fluent_core/examples/*
	@pip install -r requirements/requirements_doc.txt
	@xvfb-run make -C doc html
	@touch doc/_build/html/.nojekyll
	@echo "$(DOCS_CNAME)" >> doc/_build/html/CNAME

compare-flobject:
	@python .ci/compare_flobject.py
