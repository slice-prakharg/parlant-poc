import parlant.sdk as p

class BankLinkingIssuesObservations:
    """Singleton container for all bank linking issues observations.
    
    All observations are initialized when register_bank_linking_issues_journey_selection_conditions() is called.
    """
    
    BANK_LINKING_ISSUES_GENERAL: p.Guideline

bank_linking_issues_observations = BankLinkingIssuesObservations()


async def register_bank_linking_issues_journey_selection_conditions(agent: p.Agent) -> None:
    """Register all bank linking issues observations with the agent."""
    bank_linking_issues_observations.BANK_LINKING_ISSUES_GENERAL = await agent.create_observation(
        condition="user says they are facing issues linking their bank account",
            description="user may be facing issues linking their bank account, such as penny drop failure, name mismatch error, etc",
            criticality=p.Criticality.HIGH
    )
