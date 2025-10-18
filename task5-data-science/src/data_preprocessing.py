"""
Data Preprocessing Module for Consumer Complaint Classification
"""

import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

class TextPreprocessor:
    def __init__(self):
        """Initialize the preprocessor with NLTK components"""
        try:
            self.stop_words = set(stopwords.words('english'))
        except LookupError:
            nltk.download('stopwords')
            self.stop_words = set(stopwords.words('english'))
        
        try:
            self.lemmatizer = WordNetLemmatizer()
        except LookupError:
            nltk.download('wordnet')
            self.lemmatizer = WordNetLemmatizer()
        
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
    
    def clean_text(self, text):
        """
        Clean and normalize text
        
        Args:
            text (str): Input text
            
        Returns:
            str: Cleaned text
        """
        if pd.isna(text):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def remove_stopwords(self, text):
        """
        Remove stopwords from text
        
        Args:
            text (str): Input text
            
        Returns:
            str: Text without stopwords
        """
        tokens = word_tokenize(text)
        filtered_tokens = [word for word in tokens if word not in self.stop_words]
        return ' '.join(filtered_tokens)
    
    def lemmatize_text(self, text):
        """
        Lemmatize text
        
        Args:
            text (str): Input text
            
        Returns:
            str: Lemmatized text
        """
        tokens = word_tokenize(text)
        lemmatized = [self.lemmatizer.lemmatize(word) for word in tokens]
        return ' '.join(lemmatized)
    
    def preprocess(self, text):
        """
        Complete preprocessing pipeline
        
        Args:
            text (str): Input text
            
        Returns:
            str: Fully preprocessed text
        """
        text = self.clean_text(text)
        text = self.remove_stopwords(text)
        text = self.lemmatize_text(text)
        return text

def load_and_prepare_data(filepath, sample_size=None):
    """
    Load and prepare the consumer complaint dataset
    
    Args:
        filepath (str): Path to the CSV file
        sample_size (int, optional): Number of samples to load
        
    Returns:
        pd.DataFrame: Prepared dataframe
    """
    # Load data
    df = pd.read_csv(filepath, nrows=sample_size)
    
    # Define category mapping
    category_mapping = {
        'Credit reporting, credit repair services, or other personal consumer reports': 0,
        'Credit reporting, repair, or other': 0,
        'Debt collection': 1,
        'Consumer Loan': 2,
        'Mortgage': 3
    }
    
    # Filter for relevant categories
    df = df[df['Product'].isin(category_mapping.keys())].copy()
    
    # Map categories to numbers
    df['Category'] = df['Product'].map(category_mapping)
    
    # Use 'Consumer complaint narrative' as text feature
    df = df[['Consumer complaint narrative', 'Category']].dropna()
    df.columns = ['text', 'category']
    
    return df

def preprocess_dataframe(df):
    """
    Preprocess all text in a dataframe
    
    Args:
        df (pd.DataFrame): Input dataframe with 'text' column
        
    Returns:
        pd.DataFrame: Dataframe with preprocessed text
    """
    preprocessor = TextPreprocessor()
    df['processed_text'] = df['text'].apply(preprocessor.preprocess)
    return df

if __name__ == "__main__":
    # Example usage
    print("Text Preprocessing Module")
    print("=" * 50)
    
    # Test preprocessing
    preprocessor = TextPreprocessor()
    sample_text = "This is a SAMPLE text with numbers 123 and special chars!@#"
    print(f"Original: {sample_text}")
    print(f"Cleaned: {preprocessor.clean_text(sample_text)}")
    print(f"Processed: {preprocessor.preprocess(sample_text)}")
