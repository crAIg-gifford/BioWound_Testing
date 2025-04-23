def pVerify_general_payer_payment_responsibility(response):
    if response['APIResponseCode'] != "0":
        return "Error"
    if response['PlanCoverageSummary']['Status'] == "Inactive":
        responsibility_details = {
            "PayerName": response['PayerName'],
            "Status": "Plan is inactive"
        }
        return responsibility_details
    responsibility_details = {}
    hbpc_info = response['HBPC_Deductible_OOP_Summary']
    # DMESummary = response['DMESummary']

    # Payer Name
    responsibility_details["PayerName"] = (
            response['PayerName'])
    
    # Plan Type
    responsibility_details["PlanType"] = (
            response['PlanCoverageSummary']['PolicyType'])

    # In Network Coverage
    responsibility_details["isInNetworkCoverage"] = (
            response['IsProviderInNetwork'])

    # Individual Deductible
    responsibility_details["Deductible"] = (
            hbpc_info['IndividualDeductibleInNet'])

    # Individual Deductible Remaining
    responsibility_details["Deductible_Remaining"] = (
            hbpc_info['IndividualDeductibleRemainingInNet'])

    # Coinsurance - TODO: Add this to the response
    # coins_in_net = {x}.get('CoInsInNet')

    # Copay
    # Copay - TODO: Add this to the response

    # OOP Max
    responsibility_details["OOP_Max"] = (
            hbpc_info['IndividualOOP_InNet'])

    # OOP Remaining
    responsibility_details["OOP_Remaining"] = (
            hbpc_info['IndividualOOPRemainingInNet'])

    return responsibility_details


def stedi_general_payer_payment_responsibility(response):
    return "currently not implemented"