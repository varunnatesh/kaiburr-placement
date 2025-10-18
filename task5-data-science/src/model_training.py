"""
Model Training Module for Consumer Complaint Classification
"""

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from xgboost import XGBClassifier
import joblib
import numpy as np

class ModelTrainer:
    def __init__(self):
        """Initialize the model trainer"""
        self.vectorizer = None
        self.models = {}
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        
    def prepare_features(self, df, test_size=0.2, random_state=42, vectorizer_type='tfidf'):
        """
        Prepare features using TF-IDF or Count Vectorizer
        
        Args:
            df (pd.DataFrame): Dataframe with 'processed_text' and 'category' columns
            test_size (float): Proportion of test set
            random_state (int): Random seed
            vectorizer_type (str): 'tfidf' or 'count'
            
        Returns:
            tuple: X_train, X_test, y_train, y_test
        """
        # Split data
        X = df['processed_text']
        y = df['category']
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        # Initialize vectorizer
        if vectorizer_type == 'tfidf':
            self.vectorizer = TfidfVectorizer(
                max_features=5000,
                ngram_range=(1, 2),
                min_df=2,
                max_df=0.8
            )
        else:
            self.vectorizer = CountVectorizer(
                max_features=5000,
                ngram_range=(1, 2),
                min_df=2,
                max_df=0.8
            )
        
        # Fit and transform
        self.X_train = self.vectorizer.fit_transform(X_train)
        self.X_test = self.vectorizer.transform(X_test)
        self.y_train = y_train
        self.y_test = y_test
        
        return self.X_train, self.X_test, self.y_train, self.y_test
    
    def train_logistic_regression(self, max_iter=1000):
        """Train Logistic Regression model"""
        print("Training Logistic Regression...")
        model = LogisticRegression(
            max_iter=max_iter,
            random_state=42,
            multi_class='multinomial',
            solver='lbfgs',
            n_jobs=-1
        )
        model.fit(self.X_train, self.y_train)
        self.models['Logistic Regression'] = model
        return model
    
    def train_naive_bayes(self):
        """Train Multinomial Naive Bayes model"""
        print("Training Naive Bayes...")
        model = MultinomialNB(alpha=1.0)
        model.fit(self.X_train, self.y_train)
        self.models['Naive Bayes'] = model
        return model
    
    def train_random_forest(self, n_estimators=100):
        """Train Random Forest model"""
        print("Training Random Forest...")
        model = RandomForestClassifier(
            n_estimators=n_estimators,
            random_state=42,
            n_jobs=-1,
            max_depth=20
        )
        model.fit(self.X_train, self.y_train)
        self.models['Random Forest'] = model
        return model
    
    def train_svm(self):
        """Train Linear SVM model"""
        print("Training SVM...")
        model = LinearSVC(
            random_state=42,
            max_iter=1000,
            dual=False
        )
        model.fit(self.X_train, self.y_train)
        self.models['SVM'] = model
        return model
    
    def train_xgboost(self, n_estimators=100):
        """Train XGBoost model"""
        print("Training XGBoost...")
        model = XGBClassifier(
            n_estimators=n_estimators,
            random_state=42,
            n_jobs=-1,
            max_depth=6,
            learning_rate=0.1
        )
        model.fit(self.X_train, self.y_train)
        self.models['XGBoost'] = model
        return model
    
    def train_all_models(self):
        """Train all models"""
        self.train_logistic_regression()
        self.train_naive_bayes()
        self.train_random_forest()
        self.train_svm()
        self.train_xgboost()
        return self.models
    
    def cross_validate(self, model, cv=5):
        """
        Perform cross-validation
        
        Args:
            model: Trained model
            cv (int): Number of folds
            
        Returns:
            dict: Cross-validation scores
        """
        scores = cross_val_score(model, self.X_train, self.y_train, cv=cv)
        return {
            'mean': scores.mean(),
            'std': scores.std(),
            'scores': scores
        }
    
    def save_model(self, model, model_name, filepath):
        """
        Save model and vectorizer
        
        Args:
            model: Trained model
            model_name (str): Name of the model
            filepath (str): Directory to save
        """
        joblib.dump(model, f'{filepath}/{model_name}_model.pkl')
        joblib.dump(self.vectorizer, f'{filepath}/{model_name}_vectorizer.pkl')
        print(f"Model saved: {model_name}")
    
    def load_model(self, model_name, filepath):
        """
        Load model and vectorizer
        
        Args:
            model_name (str): Name of the model
            filepath (str): Directory to load from
            
        Returns:
            tuple: (model, vectorizer)
        """
        model = joblib.load(f'{filepath}/{model_name}_model.pkl')
        vectorizer = joblib.load(f'{filepath}/{model_name}_vectorizer.pkl')
        return model, vectorizer
    
    def predict(self, model, texts):
        """
        Make predictions on new texts
        
        Args:
            model: Trained model
            texts (list): List of text strings
            
        Returns:
            np.array: Predictions
        """
        X = self.vectorizer.transform(texts)
        return model.predict(X)
    
    def predict_proba(self, model, texts):
        """
        Get prediction probabilities
        
        Args:
            model: Trained model
            texts (list): List of text strings
            
        Returns:
            np.array: Prediction probabilities
        """
        X = self.vectorizer.transform(texts)
        return model.predict_proba(X)

if __name__ == "__main__":
    print("Model Training Module")
    print("=" * 50)
    print("Available models:")
    print("1. Logistic Regression")
    print("2. Naive Bayes")
    print("3. Random Forest")
    print("4. SVM")
    print("5. XGBoost")
