## book.mk - Book-building targets (zensical-based)

ROOT := $(shell git rev-parse --show-toplevel)

.PHONY: book serve test benchmark stress hypothesis-test _book-reports _book-notebooks

# No-op stubs — overridden by test.mk / bench.mk when present
test:: ; @:
benchmark:: ; @:
stress:: ; @:
hypothesis-test:: ; @:

# Output directory for the compiled book (override on the CLI: make book BOOK_OUTPUT=site)
BOOK_OUTPUT ?= _book

# Detect mkdocs config: prefer root-level mkdocs.yml, fall back to docs/mkdocs-base.yml
_MKDOCS_CFG := $(if $(wildcard $(ROOT)/mkdocs.yml),$(ROOT)/mkdocs.yml,$(if $(wildcard $(ROOT)/docs/mkdocs-base.yml),$(ROOT)/docs/mkdocs-base.yml,))

##@ Book

# Collect test/benchmark/stress/hypothesis HTML artifacts into docs/reports/.
# Each sub-directory is only copied when it exists and is non-empty; missing
# directories produce a WARN instead of a hard failure so a partial run still
# builds a book.
_book-reports: test benchmark stress hypothesis-test
	@mkdir -p $(ROOT)/docs/reports
	@for src_dir in \
	  "_tests/html-coverage:reports/coverage" \
	  "_tests/html-report:reports/test-report" \
	  "_tests/benchmarks:reports/benchmarks" \
	  "_tests/stress:reports/stress" \
	  "_tests/hypothesis:reports/hypothesis"; do \
	  src=$(ROOT)/$${src_dir%%:*}; dest=$(ROOT)/docs/$${src_dir#*:}; \
	  if [ -d "$$src" ] && [ -n "$$(ls -A "$$src" 2>/dev/null)" ]; then \
	    printf "${BLUE}[INFO] Copying $$src -> $$dest${RESET}\n"; \
	    mkdir -p "$$dest"; cp -r "$$src/." "$$dest/"; \
	  else \
	    printf "${YELLOW}[WARN] $$src not found, skipping${RESET}\n"; \
	  fi; \
	done
	@printf "# Reports\n\n" > $(ROOT)/docs/reports.md
	@[ -f "$(ROOT)/docs/reports/test-report/report.html" ] && echo "- [Test Report](reports/test-report/report.html)"       >> $(ROOT)/docs/reports.md || true
	@[ -f "$(ROOT)/docs/reports/hypothesis/report.html" ]  && echo "- [Hypothesis Report](reports/hypothesis/report.html)" >> $(ROOT)/docs/reports.md || true
	@[ -f "$(ROOT)/docs/reports/benchmarks/report.html" ]  && echo "- [Benchmarks](reports/benchmarks/report.html)"        >> $(ROOT)/docs/reports.md || true
	@[ -f "$(ROOT)/docs/reports/stress/report.html" ]      && echo "- [Stress Report](reports/stress/report.html)"         >> $(ROOT)/docs/reports.md || true
	@[ -f "$(ROOT)/docs/reports/coverage/index.html" ]     && echo "- [Coverage Report](reports/coverage/index.html)"      >> $(ROOT)/docs/reports.md || true

# Export each Marimo notebook to a self-contained HTML file under
# $(BOOK_OUTPUT)/notebooks/ and generate a notebooks.md index.
# Skipped silently when MARIMO_FOLDER is not set or does not exist.
_book-notebooks:
	rm -rf ${ROOT}/docs/notebooks
	mkdir -p ${ROOT}/docs/notebooks

	@if [ -d "$(MARIMO_FOLDER)" ]; then \
	  printf "${BLUE}[INFO] Exporting Marimo notebooks from $(MARIMO_FOLDER)${RESET}\n"; \
	  for nb in $(MARIMO_FOLDER)/*.py; do \
	    name=$$(basename "$$nb" .py); \
	    printf "${BLUE}[INFO] Exporting $$nb -> ${ROOT}/docs/notebooks/$$name.html${RESET}\n"; \
	    abs_output="${ROOT}/docs/notebooks/$$name.html"; \
	    (cd "$$(dirname "$$nb")" && ${UV_BIN} run marimo export html --sandbox "$$(basename "$$nb")" -o "$$abs_output"); \
	  done; \
	  printf "${BLUE}[INFO] Writing notebook index${RESET}\n"; \
	  printf "# Marimo Notebooks\n\n" > ${ROOT}/docs/notebooks.md; \
	  for html in ${ROOT}/docs/notebooks/*.html; do \
	    name=$$(basename "$$html" .html); \
	    echo "- [$$name](notebooks/$$name.html)" >> ${ROOT}/docs/notebooks.md; \
	  done; \
	else \
	  printf "${YELLOW}[WARN] MARIMO_FOLDER not set or missing, skipping notebook export${RESET}\n"; \
	fi

# Serve the built book locally on port 8000.
# Uses Python's built-in HTTP server so the JetBrains built-in server (which
# refuses to serve gitignored directories like _book) is not needed.
serve: book ## build and serve the book at http://localhost:8000
	@printf "${BLUE}[INFO] Serving book at http://localhost:8000 (Ctrl-C to stop)${RESET}\n"
	@cd $(BOOK_OUTPUT) && python3 -m http.server 8000

# Full book build: run tests, export notebooks, then compile via zensical.
# The output directory is wiped before each build to avoid stale assets.
book:: _book-reports _book-notebooks ## compile the companion book via zensical
	@printf "${BLUE}[INFO] Building book with config: $(_MKDOCS_CFG)${RESET}\n"
	@${UVX_BIN} zensical build -f "$(_MKDOCS_CFG)"
	@touch "$(BOOK_OUTPUT)/.nojekyll"
	@printf "${GREEN}[SUCCESS] Book built at $(BOOK_OUTPUT)/${RESET}\n"
	@tree $(BOOK_OUTPUT)
