import great_expectations as gx
from great_expectations.core.expectation_configuration import (
    ExpectationConfiguration
)


if __name__ == "__main__":

    context = gx.get_context(
        project_root_dir="data-quality/great-expectations"
    )

    taxi_suite = context.add_or_update_expectation_suite("taxi_suite")

    taxi_suite.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_values_to_be_in_set",
            kwargs={
                "column": "VendorID",
                "value_set": [1, 2]
            }
        )
    )

    context.save_expectation_suite(expectation_suite=taxi_suite)

    azure_options = {
        "conn_str": "AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;DefaultEndpointsProtocol=http;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;TableEndpoint=http://127.0.0.1:10002/devstoreaccount1;"
    }
    taxi_datasource_azure = context.sources.add_or_update_pandas_abs(
        "taxi_datasource_azure",
        azure_options=azure_options
    )

    taxi_data_asset = taxi_datasource_azure.add_csv_asset(
        name="taxi_asset",
        abs_container="taxi",
        abs_name_starts_with="yellow_taxi",
        batching_regex=r"yellow_tripdata_(?P<year>\d{4})-(?P<seq>\d{2})\.csv",
        order_by=["+year", "+seq"]
    )

    taxi_batch_request = taxi_data_asset.build_batch_request()

    taxi_checkpoint = context.add_or_update_checkpoint(
        name="taxi_checkpoint",
        validations=[
            {
                "batch_request": taxi_batch_request,
                "expectation_suite_name": "taxi_suite",
            },
        ],
    )

    # Run with custom batch
    batch_request = taxi_data_asset.build_batch_request(
        options={
            "year": "2023",
            "seq": "02"
        }
    )

    taxi_checkpoint.validations.clear()
    result = taxi_checkpoint.run(
        validations=[
            {
                "batch_request": batch_request,
                "expectation_suite_name": "taxi_suite"
            }
        ]
    )

    print(result.to_json_dict())
