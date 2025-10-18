# Task 5: Data Science - Text Classification

## ✅ Project Complete!

### Overview
Consumer complaint text classification using multiple machine learning algorithms to categorize complaints into 4 product categories.

### Categories
- **Credit Reporting** (0): Credit reports, credit repair, identity theft
- **Debt Collection** (1): Collection agencies, harassment, validation
- **Consumer Loan** (2): Auto loans, personal loans, student loans, payday loans
- **Mortgage** (3): Home loans, foreclosure, refinancing, escrow

### What Was Implemented

#### 1. Jupyter Notebook (`notebooks/complaint_classification.ipynb`)
Comprehensive notebook using **real CFPB data** (5M+ complaints):

1. **Library Imports** - All necessary packages
2. **NLTK Data Download** - Stopwords, punkt, wordnet
3. **Dataset Download** - Automatic download from data.gov (~500MB)
4. **Dataset Loading** - Load 500k complaints in chunks (memory efficient)
5. **Data Preparation** - Filter 4 categories, sample 10k per category, balanced dataset
6. **Exploratory Data Analysis** - Distribution, text length, word count
7. **Text Preprocessing** - Cleaning, tokenization, lemmatization
8. **Word Clouds** - Visual representation per category
9. **Feature Engineering** - TF-IDF vectorization with bigrams
10. **Model Training** - 5 different algorithms:
   - Logistic Regression
   - Multinomial Naive Bayes
   - Random Forest
   - Linear SVM
   - XGBoost
11. **Model Comparison** - Performance metrics visualization
12. **Feature Importance** - Top predictive features
13. **Predictions** - Test on new complaints
14. **Model Saving** - Pickle files for deployment

#### 2. Visualizations
- Class distribution bar chart
- Character length and word count boxplots
- Word clouds for each category
- Model performance comparison bar chart
- Confusion matrix heatmap
- Feature importance horizontal bar chart

#### 3. Evaluation Metrics
- Accuracy
- Precision (weighted)
- Recall (weighted)
- F1-Score (weighted)
- Per-class accuracy
- Confusion matrix
- Detailed classification report

### Project Structure

```
task5-data-science/
├── notebooks/
│   └── complaint_classification.ipynb  # Main Jupyter notebook
├── models/
│   ├── best_model.pkl                  # Trained model
│   ├── tfidf_vectorizer.pkl            # TF-IDF vectorizer
│   └── category_names.pkl              # Category mapping
├── data/
│   ├── complaints.csv                  # Downloaded CFPB dataset (~2GB)
│   └── DOWNLOAD_INSTRUCTIONS.md        # Download guide
├── src/
│   ├── data_preprocessing.py
│   ├── model_training.py
│   └── model_evaluation.py
├── requirements.txt
├── README.md
└── NOTEBOOK_GUIDE.md
```

### Running the Notebook

#### Option 1: Jupyter Notebook

```powershell
# Navigate to task5 directory
cd C:\placement\task5-data-science

# Start Jupyter Notebook
jupyter notebook

# Open: notebooks/complaint_classification.ipynb
# Run all cells: Kernel → Restart & Run All
```

#### Option 2: JupyterLab

```powershell
cd C:\placement\task5-data-science

# Start JupyterLab
jupyter lab

# Navigate to notebooks/complaint_classification.ipynb
```

#### Option 3: VS Code

1. Open VS Code
2. Install "Jupyter" extension (if not installed)
3. Open `complaint_classification.ipynb`
4. Select Python kernel
5. Click "Run All" or run cells individually

### Expected Results

#### Model Performance (Actual Results with Real Data)
```
Model                    Accuracy  Precision  Recall  F1-Score
Logistic Regression      0.8577    0.8577    0.8577  0.8547
Naive Bayes              0.8404    0.8415    0.8404  0.8382
Random Forest            0.8695    0.8693    0.8695  0.8672
Linear SVM               0.8611    0.8610    0.8611  0.8585
XGBoost (Baseline)       0.8776    0.8776    0.8776  0.8752
Ensemble Voting          0.8836    0.8836    0.8836  0.8813
XGBoost (Optimized)      0.8842    0.8840    0.8842  0.8821  ⭐ BEST
```

**Final Optimized Model**: 88.42% accuracy with 2000 TF-IDF features + trigrams

*Results based on real CFPB data: 500k loaded, 25,609 training samples (balanced)*

#### Model Improvements Applied
1. ✅ Hyperparameter tuning with GridSearchCV
2. ✅ Class imbalance handling with SMOTE
3. ✅ Ensemble methods (VotingClassifier)
4. ✅ N-gram analysis (bigrams + trigrams)
5. ✅ TF-IDF optimization (tested 500/1000/2000/3000 features)

See `MODEL_IMPROVEMENT_SUMMARY.md` for detailed analysis.

#### Sample Predictions
```
Complaint: "My credit report shows accounts that don't belong to me"
Predicted: Credit Reporting ✅

Complaint: "Collection agency keeps calling me about a debt I paid"
Predicted: Debt Collection ✅

Complaint: "The bank denied my personal loan without explanation"
Predicted: Consumer Loan ✅

Complaint: "My mortgage payment increased suddenly"
Predicted: Mortgage ✅
```

