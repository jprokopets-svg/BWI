# Regenerate every data table in the paper from data/ alone.
# CSVs land in tables/, LaTeX versions in tables/tex/, scripts live in tables/scripts/.
PY ?= python3
TABLES = table03_top25 table04_top_bottom10 table05_fastest_growing table06_rank_association table07_quadrants table08_ability_anchors table09_decomposition table10_ability_rankings table_teachers_variants table_2026_extension

tables:
	@for t in $(TABLES); do (cd tables/scripts && $(PY) $$t.py); done
	@echo "CSV tables written to tables/, LaTeX to tables/tex/"

.PHONY: tables
