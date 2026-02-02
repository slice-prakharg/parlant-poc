import parlant.sdk as p
from journey_conditions import borrow_observations, bank_linking_issues_observations
from journeys.borrow_matchers import * # type: ignore

# only checking this journey for now

async def on_guideline_match(ctx: p.EngineContext, match: p.GuidelineMatch) -> None:
    print(f"on_guideline_match: {match.id}, rationale: {match.rationale}, matched: {match.matched}")

async def on_journey_state_match(ctx: p.EngineContext, match: p.JourneyStateMatch) -> None:
    print(f"on_journey_state_match: {match.state_id}, {match.transition_id}, rationale: {match.rationale}, matched: {match.matched}")

async def create_journey_issues_with_borrow_application(agent: p.Agent) -> p.Journey:
    application_issues_journey: p.Journey = await agent.create_journey(
        title="borrow application issues",
        description="journey to handle user's issues with their borrow application.",
        conditions=[
            borrow_observations.BORROW_APPLICATION_ISSUE,
            borrow_observations.APPLICATION_STUCK_KYC_PAN,
        ]
    )

    guideline_is_cc_user = await application_issues_journey.create_guideline(
        matcher=match_user_has_credit_card,
        condition="",
        description="this guideline is used to disqualify user from borrow application issues query if they are currently using credit card product",
        action="Inform user that they are currently upgraded to slice Credit Card, therefore borrow application related should no longer be a concern for them. They can simply use their credit card for their money needs.",
        on_match=on_guideline_match
    )

    guideline_is_personal_loan_user = await application_issues_journey.create_guideline(
        matcher=match_user_has_personal_loan,
        condition="",
        description="this guideline is used to disqualify user from borrow application issues query if they are currently using personal loan product",
        action="Inform user that they are currently upgraded to slice Personal Loan, therefore borrow application related issues should no longer be a concern for them. Thank them for being a part of slice and encourage them to continue using slice products.",
        on_match=on_guideline_match
    )

    observation_is_savings_account_onboarding_pending = await application_issues_journey.create_guideline(
        matcher=is_savings_account_onboarding_pending,
        condition="",
        description="informs whether user's savings account onboarding is still not completed",
        action="Inform user's that they can explore our digital savings account and explain the benefits of it like high interest rate, easy to use, etc",
        on_match=on_guideline_match
    )

    guideline_is_application_declined = await application_issues_journey.create_guideline(
        matcher=match_borrow_application_declined,
        condition="",
        description="this guideline is used to disqualify user from borrow application issues query if their borrow application has been declined",
        action="Inform user that we cannot provide them borrow at the moment just yet but our evaluation criteria updates regularly, therefore they can check back later",
        on_match=on_guideline_match
    )

    await guideline_is_application_declined.entail(observation_is_savings_account_onboarding_pending)

    guideline_application_needs_correction = await application_issues_journey.create_guideline(
        matcher=match_application_needs_correction,
        condition="",
        description="this guideline is used to inform user that their borrow application needs correction",
        action="Your application could not be processed and we’ve sent it back to you for review — please check and resubmit after making the updates. Going through the onboarding again can help fix the issue.",
        composition_mode=p.CompositionMode.STRICT,
        on_match=on_guideline_match
    )

    guideline_user_frutrated_app_needs_correction = await application_issues_journey.create_guideline(
        condition="user shows frustration and mentions they have tried all steps multiple times but application is still not getting approved",
        action="Apologize to user and inform them that you will transfer their query to our dedicated support team who will help them with their application issue",
        composition_mode=p.CompositionMode.FLUID,
        on_match=on_guideline_match
    )

    await guideline_user_frutrated_app_needs_correction.depend_on(guideline_application_needs_correction)


    guideline_application_started = await application_issues_journey.create_guideline(
        matcher=match_application_started,
        condition="",
        description="lets us know if user's application is still in the started state",
        action="It looks like your borrow application isn't complete yet. Complete it soon so you can start enjoying slice borrow ",
        composition_mode=p.CompositionMode.STRICT,
        on_match=on_guideline_match

    )

    guideline_user_asks_why_unable_to_complete_application = await application_issues_journey.create_guideline(
        condition="user asks why they are unable to complete their application",
        action="Apologize to user and inform them that you will transfer their query to our dedicated support team who will help them with their application issue",
        composition_mode=p.CompositionMode.FLUID,
        on_match=on_guideline_match
    )

    await guideline_user_asks_why_unable_to_complete_application.depend_on(guideline_application_started)

    guideline_kyc_pan_info = await application_issues_journey.create_guideline(
        condition="user mentions issue with PAN verification",
        action=(
            "You’re unable to borrow right now because your PAN verification is pending. This can happen for a few reasons:\n"
            "• Your PAN might already be linked to another slice account — try logging in with the same mobile number.\n"
            "• The PAN entered may have a small error — please double-check the 10-character format (e.g., ABCDE1234F).\n"
            "• If you’ve recently received a new PAN, it may take up to 7 days to become active in the official database — please try again later.\n"
            "• The PAN you entered might be different from the one linked to your slice Savings Account — please use the same PAN to keep things connected.\n\n"
            "If you’re not facing any of these issues, please complete your application to start borrowing today. 🎉"
        ),

        composition_mode=p.CompositionMode.STRICT,
        on_match=on_guideline_match

    )

    guideline_kyc_adhar_info = await application_issues_journey.create_guideline(
        condition="user mentions issue with Aadhar verification",
        action="Apologize to user and inform them that you will transfer their query to our dedicated support team who will help them with their Aadhar verification issue",
        composition_mode=p.CompositionMode.FLUID,
        on_match=on_guideline_match
    )

    await guideline_kyc_pan_info.depend_on(borrow_observations.APPLICATION_STUCK_KYC_PAN)
    await guideline_kyc_adhar_info.depend_on(borrow_observations.APPLICATION_STUCK_KYC_PAN)

    guideline_application_submitted = await application_issues_journey.create_guideline(
        matcher=match_application_submitted,
        condition="",
        description="inform if user's application has been submitted",
        action="We've received your application! Our team is on it, and we're working to get you an update as quickly as possible. You can expect to hear from us within 48 hours- often even sooner 🎉",
        composition_mode=p.CompositionMode.STRICT,
        on_match=on_guideline_match

    )

    guideline_application_kycdone = await application_issues_journey.create_guideline(
        condition="",
        matcher=match_application_kycdone,
        action="We've received your application! Our team is on it, and we're working to get you an update as quickly as possible. You can expect to hear from us within 48 hours- often even sooner 🎉",
        composition_mode=p.CompositionMode.STRICT,
        on_match=on_guideline_match
    )

    guideline_application_already_approved = await application_issues_journey.create_guideline(
        condition="",
        matcher=match_application_already_approved,
        action="Your application has already been approved! 🎉. If you are facing any other issues with borrowing money, let us know in more detail so we can help you further",
        composition_mode=p.CompositionMode.STRICT,
        on_match=on_guideline_match
    )
    

    await guideline_is_cc_user.prioritize_over(guideline_application_already_approved)
    await guideline_is_cc_user.prioritize_over(guideline_application_kycdone)
    await guideline_is_cc_user.prioritize_over(guideline_application_submitted)
    await guideline_is_cc_user.prioritize_over(guideline_application_started)
    await guideline_is_cc_user.prioritize_over(guideline_kyc_pan_info)
    await guideline_is_cc_user.prioritize_over(guideline_kyc_adhar_info)
    await guideline_is_cc_user.prioritize_over(guideline_application_needs_correction)
    await guideline_is_cc_user.prioritize_over(guideline_user_frutrated_app_needs_correction)
    await guideline_is_cc_user.prioritize_over(guideline_user_asks_why_unable_to_complete_application)

    await guideline_is_personal_loan_user.prioritize_over(guideline_application_already_approved)
    await guideline_is_personal_loan_user.prioritize_over(guideline_application_kycdone)
    await guideline_is_personal_loan_user.prioritize_over(guideline_application_submitted)
    await guideline_is_personal_loan_user.prioritize_over(guideline_application_started)
    await guideline_is_personal_loan_user.prioritize_over(guideline_kyc_pan_info)
    await guideline_is_personal_loan_user.prioritize_over(guideline_kyc_adhar_info)
    await guideline_is_personal_loan_user.prioritize_over(guideline_application_needs_correction)
    await guideline_is_personal_loan_user.prioritize_over(guideline_user_frutrated_app_needs_correction)
    await guideline_is_personal_loan_user.prioritize_over(guideline_user_asks_why_unable_to_complete_application)

    return application_issues_journey

