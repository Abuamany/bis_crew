#=================
# Import Libraries
#=================

import streamlit as st
from crewai import Agent, Task, Crew
import os
from langchain_cohere import ChatCohere


#=================
# Add Streamlit Components
#=================

#background
page_bg_img = '''
<style>
.stApp  {
background-image: url("https://images.all-free-download.com/images/graphiclarge/abstract_bright_corporate_background_310453.jpg");
background-size: cover;
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)

# title
st.title("ICC-AI Newsletter Generator")

# logo
image_url = "https://cdn-icons-png.flaticon.com/512/1998/1998614.png"
st.sidebar.image(image_url, caption="", use_column_width=True)
st.sidebar.write("This AI-powered Newsletter Generator is built using a Multi-Agent AI system. It provides comprehensive newsletters, statistical analysis, and the latest information on any topic. The Multi-Agent AI delivers on-demand knowledge!")
# Request Cohere API Key as a password input for security
cohere_api_key = st.sidebar.text_input('Enter your Cohere API Key', type='password')
# text input
business = st.text_input('Enter Newsletter Topic')
stakeholder = st.text_input('Enter Stakeholder or Team')

#=================
# LLM Object and API Key
#=================



if cohere_api_key:
    os.environ["COHERE_API_KEY"] = cohere_api_key
    llm = ChatCohere()

    #=================
    # Crew Agents
    #=================

    Research = Agent(
        role="Senior Researcher",
        goal="Uncover the latest developments in {topic}",
        backstory="You work to provide insights about: {topic}. "
                  "You gather information that helps stakeholders make informed decisions. "
                  "Your work forms the foundation for the Business Writer "
                  "to offer accurate and insightful content. "
                  "As a highly experienced journalist, your research is thorough and reliable, "
                  "and you always ensure to include the complete URL of the articles you reference.",
        allow_delegation=False,
        verbose=True,
        llm=llm
    )

    writer = Agent(
        role="Business Writer",
        goal="Craft accurate and insightful content about the topic: {topic}",
        backstory="You are tasked with writing a comprehensive business insight report on: {topic}. "
                  "You build on the work of the Researcher and Data Analyst, "
                  "who provide research and statistical analysis for your writing. "
                  "Your report is professional, objective, and aligned with the interests of the stakeholders: {stakeholder}.",
        allow_delegation=False,
        verbose=True,
        llm=llm
    )

    analyst = Agent(
        role="Data Analyst",
        goal="Provide comprehensive statistical analysis on the topic: {topic}",
        backstory="Your strong analytical skills are used to provide detailed statistical reports on the topic: {topic}. "
                  "Your analysis helps the Business Writer and aligns with the work of the Researcher.",
        allow_delegation=False,
        verbose=True,
        llm=llm
    )

    editor = Agent(
        role="Chief Editor",
        goal="Ensure the quality and accuracy of the final newsletter for the topic: {topic}",
        backstory="You are the Chief Editor at a prestigious news organization. "
                  "You oversee the production of the newsletter, ensuring that it meets the highest standards of quality, accuracy, and readability. "
                  "You review articles provided by the Researcher, adding context and making sure the most important news stories are highlighted.",
        allow_delegation=False,
        verbose=True,
        llm=llm
    )

    #=================
    # Crew Tasks
    #=================

    research = Task(
      description=(
        """Conduct thorough research on the latest news for {topic}.
        Ensure you use reliable sources and up-to-date news. Do not include articles that are not directly relevant to {topic}.
        Create a list of the most relevant news stories based on your research.

        Follow these rules:
        - Only include articles that are directly relevant to {topic}. Avoid unrelated news.
        - Summarize each news story in a few sentences, including the most relevant information.
        - Include the URL for each article.
        - Provide between 7 and 10 relevant news articles.

        IMPORTANT: When using tools, do not use underscores "_" unless necessary. Ensure proper usage of tools for query searches."""),
      expected_output=
        """Markdown document with the most relevant news stories. Each story should include:
         - News Title
         - Summary of the news
         - URL of the article where the news was found
        Example format:

        <EXAMPLE>
          Story 1:
          - Title: **AI now outperforms humans in reading and basic math**
          - **Summary:** AI systems are now matching and sometimes surpassing human performance in basic tasks. This report explores the need for new benchmarks to assess AI capability and raises ethical considerations for AI models.
          - **URL:** [Nature Article](https://www.nature.com/articles/d41586-024-01125-1)
        </EXAMPLE>
        """,
      agent=Research,
    )

    analyse = Task(
      description="Perform comprehensive statistical analysis for {topic}.",
      expected_output="A detailed report with statistical tables and graphs to support the topic {topic}.",
      agent=analyst,
    )

    write = Task(
      description="Write a business insight report based on the research and analysis for {topic}.",
      expected_output="A detailed narrative report that includes comprehensive business insights for the topic {topic}.",
      agent=writer,
    )

    edit = Task(
      description="Review and edit the final document for {topic} to ensure quality, accuracy, and flow.",
      expected_output="The final document ready to be published as a newsletter for {topic}.",
      agent=editor,
    )

    #=================
    # Execution
    #=================

    crew = Crew(
        agents=[Research, writer, analyst, editor],
        tasks=[research, analyse, write, edit],
        verbose=2
    )

    if st.button("Run"):
        with st.spinner('Loading...'):
            result = crew.kickoff(inputs={"topic": business, "stakeholder": stakeholder})
            # st.write(result)

            # Use st.markdown to display the result in markdown format
            st.markdown(result)
