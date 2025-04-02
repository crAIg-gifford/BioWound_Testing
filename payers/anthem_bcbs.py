def anthem_bcbs_payment_responsibility(response):
    print("anthem_bcbs 222")

    if response['APIResponseCode'] == "1":
        return "Error"
    
    responsibility_details = {}
    DMESummary = response['DMESummary']

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