# async def create_journey_bank_linking_issues(agent: p.Agent) -> p.Journey:
#     bank_linking_issues_journey: p.Journey = await agent.create_journey(
#         title="bank linking issues",
#         description="journey to handle user's issues with their bank linking.",
#         conditions=[
#             bank_linking_issues_observations.BANK_LINKING_ISSUES_GENERAL,
#         ]
#     )

#     penny_drop_failure = await bank_linking_issues_journey.create_guideline(
#         condition="user says explicitly they are facing penny drop failure",
#         action=(
#             "It looks like the ₹1 penny drop transaction didn't go through. This can happen due to a couple of reasons:\n\n"
#             "• Insufficient balance — Please ensure there's enough balance in your account to complete the transaction.\n"
#             "• Transaction declined by bank — Sometimes banks temporarily decline these small verification transactions, which can resolve itself.\n\n"
#             "Here's what you can do:\n"
#             "• Check your account balance and add funds if needed\n"
#             "• Try the penny drop verification again after some time\n"

#             "If you continue to experience issues, feel free to reach out—we're here to help!"
#         ),
#         composition_mode=p.CompositionMode.STRICT
#     )

#     name_mismatch_error = await bank_linking_issues_journey.create_guideline(
#         condition="user says explicitly they are facing name mismatch error ",
#         action="Apologize to user and inform them that you will transfer their query to our dedicated support team who will help them with their name mismatch error issue",
#         composition_mode=p.CompositionMode.FLUID
#     )

