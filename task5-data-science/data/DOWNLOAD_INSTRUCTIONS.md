# Download Consumer Complaint Database

## Automatic Download (Recommended)

The notebook will automatically download the dataset when you run cell #7 (after imports and NLTK downloads).

**What happens:**
1. Downloads from: https://files.consumerfinance.gov/ccdb/complaints.csv.zip
2. File size: ~500MB (ZIP), ~2GB (unzipped CSV)
3. Downloads to: `C:\placement\task5-data-science\data\`
4. Automatically extracts and removes ZIP to save space
5. Shows download progress

## Manual Download (If Automatic Fails)

### Option 1: Direct Download
```
1. Visit: https://files.consumerfinance.gov/ccdb/complaints.csv.zip
2. Download the ZIP file (~500MB)
3. Extract complaints.csv to: C:\placement\task5-data-science\data\
4. File should be at: C:\placement\task5-data-science\data\complaints.csv
```

### Option 2: Data.gov Portal
```
1. Visit: https://catalog.data.gov/dataset/consumer-complaint-database
2. Click "Download" → "CSV"
3. Save and extract to: C:\placement\task5-data-science\data\
```

### Option 3: Consumer Finance Bureau
```
1. Visit: https://www.consumerfinance.gov/data-research/consumer-complaints/
2. Click "Download the data"
3. Select CSV format
4. Extract to data folder
```

## Dataset Details

**Source**: Consumer Financial Protection Bureau (CFPB)

**Size**: 
- ZIP: ~500MB
- CSV: ~2GB
- Rows: 5+ million complaints
- Updated: Daily

**Key Columns**:
- `Consumer complaint narrative` - The complaint text
- `Product` - Category of the complaint
- `Date received` - When complaint was filed
- `Company` - Company complained about
- `State` - Consumer's state
- `Issue` - Type of issue
- `Sub-product` - More specific category

## Using in Notebook

The notebook automatically:
1. ✅ Checks if file exists
2. ✅ Downloads if missing
3. ✅ Loads data in chunks (memory efficient)
4. ✅ Filters for 4 main categories:
   - Credit reporting
   - Debt collection
   - Consumer Loan
   - Mortgage
5. ✅ Samples balanced dataset (10,000 per category)
6. ✅ Removes null/empty complaints

## Troubleshooting

### Download Fails
```python
# If automatic download fails, download manually and place at:
# C:\placement\task5-data-science\data\complaints.csv

# Then skip cell #7 and run cell #8 to load the data
```

### Out of Memory
```python
# Reduce sample size in cell #9:
n_samples_per_class = 5000  # Instead of 10000
```

### File Not Found
```python
# Check file path:
import os
csv_path = r'C:\placement\task5-data-science\data\complaints.csv'
print(f"File exists: {os.path.exists(csv_path)}")
```

## Dataset Preview

Once loaded, you'll see:
- ~40,000 complaints (10,000 per category)
- Real consumer complaints from CFPB database
- Clean, balanced dataset ready for ML training
- Realistic text classification problem

## Data Considerations

**Privacy**: 
- Complaints are public records
- Personal information is redacted
- Company names are included

**Quality**:
- Not all complaints have narrative text
- Text length varies (50 - 5000+ characters)
- Some complaints may be duplicates
- Language may contain typos/errors

**Bias**:
- Data represents complaints submitted to CFPB
- May not represent all consumer experiences
- Some products/companies more common than others
- Geographic and temporal biases exist

## Next Steps

After downloading:
1. Run the notebook cells in order
2. First run loads ~500k complaints
3. Filters to 4 categories
4. Samples balanced dataset
5. Ready for EDA and model training!

---

**Questions?** Check the notebook or NOTEBOOK_GUIDE.md for detailed instructions.
