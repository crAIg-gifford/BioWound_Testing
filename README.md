## Overview
This tool automates the process of verifying insurance eligibility for patients by interfacing with pVerify's API. It processes patient data from Excel files and generates detailed eligibility responses.

## Features
- Processes patient data from Excel spreadsheets
- Handles multiple insurance payers
- Exports responses as JSON files
- Returns IVR results in JSON format by Subscriber Name

## Links
- [pVerify API Documentation](https://pverify.com/api-documentation/)
- [pVerify Payer List](https://pverify.com/payer-list/)
- [pVerify Cost Calculator](https://docs.google.com/spreadsheets/d/1YNJ-GKqILvrFeaFD969Txb1CK0GqmyCgpg2xWQFXIK0/edit?gid=0#gid=0)
- [Stedi API Documentation](https://www.stedi.com/docs/api-reference/healthcare/post-healthcare-eligibility)
- [Stedi Payer List](https://www.stedi.com/healthcare/network)
- 
## Steps
1. Create a .env file in the root directory and cp the data found in [Bitwarden -> Portal Aggregator -> pVerify -> notes]
2. Reference the test_patients.xlsx template from the templates dir
3. Modify the test_patients.xlsx file to include the patient data you want to verify (make sure to reference the correct payer code via pVerify and Stedi payer list)
4. Place the test_patients.xlsx in the data/input folder
5. Run pVerify
   1. Generate a token with the pVerify_generate_token.py script
   2. Update the pVERIFY_BEARER_TOKEN in the .env file with the new access token
   3. Run the pVerify_main.py script
6. Run Stedi
   1. Run the stedi_main.py script
7. Outputs will be in the data/output folder
