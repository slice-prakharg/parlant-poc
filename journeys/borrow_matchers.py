import parlant.sdk as p


async def match_user_has_credit_card(
    context: p.GuidelineMatchingContext, 
    guideline: p.Guideline
) -> p.GuidelineMatch:
    """Match if user is currently using credit card product."""
    profile_details_variable = await context.agent.find_variable(name="profile_data")
    assert profile_details_variable

    details = await profile_details_variable.get_value_for_customer(context.customer)
    assert details

    print("=" * 20)
    print(f"match_user_has_credit_card: {match_user_has_credit_card.__name__}")

    
    
    if details["user_current_product_type"] == "credit_card":
        return p.GuidelineMatch(
            id=guideline.id,
            matched=True,
            rationale="User is currently on credit card, so they can simply use their credit card for their money needs. Only one lending product can be used at a time by a user"
        )
    
    return p.GuidelineMatch(
        id=guideline.id,
        matched=False,
        rationale="User is not on credit card product"
    )


async def match_user_has_personal_loan(
    context: p.GuidelineMatchingContext, 
    guideline: p.Guideline
) -> p.GuidelineMatch:
    """Match if user is currently using personal loan product."""
    profile_details_variable = await context.agent.find_variable(name="profile_data")
    assert profile_details_variable

    details = await profile_details_variable.get_value_for_customer(context.customer)
    assert details

    print("=" * 20)
    print(f"match_user_has_personal_loan: {match_user_has_personal_loan.__name__}")

    if details["user_current_product_type"] == "personal_loan":
        return p.GuidelineMatch(
            id=guideline.id,
            matched=True,
            rationale="User is currently upgraded to personal loan from borrow, therefore no need to apply for borrow application"
        )

    return p.GuidelineMatch(
        id=guideline.id,
        matched=False,
        rationale="User is not on personal loan product"
    )


async def match_borrow_application_declined(
    context: p.GuidelineMatchingContext, 
    guideline: p.Guideline
) -> p.GuidelineMatch:
    """Match if user's borrow application was declined."""
    profile_details_variable = await context.agent.find_variable(name="profile_data")
    assert profile_details_variable

    details = await profile_details_variable.get_value_for_customer(context.customer)
    assert details

    print("=" * 20)
    print(f"match_borrow_application_declined: {match_borrow_application_declined.__name__}")

    if details["borrow_application_status"] == "declined" or details["borrow_profile_status"] == "declined":
        return p.GuidelineMatch(
            id=guideline.id,
            matched=True,
            rationale="At this moment, borrow is not available for user, but our eligibility criteria updates regularly, therefore the user should keep checking back later"
        )

    return p.GuidelineMatch(
        id=guideline.id,
        matched=False,
        rationale="User's borrow application is not declined"
    )


async def match_user_has_not_started_borrow_application(
    context: p.GuidelineMatchingContext, 
    guideline: p.Guideline
) -> p.GuidelineMatch:
    """Match if user has not yet started their borrow application."""
    profile_details_variable = await context.agent.find_variable(name="profile_data")
    assert profile_details_variable

    details = await profile_details_variable.get_value_for_customer(context.customer)
    assert details

    print("=" * 20)
    print(f"match_user_has_not_started_borrow_application: {match_user_has_not_started_borrow_application.__name__}")

    if details["user_current_product_type"] == "unassigned" and details["borrow_application_status"] is None:
        return p.GuidelineMatch(
            id=guideline.id,
            matched=True,
            rationale="User has not yet started his borrow application, therefore they must be prompted to start a new application from borrow section to start borrowing money"
        )

    return p.GuidelineMatch(
        id=guideline.id,
        matched=False,
        rationale="User has already started their borrow application"
    )

async def match_application_needs_correction(
    context: p.GuidelineMatchingContext, 
    guideline: p.Guideline
) -> p.GuidelineMatch:
    """Match if user's borrow application needs correction."""
    profile_details_variable = await context.agent.find_variable(name="profile_data")
    assert profile_details_variable

    details = await profile_details_variable.get_value_for_customer(context.customer)
    assert details

    print("=" * 20)
    print(f"match_application_needs_correction: {match_application_needs_correction.__name__}")

    if details["borrow_application_status"] in ("appStart", "appstart", "app_started"):
        return p.GuidelineMatch(
            id=guideline.id,
            matched=True,
            rationale="User's borrow application has been started, therefore they need to correct it"
        )

    return p.GuidelineMatch(
        id=guideline.id,
        matched=False,
        rationale="User's borrow application has not been started"
    )


