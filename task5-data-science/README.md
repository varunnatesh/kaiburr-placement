# Task 5: Consumer Complaint Text Classification

This project performs multi-class text classification on **real consumer complaint data** from the Consumer Financial Protection Bureau (CFPB).

## Dataset
**Source**: Consumer Financial Protection Bureau (CFPB)  
**URL**: https://files.consumerfinance.gov/ccdb/complaints.csv.zip  
**Size**: 5+ million real consumer complaints (~2GB unzipped)  
**Categories**: Credit Reporting, Debt Collection, Consumer Loan, Mortgage  
**Auto-Download**: ✅ Notebook automatically downloads the dataset

## Requirements
```
pandas==2.1.4
numpy==1.26.2
scikit-learn==1.3.2
matplotlib==3.8.2
seaborn==0.13.0
nltk==3.8.1
wordcloud==1.9.3
jupyter==1.0.0
```

## Project Structure
```
task5-data-science/
├── data/
│   ├── complaints.csv                    # Auto-downloaded (~2GB)
│   ├── DOWNLOAD_INSTRUCTIONS.md
│   └── (training data generated here)
├── notebooks/
│   └── complaint_classification.ipynb    # Main ML pipeline
├── src/
│   ├── data_preprocessing.py
│   ├── feature_engineering.py
│   ├── model_training.py
│   └── model_evaluation.py
├── models/
│   └── (saved models will be here)
├── requirements.txt
└── README.md
```

## Quick Start

### 1. Install Dependencies
```powershell
cd C:\placement\task5-data-science
pip install -r requirements.txt
```

### 2. Start Jupyter Notebook
```powershell
cd notebooks
jupyter notebook complaint_classification.ipynb
```

### 3. Run All Cells
- Cell 1-2: Imports and NLTK downloads (automatic)
- **Cell 3**: Downloads CFPB dataset automatically (~5-10 min first time)
- Cell 4-5: Loads and prepares 40k balanced complaints
- Cell 6+: EDA, training, evaluation

**That's it!** The notebook handles everything automatically.

### Manual Download (Optional)
If automatic download fails:
1. Visit: https://files.consumerfinance.gov/ccdb/complaints.csv.zip
2. Extract to: `data/complaints.csv`
3. See `data/DOWNLOAD_INSTRUCTIONS.md` for details

## Classification Categories
- 0: Credit reporting, repair, or other
- 1: Debt collection
- 2: Consumer Loan
- 3: Mortgage

## ML Pipeline

### 1. **Data Acquisition** (Automatic)
- Downloads 500k complaints from CFPB
- Extracts and caches locally
- Filters for 4 target categories
- Samples 10k per category (balanced)

### 2. **Exploratory Data Analysis**
- Class distribution visualization
- Text length and word count analysis
- Word clouds per category
- Statistical summaries

### 3. **Text Preprocessing**
- Lowercase conversion
- Special character removal
- Tokenization with NLTK
- Stopword removal
- Lemmatization

### 4. **Feature Engineering**
- TF-IDF vectorization
- Unigrams + Bigrams (500 features)
- Train/test split (80/20)
- Stratified sampling

### 5. **Model Training** (5 Algorithms)
- Logistic Regression
- Multinomial Naive Bayes
- Random Forest Classifier
- Linear SVM
- XGBoost Classifier

### 6. **Evaluation & Comparison**
- Accuracy, Precision, Recall, F1-Score
- Confusion matrices
- Feature importance analysis
- Model performance visualization

### 7. **Prediction & Deployment**
- Test on new complaint text
- Save best model + vectorizer
- Pickle files for production use

## Expected Performance (Real Data)

```
Model                 Accuracy  Training Time
Logistic Regression   83-85%    ~30 seconds
Naive Bayes           78-80%    ~10 seconds
Random Forest         87-89%    ~2 minutes
Linear SVM            85-87%    ~45 seconds
XGBoost              88-90%    ~3 minutes
```

## Documentation

- **REAL_DATA_QUICKSTART.md** - Complete guide for using real CFPB data
- **TASK5-SUMMARY.md** - Project overview and results
- **NOTEBOOK_GUIDE.md** - Step-by-step notebook walkthrough
- **data/DOWNLOAD_INSTRUCTIONS.md** - Dataset download help
5. Model Comparison
6. Evaluation
7. Prediction

Run the Jupyter notebook for complete analysis.
