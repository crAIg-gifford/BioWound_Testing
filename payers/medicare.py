def pVerify_medicare_payment_responsibility(response):
    if response['APIResponseCode'] != "0":
        return "Error"
    responsibility_details = {}
    medicare_info = response['MedicareInfoSummary']
    hbpc_info = response['HBPC_Deductible_OOP_Summary']

    # Payer Name
    responsibility_details["PayerName"] = (
        response['PayerName'])

    # Plan Type
    responsibility_details["PlanType"] = (
        response['PlanCoverageSummary']['PolicyType'])

    # QMB Designation
    responsibility_details["QMB_Designation"] = medicare_info['QMBPolicyType']

    # Part B Deductible
    responsibility_details["Part_B_Deductible"] = (
            medicare_info['Part_B_Deductible']['Value'])

    # Part B Deductible Remaining
    responsibility_details["Part_B_Deductible_Remaining"] = (
            medicare_info['Part_B_Deductible_Remaining']['Value'])

    # Coinsurance
    responsibility_details["Coinsurance"] = (
            medicare_info['MedicareCoInsurance']['Value'])

    # OOP Max
    responsibility_details["OOP_Max"] = (
            hbpc_info['IndividualOOP_InNet'])

    # OOP Remaining
    responsibility_details["OOP_Remaining"] = (
            hbpc_info['IndividualOOPRemainingInNet'])

    return responsibility_details


def stedi_medicare_payment_responsibility(response):
    return "currently not implemented"
