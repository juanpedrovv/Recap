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
            La data con la que has sido entrenado es un conjunto de transcripciones de videos de youtube.

            Podrias resumir de que trata el video?
                             
        """

        if (query):

            docs = knowledge_base.similarity_search(query)
            llm = OpenAI()
            chain = load_qa_chain(llm, chain_type="stuff")
            with get_openai_callback() as cb:
                response = chain.run(input_documents=docs, question=query)
                print(cb)
            
            pprint(response)


if __name__ == '__main__':
    main()



#Fuentes:
#    - https://www.neum.ai/post/llm-spreadsheets
#    - https://www.youtube.com/watch?v=wUAUdEw5oxM
#    - https://medium.com/@oladenj/extracting-timestamps-from-youtube-video-transcripts-using-python-e2329503d1e0