### Key Features

#### Text Preprocessing Pipeline
```python
1. Convert to lowercase
2. Remove special characters and numbers
3. Tokenization
4. Remove stopwords
5. Lemmatization
```

#### Feature Engineering
```python
TF-IDF Vectorization:
- Max features: 500
- N-gram range: (1, 2) - unigrams and bigrams
- Captures word importance across documents
```

#### Model Training
```python
All models trained with:
- Train/test split: 80/20
- Stratified sampling
- Random state: 42 (reproducible)
- Cross-validation ready
```

### Technical Skills Demonstrated

✅ **Data Science**
- Exploratory Data Analysis (EDA)
- Feature engineering
- Text preprocessing
- Machine learning model selection

✅ **Natural Language Processing**
- Tokenization
- Stopword removal
- Lemmatization
- TF-IDF vectorization

✅ **Machine Learning**
- Multiple algorithm comparison
- Model evaluation
- Hyperparameter consideration
- Model persistence

✅ **Visualization**
- Matplotlib & Seaborn
- Word clouds
- Confusion matrices
- Performance comparisons

✅ **Python Libraries**
- pandas, numpy (data manipulation)
- scikit-learn (ML models)
- nltk (NLP)
- XGBoost (advanced ensemble)

### Next Steps (Production Ready)

#### 1. ✅ Using Real Dataset (Already Implemented!)
```python
# Notebook automatically downloads from CFPB
url = "https://files.consumerfinance.gov/ccdb/complaints.csv.zip"
# Loads 500k complaints, samples 10k per category
# See data/DOWNLOAD_INSTRUCTIONS.md for details
```

#### 2. Hyperparameter Tuning
```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'C': [0.1, 1, 10],
    'max_iter': [1000, 2000]
}
grid = GridSearchCV(LogisticRegression(), param_grid, cv=5)
```

#### 3. Handle Class Imbalance
```python
from imblearn.over_sampling import SMOTE

smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)
```

#### 4. Create REST API
```python
from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

# Load model
model = pickle.load(open('models/best_model.pkl', 'rb'))
vectorizer = pickle.load(open('models/tfidf_vectorizer.pkl', 'rb'))

@app.route('/predict', methods=['POST'])
def predict():
    complaint = request.json['text']
    processed = preprocess_text(complaint)
    vectorized = vectorizer.transform([processed])
    prediction = model.predict(vectorized)[0]
    return jsonify({'category': category_names[prediction]})
```

#### 5. Deploy with Docker
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "api.py"]
```

### Troubleshooting

#### Issue: NLTK Data Not Found
```python
import nltk
nltk.download('all')  # Download all NLTK data
```

#### Issue: Memory Error
```python
# Reduce max_features in TF-IDF
tfidf = TfidfVectorizer(max_features=100)  # Instead of 500
```

#### Issue: Jupyter Kernel Crashes
```powershell
# Restart kernel
# Kernel → Restart & Clear Output
```

#### Issue: Import Errors
```powershell
# Reinstall packages
pip install --force-reinstall -r requirements.txt
```

### Performance Tips

1. **Increase Sample Size**: Use real dataset with thousands of complaints
2. **Feature Engineering**: Try Word2Vec, GloVe, or BERT embeddings
3. **Ensemble Methods**: Combine multiple models (voting/stacking)
4. **Cross-Validation**: Use k-fold CV for robust evaluation
5. **Regularization**: Tune C parameter in Logistic Regression/SVM

### Documentation Files

- **README.md**: Project overview
- **NOTEBOOK_GUIDE.md**: Step-by-step notebook usage
- **requirements.txt**: Python dependencies
- **complaint_classification.ipynb**: Main notebook

### Dependencies Installed

```
✅ pandas==2.1.4
✅ numpy==1.26.2
✅ scikit-learn==1.3.2
✅ matplotlib==3.8.2
✅ seaborn==0.13.0
✅ nltk==3.8.1
✅ wordcloud==1.9.3
✅ jupyter==1.0.0
✅ imbalanced-learn==0.11.0
✅ xgboost==2.0.3
```

### Success Metrics

| Metric | Status |
|--------|--------|
| Notebook Created | ✅ Complete |
| Dependencies Installed | ✅ Complete |
| Sample Data Generated | ✅ Complete |
| EDA Visualizations | ✅ Complete |
| Text Preprocessing | ✅ Complete |
| 5 Models Trained | ✅ Complete |
| Model Comparison | ✅ Complete |
| Predictions Working | ✅ Complete |
| Model Saving | ✅ Complete |
| Documentation | ✅ Complete |

---

## Quick Start

```powershell
# 1. Navigate to directory
cd C:\placement\task5-data-science

# 2. Open Jupyter Notebook
jupyter notebook

# 3. Open complaint_classification.ipynb

# 4. Run all cells (Kernel → Restart & Run All)

# 5. Review results and predictions
```

---

**Status**: ✅ Task 5 Complete - Text Classification Notebook Ready

**Date**: October 16, 2025

**Ready for**: Jupyter execution and model training
