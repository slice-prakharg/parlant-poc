import parlant.sdk as p


class BorrowObservations:
    """Singleton container for all borrow-related observations.
    
    All observations are initialized when register_borrow_journey_selection_conditions() is called.
    """
    
    # Application issues observations
    BORROW_APPLICATION_ISSUE: p.Guideline
    APPLICATION_STUCK_KYC_PAN: p.Guideline
    
    # Profile issues observations
    REMOVE_ON_HOLD_REQUESTED: p.Guideline
    DELETED_BORROW_PROFILE: p.Guideline
    BORROW_PROFILE_ISSUES: p.Guideline
    
    # Purchase power issues observations
    INCREASE_PURCHASE_POWER_REQUESTED: p.Guideline
    KNOW_MY_PURCHASE_POWER: p.Guideline
    WHY_LOW_PP: p.Guideline


# Singleton instance (exportable)
borrow_observations = BorrowObservations()


async def register_borrow_journey_selection_conditions(agent: p.Agent) -> None:
    """Register all borrow journey observations with the agent."""
    
    # Application issues
    borrow_observations.BORROW_APPLICATION_ISSUE = await agent.create_observation(
        condition="user says they are facing issue with their borrow application onboarding",
        description="this observation is around user's query for borrow application and not borrow profile. User can mention that their borrow application is stuck, not getting approved, got declined, etc",
        criticality=p.Criticality.HIGH
    )

    borrow_observations.APPLICATION_STUCK_KYC_PAN = await agent.create_observation(
        condition="user says their borrow application is stuck at kyc/pan verification",
        description="user's application is stuck at kyc/pan verification"
    )

    # Profile issues
    borrow_observations.REMOVE_ON_HOLD_REQUESTED = await agent.create_observation(
        condition="user wants to remove their borrow profile from on hold",
        description="on hold can keep user from borrowing money. When profile is on hold, user may wish to remove the hold status and make his borrow profile active again",
        criticality=p.Criticality.HIGH
    )

    borrow_observations.DELETED_BORROW_PROFILE = await agent.create_observation(
        condition="user wants to restore their deleted borrow profile",
        description="user may have deleted their borrow profile due to some reason. They may wish to restore the profile and continue using it",
    )

    borrow_observations.BORROW_PROFILE_ISSUES = await agent.create_observation(
        condition="user says they are facing issues with their borrow profile",
        description="user may be facing issues with their borrow profile (NOT APPLICATION ISSUES), such as profile on hold, deleted, declined.",
        criticality=p.Criticality.HIGH
    )

    # Purchase power issues
    borrow_observations.INCREASE_PURCHASE_POWER_REQUESTED = await agent.create_observation(
        condition="user wants to increase their purchase power",
        description="user may want to increase their purchase power to borrow more money",
        criticality=p.Criticality.HIGH
    )

    borrow_observations.KNOW_MY_PURCHASE_POWER = await agent.create_observation(
        condition="user wants to know their purchase power",
        description="user may want to know their purchase power to borrow more money",
        criticality=p.Criticality.HIGH
    )

    borrow_observations.WHY_LOW_PP = await agent.create_observation(
        condition="user wants to know why their purchase power is low",
        description="user may want to know why their purchase power is low to borrow more money",
        criticality=p.Criticality.HIGH  
    )

    borrow_observations.LOCK_ON_PP_ISSUE = await agent.create_observation(
        condition="user wants to remove the lock on their purchase power",
        description="purchase power gets locked when profile is put on hold, and hold can be lifted by clearing the pending outstanding amount. The hold can also happen due to internal risk assessment or account closure request in progress or completed",
        criticality=p.Criticality.HIGH
    )


