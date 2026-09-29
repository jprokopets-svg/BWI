# Regenerate every data table in the paper from data/ alone.
PY ?= python3
TABLES = table03_top25 table04_top_bottom10 table05_fastest_growing table06_rank_association table07_quadrants table08_ability_anchors table09_decomposition table10_ability_rankings

tables:
	@for t in $(TABLES); do (cd tables && $(PY) $$t.py); done
	@cp tables/static/*.tex output/
	@echo "Tables written to output/"

clean:
	@rm -rf output

.PHONY: tables clean
