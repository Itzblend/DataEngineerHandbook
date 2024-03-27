# Integrations

INSTRUCTIONS TO RETRIEVE DATA FROM DATA STORE IS NOT AN INTEGRATION!!!!


Characteristics of a good data platform integration
- No initial data transfer*
- Versioning
- Abstraction?

*An object exists of the data without having to read the actual data


|Name|Type|Current version|Latest version|Created time|Modified time|
--- |--- | --- | --- | --- | ---|
|titanic-test|File(uri_file)|2|1|Feb 25, 2024 2:21 PM|Feb 28, 2024 9:46 AM


Above is an example from Azure Machine Learning Studio about what information is available
of your data without moving the data out of Azure Storage Account

And below is an example how you would read the data in Azure ML .

```py
import pandas as pd
from azure.ai.ml import MLClient, command, Input
from azure.identity import DefaultAzureCredential
from azure.ai.ml.constants import AssetTypes, InputOutputModes

ml_client = MLClient.from_config(credential=DefaultAzureCredential())
data_asset = ml_client.data.get("titanic-test", version="2")

# Use pandas to read with the path to Storage Account
df = pd.read_csv(data_asset.path)

# Or use the Input class to point to the data asset id
job = command(
        command='ls "${{inputs.data}}"',
        inputs={
          "data": Input(path=data_asset.id,
              type=AssetTypes.URI_FILE,
              mode=InputOutputModes.RO_MOUNT
              )
          },
        environment="azureml:AzureML-sklearn-1.0-ubuntu20.04-py38-cpu@latest"
      )
```

You should already see how this type of abstraction around your data gives you
security with the versioning 


Instead how does Databricks handle this? They give you a notebook.
What does the notebook say? "Read it with spark"

```
storage_account_name = "STORAGE_ACCOUNT_NAME"
storage_account_access_key = "YOUR_ACCESS_KEY"

file_location = "wasbs://example/location"
file_type = "csv"

df = spark.read.format(file_type).option("inferSchema", "true").load(file_location)
```

Would you call this an integration? - Well luckily Databricks doesn't call it that, but many of your AI powered start ups do

WIP!
must address about data abstractions:
- Azure ML doesnt offer integration outside of Azure -> Vendor Lock
-> Not perfect but still doesnt give excuse to Databricks in Azure
-> The similar tool AWS Sagemaker is very similar with how it operates
  -> If you cant move your data out of AWS, make sure your models are lift&shift -able



### Examples

[Deepnote](https://deepnote.com/docs/azure-blob-storage)

[Data Versioning in Databricks](./Analytics/Databricks/databricks.md#data-versioning)
