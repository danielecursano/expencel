from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime


model = init_chat_model("llama3-8b-8192", model_provider="groq")

system_template = f"""
You are provided with a dataframe containing data on daily expenses, including information such as the date, category (e.g., restaurants, transportation, entertainment), amount, and a description of the purchase. The expense descriptions may contain relevant details for a deeper understanding of the transactions.  

Your responses must be based solely on the provided data, answering the user's questions using the information contained in the dataframe. For complex questions, explore and analyze the expense descriptions, making inferences if necessary (e.g., comparing different categories or time periods).  

If a question involves a temporal analysis (e.g., comparing expenses across different months), make sure to carefully consider the dates and provide a contextualized response based on the time-related data.  

Always respond with text. For your information, today’s date is: {datetime.now().isoformat()}
"""

prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", "Dataframe: {dataframe}, Prompt: {prompt}, sheet_name: {sheet_name}")]
)

def interact(df_name, prompt, df):
    prompt_input = prompt_template.invoke({"dataframe": df.to_string(), "prompt": prompt, "sheet_name": df_name})
    response = model.invoke(prompt_input)
    return response