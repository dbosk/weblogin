.PHONY: all
all: weblogin.pdf

LATEXFLAGS+=	-shell-escape
TEX_PYTHONTEX=	yes
PYTHONTEXFLAGS=	--interpreter "python:poetry run python3"

weblogin.pdf: preamble.tex abstract.tex ../LICENSE didactic.sty
weblogin.pdf: intro.tex

FIGS+=		figs/weblogin.pdf

weblogin.pdf: ${FIGS}

weblogin.pdf: ../src/weblogin/init.tex
weblogin.pdf: ../src/weblogin/kth.tex
weblogin.pdf: ../src/weblogin/seamlessaccess.tex
weblogin.pdf: ../src/weblogin/ladok.tex
weblogin.pdf: ../src/weblogin

../src/weblogin::
	${MAKE} -C $@ all

../%::
	${MAKE} -C $(dir $@) $(notdir $@)

${FIGS}::
	${MAKE} -C $(dir $@) $(notdir $@)


.PHONY: clean
clean:
	${RM} weblogin.pdf
	${MAKE} -C ../src/weblogin clean
	${MAKE} -C figs clean

.PHONY: distclean
distclean:
	${RM} -Rf __pycache__
	${MAKE} -C ../src/weblogin distclean
	${MAKE} -C figs distclean



INCLUDE_MAKEFILES=../makefiles
include ${INCLUDE_MAKEFILES}/tex.mk
INCLUDE_DIDACTIC=./didactic
include ${INCLUDE_DIDACTIC}/didactic.mk
