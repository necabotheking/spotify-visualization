BASEDIR=./spotify_tableau_project

.PHONY: pretty
pretty:
	black ${BASEDIR}/api	${BASEDIR}/tests