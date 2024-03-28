# Lift and Shift

Moving to cloud with MLOps has been made super easy. Even the tooling around MLOps topics are
super similar with each other across different public clouds.

What is expected from a end-to-end MLOps solutions:
- Storage integrations
- Role Based Access Control
- Seamless workflow with cloud compute
- Managed inference
- Model versioning

With a good MLOps solutions, you shouldn't need to have cloud-specific code in your
model training script. Everything that you need to deploy your models to cloud should
be in an external script or a lightweight wrapper.

Let's take and example from AWS Sagemaker

Lift & Shift model training script
```py
"""
Local usage: python script.py \
  --model-dir models \
  --train-dir data/train/ \
  --test-dir data/test/ \
  --features "Pclass Sex SibSp Parch" \
  --target "Survived"
"""

import argparse
import joblib
import os

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from io import StringIO
import sklearn

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-estimators", type=int, default=10)

    # Data, model, and output directories
    parser.add_argument("--model-dir", type=str, default=os.environ.get("SM_MODEL_DIR"))
    parser.add_argument("--train-dir", type=str, default=os.environ.get("SM_CHANNEL_TRAIN"))
    parser.add_argument("--test-dir", type=str, default=os.environ.get("SM_CHANNEL_TEST"))
    parser.add_argument("--train-file", type=str, default="train.csv")
    parser.add_argument("--test-file", type=str, default="test.csv")
    parser.add_argument(
        "--features", type=str
    )
    parser.add_argument(
        "--target", type=str
    )

    args, _ = parser.parse_known_args()

    train_df = pd.read_csv(os.path.join(args.train_dir, args.train_file))
    test_df = pd.read_csv(os.path.join(args.test_dir, args.test_file))

    X_train = pd.get_dummies(train_df[args.features.split()])
    y_train = train_df[args.target]
    X_test = pd.get_dummies(test_df[args.features.split()])
    y_test = test_df[args.target]

    model = RandomForestClassifier(
        n_estimators=args.n_estimators, max_depth=5, random_state=1
    )

    model.fit(X_train.values, y_train)

    # persist model
    path = os.path.join(args.model_dir, "model.joblib")
    joblib.dump(model, path)
```

This is a script you can use to train your model locally as well as in Sagemaker
and the only AWS specific values in this are SM_MODEL_DIR, SM_CHANNEL_TRAIN and SM_CHANNEL_TEST
which you will be able to override when running locally.

The environment variables listed above are present in the environments that Sagemaker deploys
when running your code.

Now how can we run this code in Sagemaker? For that we'll need an Estimator

```py
from sagemaker.sklearn.estimator import SKLearn

role = os.environ.get("SAGEMAKER_ROLE")

sklearn_estimator = SKLearn(
  entry_point="src/titanic/script.py",
  role=role,
  instance_count=1,
  instance_type="ml.m4.xlarge",
  framework_version=FRAMEWORK_VERSION,
  base_job_name="rf-scikit",
  hyperparameters={
    "n-estimators": 100,
    "features": "Pclass Sex SibSp Parch",
    "target": "Survived",
  },
)

sklearn_estimator.fit({"train": "s3://<bucket>/titanic/train.csv",
                       "test": "s3://<bucket>/titanic/test.csv"})

```

The estimator is a wrapper around our sklearn model and we pass it the suitable arguments.
The command that Sagemaker runs translates into the script below, overriding all the local arguments
and telling sagemaker what script to run and where it can read the data for the model

```sh
miniconda script.py \
  --n-estimators 100 \
  --features "Pclass Sex SibSp Parch" \
  --target Survived \
  --train s3://<bucket>/titanic/train.csv,
  --test s3://<bucket>/titanic/test.csv
```