#     return bank_linking_issues_journey


@p.tool
async def call_test_tool(context: p.ToolContext) -> p.ToolResult:
    return p.ToolResult(
        data={
            "weather": "sunny"
        }
    )


async def test_journey(agent: p.Agent) -> p.Journey:
    test_journey: p.Journey = await agent.create_journey(
        title="test journey",
        description="journey to test the journey creation and execution.",
        conditions=[
            "user wants to know about the weather"
        ]
    )
    t1 = await test_journey.initial_state.transition_to(
        tool_state=call_test_tool,
        tool_instruction="gets the weather of the user's location",

    )

    fork =  await t1.target.fork()

    f1 = await fork.target.transition_to(
        condition="weather is sunny",
        chat_state="inform the user that the weather is sunny",
        on_match=on_journey_state_match
    )

    f2 = await fork.target.transition_to(
        condition="weather is cloudy",
        chat_state="inform the user that the weather is cloudy",
        on_match=on_journey_state_match
    )
    

    return test_journey

# async def create_journey_purchase_power_issues(agent: p.Agent) -> p.Journey:
    purchase_power_issues_journey: p.Journey = await agent.create_journey(
        title="purchase power issues",
        description="journey to handle user's issues with their purchase power.",
        conditions=[
            borrow_observations.INCREASE_PURCHASE_POWER_REQUESTED,
            borrow_observations.KNOW_MY_PURCHASE_POWER,
            borrow_observations.WHY_LOW_PP,
            borrow_observations.LOCK_ON_PP_ISSUE,
        ]
    )

    is_cc_user = await purchase_power_issues_journey.create_guideline(
        matcher=match_user_has_credit_card,
        condition="",
        description="this guideline is used to disqualify user from purchase power issues query if they are currently using credit card product",
        action="Inform user that they are currently upgraded to slice Credit Card, therefore purchase power is not applicable to them. They can simply use their credit card for their money needs.",
        composition_mode=p.CompositionMode.FLUID
    )

    is_personal_loan_user = await purchase_power_issues_journey.create_guideline(
        matcher=match_user_has_personal_loan,
        condition="",
        description="this guideline is used to disqualify user from purchase power issues query if they are currently using personal loan product", 
        criticality=p.Criticality.HIGH,
        action="Inform user that they are currently upgraded to slice Personal Loan, therefore purchase power is not applicable to them. If they wish to know more about personal loan they can let us know.",
        composition_mode=p.CompositionMode.FLUID
    )

    declined_user = await purchase_power_issues_journey.create_guideline(
        matcher=match_borrow_application_declined,
        condition="",
        description="this guideline is used to disqualify user from purchase power issues query if their borrow application has been declined",
        criticality=p.Criticality.HIGH,
        action="Inform user that we cannot provide them borrow at the moment just yet but our evaluation criteria updates regularly, therefore they can check back later",
        composition_mode=p.CompositionMode.FLUID
    )

    know_my_pp = await purchase_power_issues_journey.create_guideline(
        condition="user wants to know their purchase power",
        description="this guideline is used to inform user about their purchase power",
        action="inform the current purchase power of the user from 'profile_data' variable",
    )
    await know_my_pp.depends_on(borrow_observations.KNOW_MY_PURCHASE_POWER)

    why_low_pp = await purchase_power_issues_journey.create_guideline(
        condition="user wants to know why their purchase power is low",
        description="this guideline is used to inform user about the reasons why their purchase power is low",
        action="purchase power is internally decided based on risk assessment and is re evaluated after every repayment, therefore if there is any outstanding balance in 'profile_details', then the same should be cleared",
        composition_mode=p.CompositionMode.FLUID
    )

    observation_pp_locked = await purchase_power_issues_journey.create_guideline(
        matcher=match_purchase_power_locked,
    )


    await why_low_pp.depends_on(borrow_observations.WHY_LOW_PP)

    await is_cc_user.prioritize_over(declined_user)
    await is_personal_loan_user.prioritize_over(declined_user)
    await is_cc_user.prioritize_over(know_my_pp)
    await is_personal_loan_user.prioritize_over(know_my_pp)

    return purchase_power_issues_journey