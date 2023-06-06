from chatterbot import ChatBot

def get_response(ques):

    bot = ChatBot(

    	'Bot',
    	
    	logic_adapters=[
       
		        {
		            'import_path': 'chatterbot.logic.BestMatch',
		            'default_response': 'I am sorry, but I do not understand.',
		            'maximum_similarity_threshold': 1000
		        }					
    	
    	]
    	)

    response = bot.get_response("- - "+ques) 
    response = str(response)
    response = response.replace("-", "")
    response = response.lower()
    response = response.strip()
    return response


        

        

        