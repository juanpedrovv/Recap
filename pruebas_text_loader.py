from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from pprint import pprint

from langchain.text_splitter import CharacterTextSplitter

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback


from langchain.callbacks import get_openai_callback

import requests
import os



def main():
    load_dotenv()

    #https://www.youtube.com/watch?v=xoKjzPjV3po
    video_id = "PR_ykicOZYU"
    text_language = "en" #esto deberia ser cambiado en el popup.js agregando un boton de settings

    #Recogemos la transcripcion del video en formato de lista
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    transcript = transcript_list.find_generated_transcript([text_language]).fetch()

    # Convierte los tiempos start a un formato standard
    for t in transcript:
        hours = int(t["start"] // 3600)
        min = int((t["start"] // 60) % 60)
        sec = int(t["start"] % 60)
        t["start"] = f"{hours:02d}:{min:02d}:{sec:02d}"

    if (transcript):

        text = ""

        for i in transcript:
            text += f'\n{i["text"]} - (start:{i["start"]})'
        
        pprint(text)

        # split into chunks
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text)

        # create embeddings
        embeddings = OpenAIEmbeddings()
        knowledge_base = FAISS.from_texts(chunks, embeddings)

        # Query the vector database for information.
        query = """

            I want you to take into account the following points:
                1. I want the response to be entertaining and not boring, as if it were a video.
                2. I want a very brief summary of what the video is about.
                3. Divide the video into sequential parts and mention what each part is about. Before mentioning each part of the video, I would like you to tell me the time at which that part of the video occurs. Note that for (start:value), value is the time at which each segment begins. Now, value would represent the time at which each segment begins.

        
            The format of the response should be as follows:
                This video is about...

                In the first part of the video (minute: value), it talks about...
                In the second part of the video (minute: value), it talks about...
                In the third part of the video (minute: value), it talks about...
                ...
                            
        """

        if (query):

            docs = knowledge_base.similarity_search(query)
            llm = OpenAI(max_tokens  = "100") #2000
            chain = load_qa_chain(llm, chain_type="stuff")
            with get_openai_callback() as cb:
                response_gpt = chain.run(input_documents=docs, question=query)
                print(cb)
            
            #save response to a file
            with open('response.txt', 'w') as f:
                f.write(response_gpt)
            
            pprint(response_gpt)

            #convert response to audio
            elevenlabs_api_key = os.getenv("ELEVEN_LABS_API_KEY")
            voice_id = "knrPHWnBmmDHMoiMeP3l"
            model_id = "eleven_turbo_v2"#"eleven_multilingual_v2"


            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

            payload = {
                "model_id": model_id,
                "voice_settings": {
                    "similarity_boost": 0,
                    "stability": 0.3
                },
                "text": response_gpt
            }
            headers = {
                "xi-api-key": elevenlabs_api_key,
                "Content-Type": "application/json"
            }

            response_elevenlabs = requests.request("POST", url, json=payload, headers=headers)

            pprint(response_elevenlabs)

            CHUNK_SIZE = 1024

            with open('output.mp3', 'wb') as f:
                for chunk in response_elevenlabs.iter_content(chunk_size=CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)
            
            

if __name__ == '__main__':
    main()



#Fuentes:
#    - https://www.neum.ai/post/llm-spreadsheets
#    - https://www.youtube.com/watch?v=wUAUdEw5oxM
#    - https://medium.com/@oladenj/extracting-timestamps-from-youtube-video-transcripts-using-python-e2329503d1e0
#    - https://community.openai.com/t/is-there-any-way-to-increase-chatbot-output-token-limits-working-from-a-custom-knowledge-base-and-deeply-ignorant/377220/8