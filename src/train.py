import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.datasets import load_breast_cancer


def train_rclf_model():
    """
    Train a Random Forest Classifier model on the breast cancer dataset
    and log model parameters and metrics using MLflow.
    """
    # Load breast cancer dataset
    data = load_breast_cancer()
    X_train, X_test, y_train, y_test = train_test_split(
        data.data, data.target, test_size=0.2, random_state=42
    )

    # Mflow experiment
    mlflow.set_experiment("breast_cancer")

    # Start MLflow run
    with mlflow.start_run(run_name="random_forest_classifier"):
        n_estimators = 100
        model = RandomForestClassifier(n_estimators=n_estimators)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)

        # Log model parameters and metrics
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)

        # Log model
        mlflow.sklearn.log_model(
            model, "sklearn_breast_cancer_classifier", input_example=X_train[:1]
        )

        # Print metrics
        print(f"Accuracy: {accuracy}")
        print(f"Precision: {precision}")
        print(f"Recall: {recall}")


if __name__ == "__main__":
    train_rclf_model()
