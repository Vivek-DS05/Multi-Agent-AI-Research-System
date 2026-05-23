#pipeline.py
from agents import (
    build_reader_agent,
    build_search_agent,
    writer_chain,
    critic_chain
)

def run_research_pipeline(topic: str):

    state = {}

    # SEARCH
    search_agent = build_search_agent()

    search_result = search_agent.invoke({
        "messages": [
            ('user', f'Find recent, reliable and detailed information about: {topic}')
        ]
    })

    state["search_result"] = search_result['messages'][-1].content

    # SCRAPE
    reader_agent = build_reader_agent()

    reader_result = reader_agent.invoke({
        'messages': [
            (
                'user',
                f'Based on the following search result about "{topic}", '
                f'pick the most relevant URL and scrape it for deeper content.\n\n'
                f'Search Results:\n{state["search_result"][:800]}'
            )
        ]
    })

    state['scraped_content'] = reader_result['messages'][-1].content

    # COMBINE RESEARCH
    research_combined = (
        f"Search Results:\n{state['search_result']}\n\n"
        f"Detailed Scraped Content:\n{state['scraped_content']}"
    )

    # WRITE REPORT
    state['report'] = writer_chain.invoke({
        'topic': topic,
        'research': research_combined
    })

    print("\nFINAL REPORT\n")
    print(state['report'])

    # CRITIC
    state['feedback'] = critic_chain.invoke({
        'report': state['report']
    })

    print("\nCRITIC REPORT\n")
    print(state['feedback'])

    return state


if __name__ == '__main__':

    topic = input('Enter a research topic: ')

    run_research_pipeline(topic)
