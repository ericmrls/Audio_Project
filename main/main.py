import openai as ai
import tempfile
import os
import sys

from utils import tts, stt, play_audio, record_audio, kaldi

from dotenv import load_dotenv

load_dotenv()

def chat(question,chat_log = None) -> str:
    if(chat_log == None):
        chat_log = start_chat_log
    prompt = f"{chat_log}\nHuman: {question}\nAI:"
    response = completion.create(prompt = prompt, engine =  "ada", temperature = 0.85,top_p=1, frequency_penalty=0, 
    presence_penalty=0.7, best_of=2,max_tokens=100,stop = "\nHuman: ")
    return prompt, response.choices[0].text

def modify_start_message(chat_log,question,answer) -> str:
    if chat_log == None:
        chat_log = start_chat_log
    chat_log += f"Human: {question}\nAI: {answer}\n"
    return chat_log


ai.api_key = os.getenv('OPENAI_KEY')

completion = ai.Completion()

start_chat_log = """Human: Hello, I am Human.
AI: Hello, human I am openai gpt3.
Human: How are you?
AI: I am fine, thanks for asking. 
"""

train = input("\nDo you want to train the openai chatbot (True/False): ")
if(train == "True"):
    print("\n(To stop the training enter stop in the question)\n")
    while(True):
        question = input("Question: ")
        if question == "stop":
            break
        answer = input("Answer: ")
        start_chat_log = modify_start_message(start_chat_log,question,answer)
        print("\n")

duration = 0
chat_log = start_chat_log
tmp_file = tempfile.NamedTemporaryFile().name


print("\nAsk openai questions (to quit type duration=0)")
while True:
    print(' '*20)
    sys.stdout.write("\033[F")
    duration = int(input("Question duration (seconds): "))
    print(' '*20)
    sys.stdout.write("\033[F")
    if duration == 0:
        break

    record_audio(tmp_file, seconds=duration)

    question = kaldi(tmp_file)
    print(f'Human: {question}')
    chat_log, answer = chat(question, chat_log)
    chat_log += answer

    tts(answer, tmp_file)
    play_audio(tmp_file)
    print("AI: ",answer)