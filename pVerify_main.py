import requests
import os
import json
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
from requests.exceptions import RequestException
from payers import medicare, general_payer

# Load environment variables
load_dotenv()

API_BASE_URL = os.getenv("pVERIFY_API_BASE_URL")
BEARER_TOKEN = os.getenv("pVERIFY_BEARER_TOKEN")
CLIENT_ID = os.getenv("pVERIFY_CLIENT_ID")
CONTENT_TYPE = os.getenv("pVERIFY_CONTENT_TYPE")

HEADERS = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "Client-API-Id": f"{CLIENT_ID}",
    "Content-Type": f"{CONTENT_TYPE}",
}


def make_request(method, payload):
    """
    Generic function to handle GET and POST requests.
    """
    endpoint = "EligibilitySummary"
    url = f"{API_BASE_URL}{endpoint}"
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
    return value.strftime('%m/%d/%Y') if not pd.isna(value) else None


def export_response(
    response, row_index, patient_name,
    payer_name, subscriber_id
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
        f"pVerify_eligibility_response_{patient_name}_"
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
        "payerCode": str(row['Payer ID pVerify']),
        "payerName": str(row['Payer Name']),
        "provider": {
            "lastName": str(row['Provider']),
            "npi": str(int(row['NPI']))
        },
        "subscriber": {
            "firstName": str(row['Subscriber First']),
            "lastName": str(row['Subscriber Last']),
            "dob": format_date(row['Subscriber DOB']),
            "memberID": str(row['Subscriber ID'])
        },
        "isSubscriberPatient": "True",
        "doS_StartDate": f"{datetime.now().strftime('%m/%d/%Y')}",
        "doS_EndDate": f"{datetime.now().strftime('%m/%d/%Y')}",
        "PracticeTypeCode": "22",   # 3 = DME; 22 = Surgical-Office
        "Location": "TA",
        "IncludeHtmlResponse": True
    }
    return payload


def main():
    df = pd.read_excel(
        os.path.join('data', 'input', 'test_patients.xlsx'),
        dtype={"Payer ID pVerify": str}
    )

    my_results = []
    ivr_results = {}
    # Process and submit data
    for index, row in df.iterrows():
        print(
            f"Processing row {index}: {row['Payer Name']}, "
            f"{row['Subscriber ID']}"
        )
        patient_name = f"{row['Subscriber First']} {row['Subscriber Last']}"
        payload = process_patient_data(row)
        print("\nProcessed Patient Data:")
        print(json.dumps(payload, indent=4))
        # API call
        response = post_data(payload)
        if response.get("error"):
            my_results.append("Error")
            continue
        else:
            my_results.append("Success")
        export_response(
            response,
            index,
            patient_name,
            str(row['Payer Name']),
            str(row['Subscriber ID'])
        )
        if str(row['Payer ID pVerify']).upper() == "00007":
            payment_responsibility_info = (
                    medicare.pVerify_medicare_payment_responsibility(response))
            print("\nPayment Responsibility Info:")
            print(json.dumps(payment_responsibility_info, indent=4))
        else:
            payment_responsibility_info = (
                    general_payer.pVerify_general_payer_payment_responsibility(
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
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f'data/output/pVerify_ivr_results_{timestamp}.json', 'w') as f:
        json.dump(ivr_results, f, indent=4)


if __name__ == "__main__":
    main()
