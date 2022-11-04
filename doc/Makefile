.PHONY: all
all: weblogin.pdf

LATEXFLAGS+=	-shell-escape
TEX_PYTHONTEX=	yes

weblogin.pdf: ../src/weblogin/init.tex
weblogin.pdf: ../src/weblogin/kth.tex

weblogin.pdf: preamble.tex abstract.tex ../LICENSE

../%::
	${MAKE} -C $(dir $@) $(notdir $@)


.PHONY: clean
clean:
	${RM} weblogin.pdf
	${MAKE} -C ../src/weblogin clean

.PHONY: distclean
distclean:
	${RM} -Rf __pycache__
	${MAKE} -C ../src/weblogin distclean



INCLUDE_MAKEFILES=../makefiles
include ${INCLUDE_MAKEFILES}/tex.mk
