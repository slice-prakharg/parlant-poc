import parlant.sdk as p

async def register_glossary_terms(agent: p.Agent) -> list[p.Term]:
    terms = []
    
    print("Registering glossary terms")
    
    print("Creating Borrow Application term...")
    BORROW_APPLICATION = await agent.create_term(
        name="Borrow Application",
        description="It is the application that user completes to get his borrow profile created after which they can borrow money from slice into their linked bank account",
        synonyms=["borrow application", "borrow onboarding application", "borrow profile application"],
    )
    terms.append(BORROW_APPLICATION)
    print("✅ Borrow application term created")

    print("Creating Borrow Profile term...")
    BORROW_PROFILE = await agent.create_term(
        name="Borrow Profile",
        description="It is the profile that user gets created after completing the borrow application. It allows them to see their borrow purchase power, pending outstanding amount to repay, and other details. REMEMBER: application issues should not be inferred as borrow profile issues and vice versa. Profile operates independently after application is approved/declined",
        synonyms=["borrow profile", "borrow account"]
    )
    terms.append(BORROW_PROFILE)
    print("✅ Borrow profile term created")

    print("Creating Purchase Power term...")
    PURCHASE_POWER = await agent.create_term(
        name="Purchase Power",
        description="It is the amount of money UP TO WHICH the user can borrow from slice into their linked bank account",
        synonyms=["purchase power", "borrow purchase power", "pp"]
    )
    terms.append(PURCHASE_POWER)
    print("✅ Purchase power term created")

    print("Creating Outstanding Amount term...")
    OUTSTANDING_AMOUNT = await agent.create_term(
        name="Outstanding Amount",
        description="It is the amount of money that user owes to slice after borrowing money from slice into their linked bank account. contains components such as principal, interest, late fees, etc.",
        synonyms=["outstanding amount", "outstanding balance", "outstanding loan amount", "foreclosure amount"]
    )
    terms.append(OUTSTANDING_AMOUNT)
    print("✅ Outstanding amount term created")

    print("Creating Product Type term...")
    PRODUCT_TYPE = await agent.create_term(
        name="Product Type",
        description="it is a contruct of slice's lending products only (i.e. borrow, credit card and personal loan). It can be one of the following: borrow, credit card, personal loan, unassigned. unassinged means user has not completed onboarding on any of the lending products (either application not started, or not completed or declined). This is an internal construct and is not visible to the user. Basis this variable, we internally decide the screen and flow for user on the lending page. \n REMEMBER:: product_type borrow does not guarentee that borrow is available for user, as the availability of borrow is dependent on other factors that are decided internally such as user's credit score, income, etc, risk score, profile status, etc.",
        synonyms=["product type", "product", "product category"]
    )
    terms.append(PRODUCT_TYPE)
    print("✅ Product type term created")  

    print("Creating Borrow Onhold term...")
    BORROW_ONHOLD = await agent.create_term(
        name="Borrow Onhold",
        description="This refers to user's borrow profile status. A borrow profile can be put on hold when:: \n 1. There is a long due pending outstanding amount to repay. \n 2. Internal risk assessment. \n 3. Complete account closure or credit line closure request raised by user is processed / in progress. \n In this case the user's purchase power is set to 0.",
        synonyms=["onHold", "on hold","borrow profile onhold", "borrow onhold"]
    )
    terms.append(BORROW_ONHOLD)
    print("✅ Borrow onhold term created")

    print("Creating DSA term...")
    DSA = await agent.create_term(
        name="DSA",
        description="DSA is a term used to refer to the Digital Savings Account product that slice offers. It is like a regular savings account but offers interest rate equal to RBI's repo rate which is highest in the market currently.",
        synonyms=["dsa", "digital savings account", "savings account"]
    )
    terms.append(DSA)
    print("✅ DSA term created")

    PENNY_DROP = await agent.create_term(
        name="Penny Drop",
        description="Penny Drop is a way to ensure that provided bank account details by user are correct. In this, we debit INR 1.00 from user's bank to ensure the correctness of information. It is a part of verification process for linking the bank account. REMEMBER: PENNY DROP FAILURE MAY HAPPEN DURE TO INSUFFICIENT BALANCE IN USER'S BANK ACCOUNT OR DUE TO BANK SIDE FAILURES SUCH AS TECHNICAL. THE USER MAY RETRY IN SUCH CASES",
        synonyms=["pd", "penny drop failure"]
    )
    terms.append(PENNY_DROP)
    print("✅ Penny drop term created")

    NAME_MATCH = await agent.create_term(
        name="Name Match",
        description="Name Match is a way to ensure that the name on the bank account details provided by user is correct. In this, we verify the name on the bank account details with the name on the user's profile. It is a part of verification process for linking the bank account.",
        synonyms=[ "name match verification", "name mismatch error"]
    )
    terms.append(NAME_MATCH)
    print("✅ Name match term created")

    print(f"\n✅ All {len(terms)} glossary terms registered successfully!")
    return terms

