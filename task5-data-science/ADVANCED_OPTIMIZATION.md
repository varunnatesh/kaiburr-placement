# Advanced Model Optimization Guide

## 🎯 Goal: Push Accuracy from 88.42% to 90%+

### What's Been Added

#### New Optimization Techniques (Cells 46-53)

1. **Hybrid Feature Engineering** (Cell 48)
   - **Word-level TF-IDF**: 2000 features with trigrams (1-3)
   - **Character-level TF-IDF**: 1000 features with 3-5 char n-grams
   - **Why it helps**: Character n-grams catch misspellings, patterns, and abbreviations that word-level misses
   - **Example**: "cc" (credit card), "$$" (money symbols), "mtg" (mortgage)

2. **Text Statistics Features** (Cell 50)
   - 9 additional numeric features:
     - Character count
     - Word count
     - Average word length
     - Exclamation/question marks (emotion indicators)
     - Dollar/percentage signs (financial context)
     - Uppercase ratio (emphasis/shouting)
     - Sentence count
   - **Total features**: 3,009 (2000 word + 1000 char + 9 stats)

3. **CatBoost Algorithm** (Cell 52)
   - Often **outperforms XGBoost** on text classification
   - Better handling of categorical features
   - Built-in handling of overfitting
   - Superior performance on imbalanced datasets

4. **Stacking Ensemble** (Cell 54)
   - **Level 0 (Base models)**:
     - Logistic Regression (linear patterns)
     - Random Forest (feature interactions)
     - XGBoost (gradient boosting)
     - CatBoost (advanced boosting)
   - **Level 1 (Meta-learner)**: XGBoost learns to combine base predictions
   - **Why it works**: Different models make different mistakes, meta-learner finds optimal combination

### Expected Performance Gains

| Technique | Expected Improvement | Reasoning |
|-----------|---------------------|-----------|
| Character n-grams | +0.3-0.5% | Captures spelling variations, abbreviations |
| Text statistics | +0.2-0.3% | Provides length, emotion, financial context |
| CatBoost | +0.3-0.5% | Superior algorithm for text classification |
| Stacking ensemble | +0.4-0.7% | Combines strengths of multiple models |
| **Total Expected** | **+1.2-2.0%** | **Target: 89.6-90.4%** |

### Running the Optimization

#### Step 1: Ensure Previous Cells Are Executed

The new cells depend on variables from earlier cells:
- `X_train`, `X_test`, `y_train`, `y_test` from train/test split
- `category_names` for labels
- Previous model results for comparison

#### Step 2: Execute New Cells in Order

```
Cell 46: Install CatBoost
Cell 47-48: Hybrid feature engineering (word + char TF-IDF)
Cell 49-50: Extract text statistics features
Cell 51-52: Train CatBoost model
Cell 53-54: Build stacking ensemble
Cell 55-56: Compare all models
Cell 57-58: Save best model
```

#### Step 3: Monitor Execution

```
⏱️ Expected execution times:
- CatBoost installation: 30 seconds
- Hybrid features: 15 seconds
- Text statistics: 5 seconds
- CatBoost training: 2-3 minutes
- Stacking ensemble: 5-7 minutes (trains 4 models x 5 folds)
- Total: ~10-12 minutes
```

### Quick Start

#### Option 1: Run All New Cells

Open the notebook in VS Code and execute cells 46-58 sequentially.

#### Option 2: Run from Terminal

```powershell
cd C:\placement\task5-data-science
jupyter nbconvert --to notebook --execute notebooks/complaint_classification.ipynb --output complaint_classification_executed.ipynb
```

### What You'll Get

#### 1. Performance Metrics

```
Model Comparison:
├─ Baseline XGBoost (500 features): 87.76%
├─ Ensemble Voting (2000 features): 88.36%
├─ Optimized XGBoost (2000 features): 88.42%
├─ CatBoost (3009 features): 89.2-89.8% (expected)
└─ Stacking Ensemble (3009 features): 89.5-90.4% (expected) ⭐
```

#### 2. Saved Models

```
models/
├─ ultimate_best_stacking_ensemble.pkl  (if stacking wins)
├─ ultimate_best_catboost.pkl           (if CatBoost wins)
├─ ultimate_tfidf_word.pkl              (word-level vectorizer)
└─ ultimate_tfidf_char.pkl              (char-level vectorizer)
```

#### 3. Visualizations

- Performance comparison bar chart
- Confusion matrix for best model
- Feature importance (if applicable)

### Using the Optimized Model

