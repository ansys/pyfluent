@ECHO OFF

setlocal

pushd %~dp0

REM Command file for Sphinx documentation
if "%SPHINXBUILD%" == "" (
    set SPHINXBUILD=sphinx-build
)

set SOURCEDIR=source
set BUILDDIR=_build
set SPHINXOPTS=-j auto -w build_errors.txt -N -q

if "%1" == "" goto help
if "%1" == "clean" goto clean

REM Check if sphinx-build command exists
%SPHINXBUILD% >NUL 2>NUL
if errorlevel 9009 (
    echo.
    echo.The 'sphinx-build' command was not found. Make sure you have Sphinx
    echo.installed, then set the SPHINXBUILD environment variable to point
    echo.to the full path of the 'sphinx-build' executable. Alternatively you
    echo.may add the Sphinx directory to PATH.
    echo.
    echo.If you don't have Sphinx installed, grab it from
    echo.http://sphinx-doc.org/
    exit /b 1
)

REM Check if BUILD_ALL_DOCS is set, and if so, skip Python script execution
if defined BUILD_ALL_DOCS (
	REM Build documentation with Sphinx by generating RST files
    @REM python api_rstgen.py
    @REM python datamodel_rstgen.py
    @REM python tui_rstgen.py
    python settings_rstgen.py
) else (
    echo BUILD_ALL_DOCS is not set. Skipping RST file generation.
)

%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS%
goto end

:clean
echo Cleaning build directories...
rmdir /s /q %BUILDDIR% > NUL 2>&1
rmdir /s /q %SOURCEDIR%\examples > NUL 2>&1
rmdir /s /q %SOURCEDIR%\api\meshing\datamodel > NUL 2>&1
rmdir /s /q %SOURCEDIR%\api\meshing\tui > NUL 2>&1
rmdir /s /q %SOURCEDIR%\api\solver\datamodel > NUL 2>&1
rmdir /s /q %SOURCEDIR%\api\solver\tui > NUL 2>&1

for /d /r %SOURCEDIR% %%d in (_autosummary) do @if exist "%%d" rmdir /s /q "%%d"
del build_errors.txt > NUL 2>&1
goto end

:help
echo.
echo Usage: makefile.bat [clean|other_commands]
echo.
%SPHINXBUILD% -M help %SOURCEDIR% %BUILDDIR% %SPHINXOPTS%
goto end

:end
popd
