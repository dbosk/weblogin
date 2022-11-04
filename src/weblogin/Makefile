MODULES+=	__init__.py
MODULES+=	kth.py

.PHONY: all
all: ${MODULES}

.INTERMEDIATE: init.py
__init__.py: init.py
	ln $< $@

.PHONY: clean
clean:
	${RM} ${MODULES}

INCLUDE_MAKEFILES=../../makefiles
include ${INCLUDE_MAKEFILES}/noweb.mk
