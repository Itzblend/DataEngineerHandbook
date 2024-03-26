# Databricks


Considerations for moving to Databricks


## Azure

### Networking

When creating a Databricks instance in Azure, you have the option to attach it to a virtual network
or you can let it manage the network resources for you.

This introduces limitation because you will not have full permissions to the network resources
managed by Databricks.

This could prove to be detrimental if you want to connect into a storage account from your
Databricks instance. While attaching the Databricks Vnet, Azure will try to attach
"Microsoft.Storage"-service to the service endpoints of a subnet of the Databricks managed Vnet
and fails for the lack of permissions.

If you want to control the full networking options for you Databricks instance in Azure, I recommend
you create the Virtual Network prior to creating the Databricks instance and attaching it in creation.



### Data Versioning

If you have data in your Storage Account and wish to use them as versioned data objects from Databricks, you
need to first read the data with Spark and then save them as a Delta table.

This feels like a lot of investment into having your data in Databricks where compared to AWS Sagemaker, you
are able to create the datasets as objects in the Sagemaker without moving the data out of S3. Sagemaker can
then use the datasets like they are objects with different attributes like version number.

Coming from other Azure and AWS tools, I was quite suprised when i opened the "Data"-tab and clicked on the
"Azure Blob Storage" integration option and was greeted with a notebook of spark code on how to read my data
in a classic Spark fashion.
