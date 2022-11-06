MODULES+=	__init__.py
MODULES+=	seamlessaccess.py
MODULES+=	kth.py

.PHONY: all
all: ${MODULES}

.INTERMEDIATE: init.py
__init__.py: init.py
	${MV} $< $@

.PHONY: clean
clean:
	${RM} ${MODULES}
	${RM} *.tex

INCLUDE_MAKEFILES=../../makefiles
include ${INCLUDE_MAKEFILES}/noweb.mk
