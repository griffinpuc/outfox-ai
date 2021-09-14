@echo off
echo.
set /p url="enter url:"
echo.
set /p outfile="enter a new file name ending in .txt:"
python3 LinkScraper.py %url% 
echo processing...
python linkParser.py %outfile%
echo the file with the tags in it will be in the new file: %outfile%.