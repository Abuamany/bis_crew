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

#st.markdown(page_bg_img, unsafe_allow_html=True)

# title
st.title("ICC-AI Newsletter Generator")

# logo
image_url = "https://cdn-icons-png.flaticon.com/512/1998/1998614.png"
st.sidebar.image(image_url, caption="", use_column_width=True)
st.sidebar.write(" This AI Newsletter Generator is built using AI Multi-Agent system. It can give you comprehensive newsletter, statistical analysis and up-to-date information about any topic. This AI Multi-Agent delivers knowledge on demand!")

# text inputs
business = st.text_input('Enter The Topic Newsletter')
stakeholder = st.text_input('Enter The Stakeholder or team ')

#=================
# LLM object and API Key
#=================
os.environ["COHERE_API_KEY"] =
llm = ChatCohere()


#=================
# Crew Agents
#=================

Research = Agent(
    role="Senior Researcher",
    goal="Uncover cutting-edge developments in {topic}",
    backstory="You're working on providing Insights about : {topic} "
              "You collect information that help them take decisions "
              "Your work is the basis for "
              "the Business Writer to deliver good insights."
              "You're a seasoned journalist with a nose for news. You're known for your great research skills and ability to dig up the most interesting stories. Your reports are always thorough and well-researched, making you a trusted source of information."
              "You always follow the rules and guidelines provided to you and you never forget to include the complete URL of the article where you found the news.",
    allow_delegation=False,
	verbose=True,
    llm = llm
)


writer = Agent(
    role="Business Writer",
    goal="Write insightful and factually accurate "
         "insights about the topic: {topic}",
    backstory="You're writing a Business Insights document "
              "about the topic: {topic}. "
              "You base your design on the work of "
              "the Business Consultant, who provides an outline "
              "and relevant context about the : {topic}. "
              "and also the data analyst who will provide you with necessary analysis about the : {topic} "
              "You follow the main objectives and "
              "direction of the outline, "
              "as provided by the Business Consultant. "
              "You also provide objective and impartial insights "
              "and back them up with information "
              "provided by the Business Consultant."
              "design your document in a professional way to be presented to : {stakeholder}."
              ,
    allow_delegation=False,
    verbose=True,
    llm=llm
)


analyst = Agent(
    role="Data Analyst",
    goal="Perform Comprehensive Statistical Analysis on the topic: {topic} ",
    backstory="You're using your strong analytical skills to provide a comprehensive statistical analysis with numbers "
              "about the topic: {topic}. "
              "You base your design on the work of "
              "the Business Consultant, who provides an outline "
              "and relevant context about the : {topic}. "
              "You follow the main objectives and "
              "direction of the outline, "
              "as provided by the Business Consultant. "
              "You also provide comprehensive statistical analysis with numbers to the Business Writer "
              "and back them up with information "
              "provided by the Business Consultant.",
    allow_delegation=False,
    verbose=True,
    llm=llm
)



editor =Agent(
    role ="Editor-in-Chief",
    goal ="Ensure the quality and accuracy of the final newsletter of the topic : {topic}",
    backstory="You are the Editor-in-Chief of a prestigious news organization. You are responsible for overseeing the production of the newsletter and ensuring that it meets the highest standards of quality, that it is accurate, well-written, and engaging."
               "You review the news articles provided by the researcher, add context to each article (like why the news story is relevant), and have a great sense of what will resonate with the readers. You use this sense of judgment to reorder the news articles in a way that the most important news is at the top of the list.",
    allow_delegation=False,
    verbose=True,
    llm=llm
)


#=================
# Crew Tasks
#=================

