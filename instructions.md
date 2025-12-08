Follow the below steps:

1. use the merimaid-diagram-creator skill to create a workflow diagram based on the notebooks in @notebooks, it is a linear workflow in the oorder of noteboo prefix
2. use the databricks-asset-bundle skill to set up a databricks asset bundle based on the mermaid diagram from step 1 with the notebooks, use the e2_demo_fieldeng profile for databricks workspace
3. use the pytest-test-creator to create and perform the unit test on the notebook code 
4. use the python-code-format to format the notebook code
5. validate, deploy, and run the asset bundle on databricks using the DEFAULT profile and dev target, make sure the job complete
6. Update an @README to document the asset bundle, includes the worklow diagram image in the readme.
