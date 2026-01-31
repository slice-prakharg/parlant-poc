import os
import parlant.sdk as p
from glossary import register_glossary_terms
from variables import create_and_register_variables
from journey_conditions.borrow import register_borrow_journey_selection_conditions
from journeys import create_journey_issues_with_borrow_application


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

        # register journey selection guideline conditions
        await register_borrow_journey_selection_conditions(agent)
        print("Journey conditions registered")

        await create_journey_issues_with_borrow_application(agent)

        # register glossary terms
        await register_glossary_terms(agent)
        print("Glossary terms registered")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())