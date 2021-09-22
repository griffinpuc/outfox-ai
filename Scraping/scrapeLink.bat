
@echo off

set argC=0
for %%x in (%*) do Set /A argC+=1


IF %argC%==0 (
    set /p url="enter url:"
    echo.
    set /p outfile="enter a new file name ending in .txt:"
    python3 LinkScraper.py %url% 
    echo Webpage collected, processing...
    python linkParser.py %outfile%
    echo the file with the tags in it will be in the new file: %outfile%.
)


IF %argC%==2 (
    python3 LinkScraper.py %1
    echo Webpage collected, processing...
    python linkParser.py %2
    echo the file with the tags in it will be in the new file: %2%
)

@REM IF %argC%==1 (
@REM     echo scrapeLink.bat is a batch script designed to scrape a webpage,
@REM     echo and then put the page content through spaCy's nlp algorithm to
@REM     echo output the most relevant terms from the webpage.
@REM     echo ..
@REM     echo ..
@REM     echo usage:
@REM     echo scrapeLink.bat
@REM     echo <or>
@REM     echo scrapeLink.bat <target-url> <output-file-name>
@REM     echo <or>
@REM     echo scrapeLink.bat help
@REM )