research= Task(
  description=(
    """Conduct a thorough research about the latest news on {topic}."
    Be sure to look for sources that are reliable and publish recent news. Do not include articles that are not news material or that are not directly related to {topic}."
    With this research, compile a list of the most relevant news stories that you found."

    Follow these rules:"
    - Only include articles that are especially relevant to {topic}. Do not include any news that are not directly related to {topic}." 
    - Do not include sources that are not a news article. If the content of the page includes a list of articles or looks like the front page of a website, do not include it in the list!"
    - Summarize the news in a few sentences. Make the summary as long as necessary to include all the relevant information, but not too long for a newsletter."
    - Include the URL of the article where you found the news."
    - Include a minimum of 7 news articles and a maximum of 10 news articles in the list."
    - When using the Search Tool, your search query should be concise (for example, "latest news on {topic}")."

    IMPORTANT INSTRUCTIONS ABOUT USING TOOLS: When using tools, DO NOT ESCAPE the underscore character "_", EVER. If you need to use a tool and pass in a parameter called 'search_query', you should write 'search_query', not 'search\_query'. THIS IS VERY IMPORTANT, else the tool will not work.
"""),
    
  expected_output=
    """A markdown document with the most relevant news stories. Each news story should contain the following:"
     - Title of the news
     - Summary of the news
     - URL of the article where the news was found
     Here is an example of the format of a news article that you could include in the document:
    
    <EXAMPLE>
      Story 1:
      - Title: **Daily briefing: AI now beats humans at basic reading and maths**
      - **Summary:** AI systems can now nearly match and sometimes exceed human performance in basic tasks. The report discusses the need for new benchmarks to assess AI capabilities and highlights the ethical considerations for AI models.
      - **URL:** [Nature Article](https://www.nature.com/articles/d41586-024-01125-1)
    </EXAMPLE>
      

      """,

agent=Research,
)

    
edit=Task(
  description=(
    """Given the list of news articles that will be used in the newsletter, do the following things:
    - Rewrite the title of each news article to make it more engaging and interesting for the readers of the newsletter.
    - Add a paragraph to each news article that explains why this news is important and how it can impact the readers of the newsletter.
    - Reorder the bullet points in a way that the most relevant news and topics are at the top of the list based on the importance of the news and topics.
    - Verify that the news articles are directly related to {topic} and that they are not off-topic. If they are off-topic, remove them from the list.
    - Verify that the URLs are correct and that they lead to the correct news article. They should lead to a news article and not to a list of articles or the front page of a website. If the URL is incorrect, ask the researcher to provide the correct URL.
    - Do not search for additional news articles or change the content of the news articles. Only edit the existing news articles.

    MPORTANT INSTRUCTIONS ABOUT USING TOOLS: When using tools, DO NOT ESCAPE the underscore character "_", EVER. If you need to use a tool and pass in a parameter called 'search_query', you should write 'search_query', not 'search\_query'. THIS IS VERY IMPORTANT, else the tool will not work."""),
    expected_output=
    "A markdown document with all the news to be included in the newsletter of the week. The document should have a title related to the curated stories of the week and a list of news articles.",    
agent=editor,
)


write = Task(
    description=(
        """1. Use the business consultant's plan to craft a compelling 
            document about {topic}.\n
		    2. Sections/Subtitles are properly named 
            in an engaging manner.\n
        3. Proofread for grammatical errors and 
            alignment with the brand's voice.\n
         3. Limit the document to only 500 words 
         4. Use impressive images and charts to reinforce your insights """
    ),
    expected_output="""- A markdown document A well-written Document 
        - A well-written Document 
        - providing Actionable insights for {stakeholder} """,
    agent=writer,
)


analyse = Task(
    description=(
        """1. Use the business consultant's plan to do 
            the needed statistical analysis with numbers on {topic}.\n
		    2. to be presented to {stakeholder} 
            in a document which will be deisgned by the Business Writer.\n
        3. You'll collaborate with your team of Business Consultant and Business writer 
            to align on the best analysis to be provided about {topic}.\n"""),
    expected_output="A clear comprehensive data analysis "
        "providing insights and statistics with numbers to the Business Writer ",
    agent=analyst,
)


#=================
# Execution
#=================

crew = Crew(
    agents=[Research,writer, analyst,editor],
    tasks=[edit, analyse, write],
    verbose=2
)

if st.button("Run"):
 with st.spinner('Loading...'):
  result = crew.kickoff(inputs={"topic": business,"stakeholder": stakeholder})
  #st.write(result)

# Use st.markdown to display the result in markdown format
  st.markdown(result)
