import currency
multisig_data = Hash()
metadata = Hash()
metadata_proposal = Hash()

@construct
def seed():
    multisig_data['addresses'] = ['d701fe13fc525264161793a4fc2a16363e5c6ff0080dad25ae0f1041bb967c1b','7e01b7c9322fd246ccd1c589ca6d690e9e17a50d0f35c0dbcf6acd75cdcef0a5','00b82d83ac279bbd42b538afec4bc662d8b99f799474b6359888c6476752fd2a']

    metadata['operator'] = ctx.caller
    metadata['test'] = 10

@export
def propose_metadata(key: str, new_value: Any):
    assert ctx.caller == metadata['operator'], "only operator can propose changes"
    multisig_addresses = multisig_data['addresses']
    proposal_approvals = {}
    for x in multisig_addresses:
        proposal_approvals.update({x : 0 })
    multisig_data['addresses', key] = proposal_approvals
    metadata_proposal[key] = new_value

@export
def approve_proposal(key: str, enable:bool):
    proposal_approvals = multisig_data['addresses', key]
    call_address = ctx.caller
    assert call_address in proposal_approvals.keys(), "You are not approved to do this."
    proposal_approvals[call_address] = int(enable)
    multisig_data['addresses', key] = proposal_approvals

@export
def implement_proposal(key: str):
    assert ctx.caller == metadata['operator'], 'Only operator can implement approved proposals'
    proposal_approvals = multisig_data['addresses', key]
    approval_check = sum(proposal_approvals.values())
    assert approval_check >= 2, "This metadata proposal is not aproved."
    metadata[key] = metadata_proposal[key]