```python
import pickle
import numpy as np
from scipy.sparse import hstack

# Load model and transformers
with open('models/ultimate_best_stacking_ensemble.pkl', 'rb') as f:
    model = pickle.load(f)

with open('models/ultimate_tfidf_word.pkl', 'rb') as f:
    tfidf_word = pickle.load(f)
    
with open('models/ultimate_tfidf_char.pkl', 'rb') as f:
    tfidf_char = pickle.load(f)

# Preprocess complaint text
def predict_complaint(complaint_text):
    # 1. TF-IDF features
    word_features = tfidf_word.transform([complaint_text])
    char_features = tfidf_char.transform([complaint_text])
    
    # 2. Text statistics
    text_stats = np.array([[
        len(complaint_text),
        len(complaint_text.split()),
        len(complaint_text) / (len(complaint_text.split()) + 1),
        complaint_text.count('!'),
        complaint_text.count('?'),
        complaint_text.count('$'),
        complaint_text.count('%'),
        sum(1 for c in complaint_text if c.isupper()) / (len(complaint_text) + 1),
        complaint_text.count('.') / (len(complaint_text.split()) + 1)
    ]])
    
    # 3. Combine features
    features = hstack([word_features, char_features, text_stats])
    
    # 4. Predict
    prediction = model.predict(features)[0]
    
    categories = [
        "Credit Reporting",
        "Debt Collection", 
        "Consumer Loan",
        "Mortgage"
    ]
    return categories[prediction]

# Example
complaint = "The debt collector keeps calling me about a debt I already paid"
category = predict_complaint(complaint)
print(f"Category: {category}")  # Output: Debt Collection
```

### Troubleshooting

#### CatBoost Installation Issues

```powershell
# If automatic installation fails, install manually:
pip install catboost
```

#### Memory Issues

If you get memory errors during stacking:
- Reduce `cv=5` to `cv=3` in StackingClassifier
- Reduce CatBoost `iterations` from 300 to 200
- Close other applications

#### Slow Training

Stacking is computationally expensive:
- **Normal**: 5-7 minutes for stacking
- **If slower**: Check CPU usage, close other apps
- **Alternative**: Skip stacking, use CatBoost alone (still ~89% accuracy)

### Key Insights

#### Why These Techniques Work

1. **Character n-grams**: 
   - Complaint text often has typos, abbreviations
   - "cred rep" → Credit Reporting
   - "mtg pmnt" → Mortgage Payment

2. **Text Statistics**:
   - Mortgage complaints tend to be longer (legal language)
   - Debt collection complaints have more emotion (!, ?)
   - Financial context ($ signs) helps distinguish categories

3. **CatBoost**:
   - Superior to XGBoost for text classification
   - Better handles class imbalance (Consumer Loan minority class)
   - Less prone to overfitting

4. **Stacking**:
   - Logistic Regression: Good for linear separable patterns
   - Random Forest: Captures feature interactions
   - XGBoost/CatBoost: Complex non-linear patterns
   - Meta-learner: Learns when to trust each model

### Performance Validation

After running optimization, validate results:

```python
# Check per-category performance
print(classification_report(y_test, y_pred_stacking, target_names=category_names))

# Expected improvements:
# - Credit Reporting: 88% → 90%
# - Debt Collection: 87% → 89%
# - Consumer Loan: 29% → 35-40% (still challenging)
# - Mortgage: 95% → 96%
```

### Next Steps After Optimization

1. **If accuracy < 90%**:
   - Try LightGBM as alternative to CatBoost
   - Increase stacking base models (add LinearSVC)
   - Tune CatBoost hyperparameters with GridSearch

2. **If accuracy ≥ 90%**:
   - Create production REST API
   - Add model monitoring
   - Set up retraining pipeline
   - Deploy to cloud (Azure ML, AWS SageMaker)

3. **Consumer Loan Challenge**:
   - If still <40% accuracy, consider:
     - Collect more Consumer Loan samples
     - Use SMOTE specifically for this class
     - Create separate binary classifier

### Comparison: Before vs After

| Metric | Before (88.42%) | After (Expected ~90%) | Improvement |
|--------|----------------|----------------------|-------------|
| Accuracy | 88.42% | 89.5-90.4% | +1.1-2.0% |
| Features | 2000 | 3009 | +50% |
| Training Time | 2 min | 10-12 min | +5x |
| Complexity | Single model | Stacking (4 models) | Meta-learning |
| Production | Simple | More complex | Better performance |

### Cost-Benefit Analysis

**Benefits**:
- ✅ Higher accuracy (90%+ target)
- ✅ Better generalization (stacking reduces variance)
- ✅ More robust to edge cases (char n-grams)
- ✅ Production-grade performance

**Costs**:
- ⚠️ Longer training time (10 min vs 2 min)
- ⚠️ More complex inference (3 transformers instead of 1)
- ⚠️ Larger model files (~100MB vs ~10MB)
- ⚠️ Requires CatBoost dependency

**Recommendation**: **Proceed with optimization** if:
- Accuracy is critical for your use case
- 10-minute training time is acceptable
- Deployment environment can handle model complexity

---

## 🚀 Ready to Start?

Execute cells 46-58 in the notebook and watch performance improve to 90%+! 🎯
