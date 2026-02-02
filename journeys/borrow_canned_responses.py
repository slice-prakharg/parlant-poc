import parlant.sdk as p


class BorrowCannedResponses:
    """Singleton container for all borrow-related canned responses.
    
    All canned responses are initialized when register_borrow_canned_responses() is called.
    """
    
    PAN_VERIFICATION_ISSUE_RESPONSE: p.CannedResponseId
    APPLICATION_NEEDS_CORRECTION_RESPONSE: p.CannedResponseId
    APPLICATION_STARTED_RESPONSE: p.CannedResponseId
    APPLICATION_SUBMITTED_RESPONSE: p.CannedResponseId
    APPLICATION_KYCDONE_RESPONSE: p.CannedResponseId
    APPLICATION_ALREADY_APPROVED_RESPONSE: p.CannedResponseId


# Singleton instance (exportable)
borrow_canned_responses = BorrowCannedResponses()


async def register_borrow_canned_responses(agent: p.Agent) -> None:
    """Register all borrow canned responses with the agent."""
    
    borrow_canned_responses.PAN_VERIFICATION_ISSUE_RESPONSE = await agent.create_canned_response(
        template="<b>PAN verification issue can happen for several reasons. A few reasons could be:</b>\n"
            "• Your PAN might already be linked to another slice account — try logging in with the same mobile number.\n"
            "• The PAN entered may have a small error — please double-check the 10-character format (e.g., ABCDE1234F).\n"
            "• If you've recently received a new PAN, it may take up to 7 days to become active in the official database — please try again later.\n"
            "• The PAN you entered might be different from the one linked to your slice Savings Account — please use the same PAN to keep things connected.\n\n"
            "If you're not facing any of these issues, please complete your application to start borrowing today. 🎉"
    )

    borrow_canned_responses.APPLICATION_NEEDS_CORRECTION_RESPONSE = await agent.create_canned_response(
        template="Your application could not be processed and we've sent it back to you for review — please check and resubmit after making the updates. Going through the onboarding again can help fix the issue."
    )

    borrow_canned_responses.APPLICATION_STARTED_RESPONSE = await agent.create_canned_response(
        template="It looks like your borrow application isn't complete yet. Complete it soon so you can start enjoying slice borrow "
    )

    borrow_canned_responses.APPLICATION_SUBMITTED_RESPONSE = await agent.create_canned_response(
        template="We've received your application! Our team is on it, and we're working to get you an update as quickly as possible. You can expect to hear from us within 48 hours- often even sooner 🎉"
    )

    borrow_canned_responses.APPLICATION_KYCDONE_RESPONSE = await agent.create_canned_response(
        template="We've received your application! Our team is on it, and we're working to get you an update as quickly as possible. You can expect to hear from us within 48 hours- often even sooner 🎉"
    )

    borrow_canned_responses.APPLICATION_ALREADY_APPROVED_RESPONSE = await agent.create_canned_response(
        template="Your application has already been approved! 🎉. If you are facing any other issues with borrowing money, let us know in more detail so we can help you further"
    )
