from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
import lightgbm as lgb
import xgboost as xgb

from sklearn.preprocessing import StandardScaler
import pandas as pd
import os
from config.path_config import *
from src.logger import get_logger
from src.custom_exception import CustomException
import matplotlib.pyplot as plt
import time
import sys

from torch.utils.tensorboard import SummaryWriter

# Use non-GUI backend
import matplotlib
matplotlib.use('Agg')

logger = get_logger(__name__)


class ModelSelection:

    def __init__(self, data_path, sample_frac=0.1):
        self.data_path = data_path
        self.sample_frac = sample_frac
        run_id = time.strftime("%Y%m%d-%H%M%S")
        self.writer = SummaryWriter(log_dir=f"tensorboard_logs/run_{run_id}")

        self.models = {
            'Logistic Regression': LogisticRegression(max_iter=1000),
            'Random Forest': RandomForestClassifier(n_estimators=50, n_jobs=-1),
            'Gradient Boosting': GradientBoostingClassifier(n_estimators=50),
            'AdaBoost': AdaBoostClassifier(n_estimators=50),
            'Support Vector Classifier': SVC(),
            'K-Nearest Neighbors': KNeighborsClassifier(),
            'Naive Bayes': GaussianNB(),
            'Decision Tree': DecisionTreeClassifier(),
            'LightGBM': lgb.LGBMClassifier(),
            'XGBoost': xgb.XGBClassifier(eval_metric='mlogloss')
        }

        self.results = {}

    def load_data(self):
        try:
            logger.info("Loading CSV file")
            if not os.path.exists(self.data_path):
                raise FileNotFoundError(f"File not found at {self.data_path}")

            df = pd.read_csv(self.data_path)
            df_sample = df.sample(frac=self.sample_frac, random_state=42)
            X = df_sample.drop(columns='satisfaction')
            y = df_sample['satisfaction']

            logger.info("Data loaded and sampled successfully")
            return X, y
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise CustomException("Error while loading data", sys)

    def split_data(self, X, y):
        try:
            logger.info("Scaling and splitting data")
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            return train_test_split(X_scaled, y, test_size=0.2, random_state=42)
        except Exception as e:
            logger.error(f"Error splitting data: {str(e)}")
            raise CustomException("Error while splitting data", sys)

    def log_confusion_matrix(self, y_true, y_pred, step, model_name):
        try:
            cm = confusion_matrix(y_true, y_pred)
            fig, ax = plt.subplots(figsize=(5, 5))
            ax.matshow(cm, cmap=plt.cm.Blues, alpha=0.7)

            for i in range(cm.shape[0]):
                for j in range(cm.shape[1]):
                    ax.text(x=j, y=i, s=cm[i, j], va="center", ha="center")

            plt.xlabel("Predicted Labels")
            plt.ylabel("True Labels")
            plt.title(f"Confusion Matrix - {model_name}")

            self.writer.add_figure(f"Confusion_Matrix/{model_name}", fig, global_step=step)
            plt.close(fig)
        except Exception as e:
            logger.error(f"Error plotting confusion matrix: {str(e)}")

    def train_and_evaluate(self, X_train, X_test, y_train, y_test):
        try:
            logger.info("Training and evaluating models")
            for idx, (name, model) in enumerate(self.models.items()):
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)

                accuracy = accuracy_score(y_test, y_pred)
                precision = precision_score(y_test, y_pred, average="weighted", zero_division=0)
                recall = recall_score(y_test, y_pred, average="weighted", zero_division=0)
                f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)

                self.results[name] = {'accuracy': accuracy, 'precision': precision, 'recall': recall, 'f1_score': f1}
                logger.info(f"{name} Metrics: Accuracy: {accuracy}, Precision: {precision}, Recall: {recall}, F1 Score: {f1}")

                self.writer.add_scalar(f'Accuracy/{name}', accuracy, idx)
                self.writer.add_scalar(f'Precision/{name}', precision, idx)
                self.writer.add_scalar(f'Recall/{name}', recall, idx)
                self.writer.add_scalar(f'F1_score/{name}', f1, idx)

                self.log_confusion_matrix(y_test, y_pred, idx, name)
            self.writer.close()
        except Exception as e:
            logger.error(f"Error during training and evaluation: {str(e)}")
            raise CustomException("Error while training and evaluating", sys)

    def run(self):
        try:
            logger.info("Starting ModelSelection pipeline")
            X, y = self.load_data()
            X_train, X_test, y_train, y_test = self.split_data(X, y)
            self.train_and_evaluate(X_train, X_test, y_train, y_test)
            logger.info("Pipeline completed successfully")
        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}")
            raise CustomException("Error in the pipeline", sys)


if __name__ == "__main__":
    model_selection = ModelSelection(ENGINEERED_DATA_PATH)
    model_selection.run()