async def match_application_started(
    context: p.GuidelineMatchingContext, 
    guideline: p.Guideline
) -> p.GuidelineMatch:
    """Match if user's borrow application has been started."""
    profile_details_variable = await context.agent.find_variable(name="profile_data")
    assert profile_details_variable

    details = await profile_details_variable.get_value_for_customer(context.customer)
    assert details

    print("=" * 20)
    print(f"match_application_started: {match_application_started.__name__}")

    if details["borrow_application_status"] == "started":
        return p.GuidelineMatch(
            id=guideline.id,
            matched=True,
            rationale="User's borrow application is only started"
        )

    return p.GuidelineMatch(
        id=guideline.id,
        matched=False,
        rationale="User's borrow application either has not started or is past the started state"
    )


async def match_application_submitted(
    context: p.GuidelineMatchingContext, 
    guideline: p.Guideline
) -> p.GuidelineMatch:
    """Match if user's borrow application has been submitted."""
    profile_details_variable = await context.agent.find_variable(name="profile_data")
    assert profile_details_variable

    details = await profile_details_variable.get_value_for_customer(context.customer)
    assert details

    print("=" * 20)
    print(f"match_application_submitted: {match_application_submitted.__name__}")

    if details["borrow_application_status"] == "submitted":
        return p.GuidelineMatch(
            id=guideline.id,
            matched=True,
            rationale="User's borrow application has been submitted"
        )

    return p.GuidelineMatch(
        id=guideline.id,
        matched=False,
        rationale="User's borrow application has not been submitted"
    )


async def match_application_kycdone(
    context: p.GuidelineMatchingContext, 
    guideline: p.Guideline
) -> p.GuidelineMatch:
    """Match if user's borrow application has been KYC done."""
    profile_details_variable = await context.agent.find_variable(name="profile_data")
    assert profile_details_variable

    details = await profile_details_variable.get_value_for_customer(context.customer)

    print("=" * 20)
    print(f"match_application_kycdone: {match_application_kycdone.__name__}")

    if details["borrow_application_status"] == "kycDone":
        return p.GuidelineMatch(
            id=guideline.id,
            matched=True,
            rationale="User's borrow application has been KYC done"
        )

    return p.GuidelineMatch(
        id=guideline.id,
        matched=False,
        rationale="User's borrow application has not been KYC done"
    )

async def match_application_already_approved(
    context: p.GuidelineMatchingContext, 
    guideline: p.Guideline
) -> p.GuidelineMatch:
    """Match if user's borrow application has been already approved."""
    profile_details_variable = await context.agent.find_variable(name="profile_data")
    assert profile_details_variable

    details = await profile_details_variable.get_value_for_customer(context.customer)
    assert details

    print("=" * 20)
    print(f"match_application_already_approved: {match_application_already_approved.__name__}")

    if details["borrow_application_status"] == "approved":
        return p.GuidelineMatch(
            id=guideline.id,
            matched=True,
            rationale="User's borrow application has been already approved"
        )

    return p.GuidelineMatch(
        id=guideline.id,
        matched=False,
        rationale="User's borrow application has not been approved yet"
    )


async def match_purchase_power_locked(
    context: p.GuidelineMatchingContext, 
    guideline: p.Guideline
) -> p.GuidelineMatch:
    """Match if user's purchase power is locked."""
    profile_details_variable = await context.agent.find_variable(name="profile_data")
    assert profile_details_variable
    
    details = await profile_details_variable.get_value_for_customer(context.customer)   
    assert details

    print("=" * 20)
    print(f"match_purchase_power_locked: {match_purchase_power_locked.__name__}")

    if details["is_purchase_power_locked"] == True:
        return p.GuidelineMatch(
            id=guideline.id,
            matched=True,
            rationale="User's purchase power is locked"
        )

    return p.GuidelineMatch(
        id=guideline.id,
        matched=False,
        rationale="User's purchase power is not locked"
    )


async def is_savings_account_onboarding_pending(
    context: p.GuidelineMatchingContext, 
    guideline: p.Guideline
) -> p.GuidelineMatch:
    """Match if user has onboarded their savings account."""
    profile_details_variable = await context.agent.find_variable(name="profile_data")
    assert profile_details_variable

    details = await profile_details_variable.get_value_for_customer(context.customer)
    assert details

    print("=" * 20)
    print(f"is_savings_account_onboarding_pending: {is_savings_account_onboarding_pending.__name__}")

    if details["is_savings_account_onboarded"] == False:
        return p.GuidelineMatch(
            id=guideline.id,
            matched=True,
            rationale="User has not yet onboarded their savings account"
        )

    return p.GuidelineMatch(
        id=guideline.id,
        matched=False,
        rationale="User has already onboarded their savings account"
    )