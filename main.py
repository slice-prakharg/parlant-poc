import os
import traceback
import parlant.sdk as p
from glossary import register_glossary_terms
from variables import create_and_register_variables
from journey_conditions.borrow import register_borrow_journey_selection_conditions
from journey_conditions.bank_linking_issues import register_bank_linking_issues_journey_selection_conditions
from journeys import create_journey_issues_with_borrow_application, register_borrow_canned_responses, create_journey_bank_linking_issues


async def main():
    async with p.Server(
        nlp_service=p.NLPServices.azure
    ) as server:
        agent = await server.create_agent(
            name="Super slicer",
            description="slice bank personal assistant"
            
        )

        
        # create customer
        customer = await server.create_customer(name="Prakhar")
        print(f"Customer created: {customer.name}")

        # create and register variables
        await create_and_register_variables(agent)
        print("Variables created and registered")

        try:
            #register canned responses
            await register_borrow_canned_responses(agent)
        except Exception as e:
            print(f"\n❌ Error in register_borrow_canned_responses: {e}")
            print("\nFull traceback:")
            traceback.print_exc()


        # register journey selection guideline conditions
        await register_borrow_journey_selection_conditions(agent)
        await register_bank_linking_issues_journey_selection_conditions(agent)
        print("Journey conditions registered")

        try:
            await create_journey_issues_with_borrow_application(agent)
            print("Journey issues created and registered")
        except Exception as e:
            print(f"\n❌ Error in create_journey_issues_with_borrow_application: {e}")
            print("\nFull traceback:")
            traceback.print_exc()

        try:
            await create_journey_bank_linking_issues(agent)
            print("Journey bank linking issues created and registered")
        except Exception as e:
            print(f"\n❌ Error in create_journey_bank_linking_issues: {e}")
            print("\nFull traceback:")
            traceback.print_exc()

        # register glossary terms
        await register_glossary_terms(agent)
        print("Glossary terms registered")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())