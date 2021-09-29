@echo off
python -m pip install --upgrade pip
pip install spacy
pip install numpy
pip install pandas
python -m spacy download en_core_web_sm
python -m spacy download en_core_web_lg
pip install beautifulsoup4
pip install requests