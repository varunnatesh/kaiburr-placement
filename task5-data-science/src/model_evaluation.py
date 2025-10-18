"""
Model Evaluation Module for Consumer Complaint Classification
"""

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix, roc_auc_score, roc_curve
)
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

class ModelEvaluator:
    def __init__(self, category_names=None):
        """
        Initialize the evaluator
        
        Args:
            category_names (dict): Mapping of category numbers to names
        """
        if category_names is None:
            self.category_names = {
                0: 'Credit reporting',
                1: 'Debt collection',
                2: 'Consumer Loan',
                3: 'Mortgage'
            }
        else:
            self.category_names = category_names
    
    def evaluate_model(self, model, X_test, y_test):
        """
        Evaluate a model comprehensively
        
        Args:
            model: Trained model
            X_test: Test features
            y_test: True labels
            
        Returns:
            dict: Evaluation metrics
        """
        # Make predictions
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision_macro': precision_score(y_test, y_pred, average='macro'),
            'recall_macro': recall_score(y_test, y_pred, average='macro'),
            'f1_macro': f1_score(y_test, y_pred, average='macro'),
            'precision_weighted': precision_score(y_test, y_pred, average='weighted'),
            'recall_weighted': recall_score(y_test, y_pred, average='weighted'),
            'f1_weighted': f1_score(y_test, y_pred, average='weighted'),
        }
        
        return metrics
    
    def get_classification_report(self, model, X_test, y_test):
        """
        Get detailed classification report
        
        Args:
            model: Trained model
            X_test: Test features
            y_test: True labels
            
        Returns:
            str: Classification report
        """
        y_pred = model.predict(X_test)
        return classification_report(
            y_test, y_pred,
            target_names=[self.category_names[i] for i in sorted(self.category_names.keys())]
        )
    
    def plot_confusion_matrix(self, model, X_test, y_test, figsize=(10, 8)):
        """
        Plot confusion matrix
        
        Args:
            model: Trained model
            X_test: Test features
            y_test: True labels
            figsize (tuple): Figure size
        """
        y_pred = model.predict(X_test)
        cm = confusion_matrix(y_test, y_pred)
        
        plt.figure(figsize=figsize)
        sns.heatmap(
            cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=[self.category_names[i] for i in sorted(self.category_names.keys())],
            yticklabels=[self.category_names[i] for i in sorted(self.category_names.keys())]
        )
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.tight_layout()
        plt.show()
    
    def compare_models(self, models_dict, X_test, y_test):
        """
        Compare multiple models
        
        Args:
            models_dict (dict): Dictionary of model_name: model
            X_test: Test features
            y_test: True labels
            
        Returns:
            pd.DataFrame: Comparison dataframe
        """
        results = []
        
        for name, model in models_dict.items():
            metrics = self.evaluate_model(model, X_test, y_test)
            metrics['Model'] = name
            results.append(metrics)
        
        df = pd.DataFrame(results)
        df = df[['Model', 'accuracy', 'precision_weighted', 'recall_weighted', 'f1_weighted']]
        return df.sort_values('f1_weighted', ascending=False)
    
    def plot_model_comparison(self, comparison_df, figsize=(12, 6)):
        """
        Plot model comparison
        
        Args:
            comparison_df (pd.DataFrame): Dataframe from compare_models
            figsize (tuple): Figure size
        """
        metrics = ['accuracy', 'precision_weighted', 'recall_weighted', 'f1_weighted']
        
        fig, axes = plt.subplots(1, len(metrics), figsize=figsize)
        
        for idx, metric in enumerate(metrics):
            ax = axes[idx]
            comparison_df.plot(
                x='Model', y=metric, kind='bar', ax=ax,
                legend=False, color='skyblue'
            )
            ax.set_title(metric.replace('_', ' ').title())
            ax.set_xlabel('')
            ax.set_ylabel('Score')
            ax.set_ylim([0, 1])
            ax.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.show()
    
    def plot_feature_importance(self, model, vectorizer, top_n=20, figsize=(12, 8)):
        """
        Plot feature importance (for models that support it)
        
        Args:
            model: Trained model
            vectorizer: Fitted vectorizer
            top_n (int): Number of top features to show
            figsize (tuple): Figure size
        """
        if hasattr(model, 'feature_importances_'):
            # Tree-based models
            importances = model.feature_importances_
            feature_names = vectorizer.get_feature_names_out()
            
            indices = np.argsort(importances)[::-1][:top_n]
            
            plt.figure(figsize=figsize)
            plt.title(f'Top {top_n} Feature Importances')
            plt.bar(range(top_n), importances[indices])
            plt.xticks(range(top_n), [feature_names[i] for i in indices], rotation=45, ha='right')
            plt.tight_layout()
            plt.show()
        
        elif hasattr(model, 'coef_'):
            # Linear models
            n_classes = model.coef_.shape[0]
            feature_names = vectorizer.get_feature_names_out()
            
            fig, axes = plt.subplots(n_classes, 1, figsize=figsize)
            
            for idx in range(n_classes):
                coef = model.coef_[idx]
                top_indices = np.argsort(np.abs(coef))[::-1][:top_n]
                
                ax = axes[idx] if n_classes > 1 else axes
                ax.barh(range(top_n), coef[top_indices])
                ax.set_yticks(range(top_n))
                ax.set_yticklabels([feature_names[i] for i in top_indices])
                ax.set_title(f'Top {top_n} Features for Class {self.category_names[idx]}')
                ax.set_xlabel('Coefficient Value')
            
            plt.tight_layout()
            plt.show()
        else:
            print("Feature importance not available for this model type")
    
    def plot_roc_curves(self, model, X_test, y_test, figsize=(10, 8)):
        """
        Plot ROC curves for multi-class classification
        
        Args:
            model: Trained model
            X_test: Test features
            y_test: True labels
            figsize (tuple): Figure size
        """
        from sklearn.preprocessing import label_binarize
        from sklearn.metrics import auc
        
        # Binarize labels
        y_test_bin = label_binarize(y_test, classes=sorted(self.category_names.keys()))
        n_classes = y_test_bin.shape[1]
        
        # Get predictions
        if hasattr(model, 'predict_proba'):
            y_score = model.predict_proba(X_test)
        else:
            print("Model does not support probability predictions")
            return
        
        # Plot ROC curve for each class
        plt.figure(figsize=figsize)
        
        for i in range(n_classes):
            fpr, tpr, _ = roc_curve(y_test_bin[:, i], y_score[:, i])
            roc_auc = auc(fpr, tpr)
            plt.plot(fpr, tpr, label=f'{self.category_names[i]} (AUC = {roc_auc:.2f})')
        
        plt.plot([0, 1], [0, 1], 'k--', label='Random Classifier')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curves for Multi-Class Classification')
        plt.legend(loc='lower right')
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    print("Model Evaluation Module")
    print("=" * 50)
    print("Available evaluation metrics:")
    print("- Accuracy")
    print("- Precision (Macro & Weighted)")
    print("- Recall (Macro & Weighted)")
    print("- F1-Score (Macro & Weighted)")
    print("- Confusion Matrix")
    print("- ROC Curves")
    print("- Feature Importance")
