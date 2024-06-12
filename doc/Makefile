# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    = -j auto -w build_errors.txt -N
SPHINXBUILD   = sphinx-build
SOURCEDIR     = source
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# customized clean due to examples gallery
clean:
	rm -rf build_errors.txt
	rm -rf $(BUILDDIR)/*
	rm -rf $(SOURCEDIR)/examples/*
	rm -rf $(SOURCEDIR)/api/meshing/datamodel
	rm -rf $(SOURCEDIR)/api/meshing/tui
	rm -rf $(SOURCEDIR)/api/solver/datamodel
	rm -rf $(SOURCEDIR)/api/solver/tui
	find . -type d -name "_autosummary" "datamodel" -exec rm -rf {} +
