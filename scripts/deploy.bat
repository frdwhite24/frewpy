@echo off
setlocal
:PROMPT
SET /P DOCSCHECK=Have you updated the docs (Y/[N])?
IF /I "%DOCSCHECK%" NEQ "Y" GOTO END
SET /P VERSIONNUMCHECK=Have you updated the version number(Y/[N])?
IF /I "%VERSIONNUMCHECK%" NEQ "Y" GOTO END
SET /P AREYOUSURE=Are you sure you want to deploy to PyPi(Y/[N])?
IF /I "%AREYOUSURE%" NEQ "Y" GOTO END

CALL conda activate C:\Users\fred.white\Documents\windows-work\frewpy\venv
CALL python setup.py bdist_wheel sdist
CALL twine upload dist/*

:END
endlocal