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

unittest-custom:
	@echo "Running custom unittest"
	@pip install -r requirements/requirements_tests.txt
	@python -m pytest -v -k test_transcript  # Update custom testlist

unittest-dev-222:
	@echo "Running unittests"
	@pip install -r requirements/requirements_tests.txt
	@python -m pytest -v -m "dev and fluent_222" --cov=ansys.fluent --cov-report=xml:cov_xml.xml --cov-report=html

unittest-dev-231:
	@echo "Running unittests"
	@pip install -r requirements/requirements_tests.txt
	@python -m pytest -v -m "dev and fluent_231" --cov=ansys.fluent --cov-report=xml:cov_xml.xml --cov-report=html

unittest-dev-241:
	@echo "Running unittests"
	@pip install -r requirements/requirements_tests.txt
	@python -m pytest -v -m "dev and fluent_241" --cov=ansys.fluent --cov-report=xml:cov_xml.xml --cov-report=html

unittest-dev-232:
	@echo "Running unittests"
	@pip install -r requirements/requirements_tests.txt
	@python -m pytest -v -m "dev and fluent_232" --cov=ansys.fluent --cov-report=xml:cov_xml.xml --cov-report=html

unittest-all-222:
	@sudo rm -rf /home/ansys/.local/share/ansys_fluent_core/examples/*
	@echo "Running all unittests"
	@pip install -r requirements/requirements_tests.txt
	@python -m pytest -v -m "fluent_222" --cov=ansys.fluent --cov-report=xml:cov_xml.xml --cov-report=html --durations=0

unittest-all-222-no-codegen:
	@sudo rm -rf /home/ansys/.local/share/ansys_fluent_core/examples/*
	@echo "Running all unittests"
	@pip install -r requirements/requirements_tests.txt
	@python -m pytest -v -m "fluent_222 and not codegen_required" --cov=ansys.fluent --cov-report=xml:cov_xml.xml --cov-report=html --durations=0

unittest-all-231:
	@sudo rm -rf /home/ansys/.local/share/ansys_fluent_core/examples/*
	@echo "Running all unittests"
	@pip install -r requirements/requirements_tests.txt
	@python -m pytest -v -m "fluent_231" --cov=ansys.fluent --cov-report=xml:cov_xml.xml --cov-report=html --durations=0

unittest-all-231-no-codegen:
	@sudo rm -rf /home/ansys/.local/share/ansys_fluent_core/examples/*
	@echo "Running all unittests"
	@pip install -r requirements/requirements_tests.txt
	@python -m pytest -v -m "fluent_231 and not codegen_required" --cov=ansys.fluent --cov-report=xml:cov_xml.xml --cov-report=html --durations=0

unittest-all-241:
	@sudo rm -rf /home/ansys/.local/share/ansys_fluent_core/examples/*
	@echo "Running all unittests"
	@pip install -r requirements/requirements_tests.txt
	@python -m pytest -v -m "fluent_241" --cov=ansys.fluent --cov-report=xml:cov_xml.xml --cov-report=html --durations=0

unittest-all-241-no-codegen:
	@sudo rm -rf /home/ansys/.local/share/ansys_fluent_core/examples/*
	@echo "Running all unittests"
	@pip install -r requirements/requirements_tests.txt
	@python -m pytest -v -m "fluent_241 and not codegen_required" --cov=ansys.fluent --cov-report=xml:cov_xml.xml --cov-report=html --durations=0

unittest-all-232:
	@sudo rm -rf /home/ansys/.local/share/ansys_fluent_core/examples/*
	@echo "Running all unittests"
	@pip install -r requirements/requirements_tests.txt
	@python -m pytest -v -m "fluent_232" --cov=ansys.fluent --cov-report=xml:cov_xml.xml --cov-report=html --durations=0

unittest-all-232-no-codegen:
	@sudo rm -rf /home/ansys/.local/share/ansys_fluent_core/examples/*
	@echo "Running all unittests"
	@pip install -r requirements/requirements_tests.txt
	@python -m pytest -v -m "fluent_232 and not codegen_required" --cov=ansys.fluent --cov-report=xml:cov_xml.xml --cov-report=html --durations=0

api-codegen:
	@echo "Running API codegen"
	@python -m venv env
	@. env/bin/activate
	@pip install -q -e .
	@python codegen/allapigen.py
	@rm -rf env

build-doc-source:
	@sudo rm -rf doc/source/api/meshing/datamodel
	@sudo rm -rf doc/source/api/meshing/tui
	@sudo rm -rf doc/source/api/solver/datamodel
	@sudo rm -rf doc/source/api/solver/tui
	@sudo rm -rf doc/source/api/solver/_autosummary/settings
	@sudo rm -rf /home/ansys/.local/share/ansys_fluent_core/examples/*
	@pip install -r requirements/requirements_doc.txt
	@xvfb-run make -C doc html

build-all-docs:
	@python doc/settings_rstgen.py
	@sudo rm -rf /home/ansys/.local/share/ansys_fluent_core/examples/*
	@pip install -r requirements/requirements_doc.txt
	@xvfb-run make -W --keep-going -C doc html

compare-flobject:
	@python .ci/compare_flobject.py
