# OUTFOX-AI: CM3 

## What are we doing?
**CM3** = (Correlational Matrix Model Manager)  
We are building a recommendation AI that will work with an existing platform, [Outfox](https://github.com/briangormanly/outfox).  
This platform is powered by a correlational matrix built using [Pandas](https://pandas.pydata.org/)  

## Features
- Auto-format CSV file to correct format
- Generate boolean table for category tags
- Generate correlational matrix from boolean table
- Provide recommendations based on an input tag

##Usage
1. Clone this repository
2. Add a CSV data file to <code>ROOT_DIR/csv/raw_data.csv</code>
3. Run csv formatter: <code>python ./main.py fmcsv</code>
4. Build boolean matrix: <code>python ./main.py gbt</code>
5. Build correlational matrix: <code>python ./main.py gcm</code> (This may take some time depending on matrix size and PC specs)
6. Test recommendation output: <code> python ./main.py rec [tag] [output num]</code>

## Sample Recommendation
### Input/Output:
```
> python ./main.py rec fashion 4
> Recommendations: ['CREATIVE', 'DRAWING', 'AESTHETICS', 'ART']
```
