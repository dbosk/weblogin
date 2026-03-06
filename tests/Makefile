define find_tests
find ../src -type f | xargs grep "<<test \[\[" | \
	sed -En "s/^(.*):.*<<test \[\[([^.]*)\.py\]\]>>.*/test_\2.py:\1/p" | sort -u
endef

define def_target
$(shell echo $1 | cut -d: -f1): $(shell echo $1 | cut -d: -f2)
	notangle ${NOTANGLEFLAGS.py} "-R$$(shell echo $$@ | sed 's/test_\(.*\)/test [[\1]]/')" $$^ > $$@
endef

TESTS=	$(shell ${find_tests})

LIVE_MARK_EXPR=	-m "live"
NONLIVE_MARK_EXPR=	-m "not live"

.PHONY: all
all: $(foreach files,${TESTS},$(shell echo ${files} | cut -d: -f1))
	poetry run pytest ${NONLIVE_MARK_EXPR} ${PYTESTFLAGS}

.PHONY: live
live: $(foreach files,${TESTS},$(shell echo ${files} | cut -d: -f1))
	poetry run pytest ${LIVE_MARK_EXPR} ${PYTESTFLAGS}

.PHONY: live-kth
live-kth: $(foreach files,${TESTS},$(shell echo ${files} | cut -d: -f1))
	poetry run pytest -m "kth_live" ${PYTESTFLAGS}

.PHONY: live-ladok
live-ladok: $(foreach files,${TESTS},$(shell echo ${files} | cut -d: -f1))
	poetry run pytest -m "ladok_live" ${PYTESTFLAGS}

$(foreach files,${TESTS},$(eval $(call def_target, ${files})))

.PHONY: clean
clean:
	${RM} $(foreach files,${TESTS},$(shell echo ${files} | cut -d: -f1))
	${RM} -Rf __pycache__

.PHONY: distclean
distclean:



INCLUDE_MAKEFILES=../makefiles
include ${INCLUDE_MAKEFILES}/noweb.mk
