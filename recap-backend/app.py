from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi

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

import base64


app = Flask(__name__)
CORS(app)
#CORS(app, origins=['http://localhost:3000', 'http://127.0.0.1:8000'])

#========================================= METHODS ========================================= 
def get_transcript(video_id="",text_language='en'):

    #text_language='en' #en que idioma va a estar el video, los timestamps (NOTA: El chatbot te hablara en el idioma que tu le hables. A pesar de ello el prompt "La data con la que has sido entrenado es un conjunto de transcripciones de videos de youtube." que va a antes del query deberia ser cambiado a este idioma para que no haya conflictos entre el idioma del prompt y el query del usuario.)

    #Recogemos la transcripcion del video en formato de lista
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    transcript = transcript_list.find_generated_transcript([text_language]).fetch()
    # Convierte los tiempos start a un formato standard
    for t in transcript:
        hours = int(t["start"] // 3600)
        min = int((t["start"] // 60) % 60)
        sec = int(t["start"] % 60)
        t["start"] = f"{hours:02d}:{min:02d}:{sec:02d}"
    
    return transcript

def create_video_summarized(transcript):

    load_dotenv()

    if (transcript):

        # Chunk and embed the transcript
        knowledge_base = chunk_and_embedding_transcript(transcript)

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

            max_tokens_limit = 50 #limite ideal 2000 #para poder limitar cuantos caracteres quieres que genere el response de GPT (Bueno para pruebas y para no gastar tokens)
            model_n = "gpt-3.5-turbo-1106"


            docs = knowledge_base.similarity_search(query)
            llm = OpenAI() #max_tokens  = max_tokens_limit
            chain = load_qa_chain(llm, chain_type="stuff")
            with get_openai_callback() as cb:
                response_gpt = chain.run(input_documents=docs, question=query)
                print(cb)
            
            """
            #save response to a file
            with open('response.txt', 'w') as f:
                f.write(response_gpt)
            """
            
            pprint(response_gpt)

            #convert response to audio
            elevenlabs_api_key = os.getenv("ELEVEN_LABS_API_KEY")
            voice_id = "knrPHWnBmmDHMoiMeP3l"
            model_id = "eleven_turbo_v2" #eleven_turbo_v2 solo soporta ingles #"eleven_multilingual_v2" es el modelo que soporta mas idiomas pero el latency es mas alto


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

            # Convierte el contenido binario a una cadena base64
            response_eleven_labs_audio_base64 = base64.b64encode(response_elevenlabs.content).decode()


            """
            #convertirlo a un archivo de audio
            CHUNK_SIZE = 1024
            with open('output.mp3', 'wb') as f:
                for chunk in response_elevenlabs.iter_content(chunk_size=CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)
            """
            
            return {"gpt": response_gpt, "elevenlabs": response_eleven_labs_audio_base64}

def chunk_and_embedding_transcript(transcript):

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

    return knowledge_base

def get_response_from_chatbot(user_query="", video_id=""):

    if (user_query and video_id):

        load_dotenv()

        transcript = get_transcript(video_id)

        '''Ver la forma de como almacenar tanto el transcript y el knowledge base para no tener que volver a hacerlo cada vez que se haga una peticion al chatbot'''
        '''Crear otra vez el knowledge base nos quita dinero de los tokens'''
        # Chunk and embed the transcript
        knowledge_base = chunk_and_embedding_transcript(transcript)

        # Query the vector database for information. #Tomar en cuenta que el idioma de respuesta del chatbot tal vez dependa de este texto (y no de en que idioma hable el usuario): The data with which you have been trained is a set of transcriptions from YouTube videos.
        query = f"""

            The data with which you have been trained is a set of transcriptions from YouTube videos.

            {user_query}
        """

        if (query):

            max_tokens_limit = 2000 #limite ideal 2000 #para poder limitar cuantos caracteres quieres que genere el response de GPT (Bueno para pruebas y para no gastar tokens)

            docs = knowledge_base.similarity_search(query)
            llm = OpenAI(max_tokens  = max_tokens_limit)
            chain = load_qa_chain(llm, chain_type="stuff")
            with get_openai_callback() as cb:
                response_gpt = chain.run(input_documents=docs, question=query)
            
            return response_gpt
        
#========================================= ROUTES ========================================= 
@app.get('/summarize') #Returns a summarized transcription using GPT-3 (using the original transcription like data) and returns this summary in audio
def summary_api():
    video_id = request.args.get('url', '')

    response_summarized = create_video_summarized(get_transcript(video_id)) #video_summarized = create_video_summarized(transcript)#get_summary(get_transcript(video_id))

    return response_summarized, 200

@app.post('/chat') #Returns a response from the chatbot
def chat_api():

    user_query = request.get_json().get("message")
    video_id = request.get_json().get("video_id")

    pprint(user_query)
    pprint(video_id)

    response = get_response_from_chatbot(user_query, video_id)

    pprint(response)

    message = {"answer": response}

    return jsonify(message), 200


if __name__ == '__main__':
    app.run(debug = True)