import great_expectations as gx
from great_expectations.core.expectation_configuration import (
    ExpectationConfiguration
)
import pathlib

"""
Simple end to end example of creating reusable GX configs
"""


if __name__ == "__main__":
    context = gx.get_context(
        project_root_dir="data-quality/great-expectations"
    )

    titanic_suite = context.add_or_update_expectation_suite("titanic_suite")

    titanic_suite.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_values_to_be_in_set",
            kwargs={
                "column": "Sex",
                "value_set": ["male", "female"]
            }
        )
    )

    context.save_expectation_suite(expectation_suite=titanic_suite)

    titanic_datasource = context.sources.add_or_update_pandas_filesystem(
        name="titanic_datasource",
        base_directory=pathlib.Path("data-quality/great-expectations/data/")
    )

    titanic_data_asset = titanic_datasource.add_csv_asset(
        name="titanic_asset",
        batching_regex="titanic.csv"
    )

    titanic_batch_request = titanic_data_asset.build_batch_request()

    titanic_checkpoint = context.add_or_update_checkpoint(
        name="titanic_checkpoint",
        validations=[
            {
                "batch_request": titanic_batch_request,
                "expectation_suite_name": "titanic_suite",
            },
        ],
    )

    titanic_checkpoint_results = titanic_checkpoint.run()

    print(titanic_checkpoint_results)
    context.build_data_docs()
