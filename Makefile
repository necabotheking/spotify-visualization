BASEDIR=./spotify_tableau_project

.PHONY: pretty
pretty:
	black ${BASEDIR}/api	${BASEDIR}/tests	${BASEDIR}/data_handling

.PHONY: test
test:
	pytest	${BASEDIR}/tests