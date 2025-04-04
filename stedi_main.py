import requests
import os
import json
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
from requests.exceptions import RequestException
from payers import general_payer

# Load environment variables
load_dotenv()

STEDI_API_BASE_URL = os.getenv("STEDI_API_BASE_URL")
CONTENT_TYPE = os.getenv("CONTENT_TYPE")
STEDI_API_KEY = os.getenv("STEDI_API_KEY")
HEADERS = {
    "Authorization": f"{STEDI_API_KEY}",
    "Content-Type": f"{CONTENT_TYPE}",
}


def make_request(method, payload):
    """
    Generic function to handle GET and POST requests.
    """
    url = f"{STEDI_API_BASE_URL}"
    print(f"URL: {url}")
    try:
        if method == "GET":
            response = requests.get(url, headers=HEADERS)
        elif method == "POST":
            response = requests.post(
                url,
                headers=HEADERS,
                data=json.dumps(payload)
            )
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.json()}
        
    except RequestException as error:
        return {"error": str(error)}


def get_data(endpoint):
    return make_request("GET", endpoint)


def post_data(payload):
    return make_request("POST", payload)


def format_date(value):
    return value.strftime('%Y%m%d') if not pd.isna(value) else None


def export_response(
    response, row_index, eligibility_type, payer_name, subscriber_id
):
    """
    Export API response to a JSON file in the data/output directory.
    """
    if response.get("error"):
        print(f"Error: {response.get('error')}")
        return
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_payer_name = "".join(
        c for c in payer_name if c.isalnum() or c in (' ', '-', '_')
    ).strip()
    filename = os.path.join(
        'data', 'output',
        f"stedi_eligibility_response_{eligibility_type}_"
        f"{safe_payer_name}_{subscriber_id}_"
        f"{row_index}_{timestamp}.json"
    )
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w') as f:
        json.dump(response, f, indent=4)
    print(f"Response exported to: {filename}")


def process_patient_data(row):
    """
    Process individual patient row data into required payload format.
    """

    payload = {
        # "payerCode": str(row['Payer ID']),
        # "payerName": str(row['Payer Name']),
        "controlNumber": "123321",
        "tradingPartnerServiceId": str(row['Payer ID Stedi']),
        "provider": {
            "organizationName": str(row['Provider']),
            "npi": str(row['NPI'])
        },
        "subscriber": {
            "firstName": str(row['Subscriber First']),
            "lastName": str(row['Subscriber Last']),
            "dateOfBirth": format_date(row['Subscriber DOB']),
            "memberId": str(row['Subscriber ID'])
        },
        "encounter": {
            "serviceTypeCodes": ["12"],
            "dateOfService": "20250402"
        }
    }

    # Add dependent info if the patient is different from subscriber
    if not pd.isna(row.get('Patient First')):
        payload["dependent"] = {
            "firstName": str(row['Patient First']),
            "lastName": str(row['Patient Last']),
            "dob": format_date(row['Patient DOB'])
        }
    return payload

# def extract_payment_responsibility_info(response):
#     """
#     Extract payment responsibility information from the API response.
#     """


def main():
    df = pd.read_excel(
        os.path.join('data', 'input', 'test_patients.xlsx'),
        dtype={"Payer ID": str}
    )

    my_results = []
    ivr_results = {}
    # Process and submit data
    for index, row in df.iterrows():
        print(
            f"Processing row {index}: {row['Type']}, {row['Payer Name']}, "
            f"{row['Subscriber ID']}"
        )
        payload = process_patient_data(row)
        print("\nProcessed Patient Data:")
        print(json.dumps(payload, indent=4))
        # API call
        response = post_data(payload)
        print(response)
        # if response.get("error"):
        #     my_results.append("Error")
        #     continue
        # else:
        #     my_results.append("Success")
        export_response(
            response, 
            index, 
            str(row['Type']),
            str(row['Payer Name']),
            str(row['Subscriber ID'])
        )
        # if str(row['Payer ID']).upper() == "00007":
        #     payment_responsibility_info = (
        #             medicare.medicare_payment_responsibility(response))
        #     print("\nPayment Responsibility Info:")
        #     print(json.dumps(payment_responsibility_info, indent=4))
        # elif str(row['Payer ID']).upper() == "000931":
        #     payment_responsibility_info = (
        #             anthem_bcbs.anthem_bcbs_payment_responsibility(response))
        #     print("\nPayment Responsibility Info:")
        #     print(json.dumps(payment_responsibility_info, indent=4))
        # else:
        payment_responsibility_info = (
                general_payer.stedi_general_payer_payment_responsibility(
                    response))
        print("\nPayment Responsibility Info:")
        print(json.dumps(payment_responsibility_info, indent=4))
        print("Not Medicare")

        # Create subscriber key
        sub_key = f"{row['Subscriber First']} {row['Subscriber Last']}"

        # Determine if the subscriber is already in the ivr_results dictionary
        if not ivr_results.get(sub_key):
            ivr_results[sub_key] = []

        # Add the payment responsibility info to the subscriber's list
        ivr_results[sub_key].append(payment_responsibility_info)

    print(f"Results: {my_results}")
    # Export the ivr_results to a JSON file
    with open(f'data/output/stedi_ivr_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json', 'w') as f:
        json.dump(ivr_results, f, indent=4)


if __name__ == "__main__":
    main()
