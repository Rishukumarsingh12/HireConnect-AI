import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)


from app.agent.company_research_agent import (
    CompanyResearchAgent
)


def main():

    agent = CompanyResearchAgent()

    result = agent.research(
        "SourceFuse Technologies"
    )
    
    print(result)


if __name__ == "__main__":
    main()