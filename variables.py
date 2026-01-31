import parlant.sdk as p

@p.tool
async def get_profile_data(context: p.ToolContext) -> p.ToolResult:
    print("@@@@"*10)
    print(f"setting profile data for user {context.customer_id}")
    data = {
        "data_successfully_fetched_from_api": True,
        "borrow_application_status": "approved",
        "borrow_profile_status": "active",
        "borrow_purchase_power_in_rupees": 1000,
        "pending_outstanding_amount_to_repay_in_rupees": 0,
        "is_savings_account_onboarded": True,
        "user_current_product_type": "borrow",
        "is_purchase_power_locked": False,
    }
    return p.ToolResult(data=data)

async def create_and_register_variables(agent: p.Agent) -> None:
    print("Creating and registering variables")

    await agent.create_variable(name="profile_data", description="contains information about user's borrow profile, borrow purchase power, borrow application, and savings account onboarding status and product type", tool=get_profile_data, freshness_rules="*/15 * * * *")

    print("Profile data variable created")


