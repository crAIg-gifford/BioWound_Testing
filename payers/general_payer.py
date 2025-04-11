def pVerify_general_payer_payment_responsibility(type, response):
    print("pVerify_general_payer 222")
    if type == "Dental":
        return "Dental Parsing needed"
    if response['APIResponseCode'] == "1":
        return "Error"
    if response['PlanCoverageSummary']['Status'] == "Inactive":
        responsibility_details = {
            "PayerName": response['PayerName'],
            "Status": "Plan is inactive"
        }
        return responsibility_details
    responsibility_details = {}
    DMESummary = response['DMESummary']

    # Payer Name
    responsibility_details["PayerName"] = (
            response['PayerName'])
    
    # Plan Type
    responsibility_details["PlanType"] = (
            response['PlanCoverageSummary']['PolicyType'])

    # In Network Coverage
    responsibility_details["isInNetworkCoverage"] = (
            DMESummary['ServiceCoveredInNet'])

    # Out of Network Coverage
    responsibility_details["isOutNetworkCoverage"] = (
            DMESummary['ServiceCoveredOutNet'])

    # Deductible
    responsibility_details["Deductible"] = (
            DMESummary['IndividualDeductibleInNet'])

    # Deductible Remaining
    responsibility_details["Deductible_Remaining"] = (
            DMESummary['IndividualDeductibleRemainingInNet'])

    # Coinsurance
    coins_in_net = DMESummary.get('CoInsInNet')
    if coins_in_net and coins_in_net.get('Value'):
        responsibility_details["Coinsurance"] = coins_in_net['Value']
    else:
        responsibility_details["Coinsurance"] = "N/A"

    # Copay
    copay_in_net = DMESummary.get('CoPayInNet')
    if copay_in_net and copay_in_net.get('Value'):
        responsibility_details["Copay"] = copay_in_net['Value']
    else:
        responsibility_details["Copay"] = "N/A"

    # OOP Max
    responsibility_details["OOP_Max"] = (
            DMESummary['IndividualOOP_InNet'])

    # OOP Remaining
    responsibility_details["OOP_Remaining"] = (
            DMESummary['IndividualOOPRemainingInNet'])

    return responsibility_details


def stedi_general_payer_payment_responsibility(response):
    return response
#     print("stedi_general_payer 222")
    
#     if response["errors"] != []:
#         return "Error"
#     responsibility_details = {}
#     try:

#         # Find dict associated with Durable Medical Equipment Purchase
#         dme_dict = next(
#             (item for item in response['benefitsInformation']
#              if "Durable Medical Equipment Purchase" in item['serviceTypes']),
#             None
#         )

#         # Payer Name
#         responsibility_details["PayerName"] = (
#                 response['payer']['name'])

#         # In Network Coverage
#         responsibility_details["isInNetworkCoverage"] = (
#                 dme_dict['inPlanNetworkIndicator'])

#         #     # Out of Network Coverage
#         #     responsibility_details["isOutNetworkCoverage"] = (
#         #             response['ServiceCoveredOutNet'])

#         #     # Deductible
#         #     responsibility_details["Deductible"] = (
#         #             response['IndividualDeductibleInNet'])

#         #     # Deductible Remaining
#         #     responsibility_details["Deductible_Remaining"] = (
#         #             response['IndividualDeductibleRemainingInNet'])

#         # Coinsurance
#         coins_in_net = dme_dict.get('benefitPercent')
#         responsibility_details["Coinsurance"] = coins_in_net
#         #     coins_in_net = response.get('CoInsInNet')
#         #     if coins_in_net and coins_in_net.get('Value'):
#         #         responsibility_details["Coinsurance"] = coins_in_net['Value']
#         #     else:
#         #         responsibility_details["Coinsurance"] = "N/A"

#         #     # Copay
#         #     copay_in_net = response.get('CoPayInNet')
#         #     if copay_in_net and copay_in_net.get('Value'):
#         #         responsibility_details["Copay"] = copay_in_net['Value']
#         #     else:
#         #         responsibility_details["Copay"] = "N/A"

#         #     # OOP Max
#         #     responsibility_details["OOP_Max"] = (
#         #             response['IndividualOOP_InNet'])

#         #     # OOP Remaining
#         #     responsibility_details["OOP_Remaining"] = (
#         #             response['IndividualOOPRemainingInNet'])

#         return responsibility_details
#     except Exception as e:
#         print(f"Error: {e}")
#         return "Error"
