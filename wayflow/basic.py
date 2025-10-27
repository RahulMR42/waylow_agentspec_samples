import os
from wayflowcore.models import OCIGenAIModel
from config.config import config_map
from wayflowcore.models.llmgenerationconfig import LlmGenerationConfig
from tools import temperature_check

class WayflowChat:

    def __init__(self,llm) -> None:
        """
        Init An assistant with basic context.
        Input:
         llm : wayflowllm config
        Output:
          Print agent conversation
        """

        from wayflowcore.agent import Agent
        from textwrap import dedent

        custom_instruction = dedent(
        """
        You are helpful agent.
        ## Context
        You will receive a city for temperature check
        ## Task
        You will follow the next instructions:
        1.Use tool temperature_check to check and provide the weather status.
        ## Output Format
        Return the summary as simple as it could.
        """).strip()

        self.llm = llm
        self.agent_master = Agent(llm=llm,
                          custom_instruction=custom_instruction,
                          tools=[temperature_check]
                          ) 
        
    def chat(self,prompt:str=None):
        try:
            conversation = self.agent_master.start_conversation()
            print(conversation.get_last_message())
            conversation.append_user_message(prompt)
            conversation.execute()
            last_message = conversation.get_last_message()
            print(last_message)
        except Exception as error:
            print(error)



if __name__ == "__main__":
    generation_config = LlmGenerationConfig(max_tokens=256, temperature=0.8, top_p=0.95)
  
    llm_oci_genai = OCIGenAIModel(
        model_id=config_map['model'],
        service_endpoint=f"https://inference.generativeai.{config_map['oci_region']}.oci.oraclecloud.com",
        compartment_id=config_map['compartment_id'],
        auth_type="API_KEY",
        auth_profile=config_map['oci_auth_profile'],
        generation_config=generation_config,
    )
    wayflow_handler = WayflowChat(llm=llm_oci_genai)
    wayflow_handler.chat(prompt="What is the weather in SFO ?")

