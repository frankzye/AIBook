import chromadb
from vllm import LLM, SamplingParams

chroma_client = chromadb.HttpClient(host='localhost', port=8000)

# check if the collection exists
if "my_collection" not in chroma_client.list_collections():
    collection = chroma_client.create_collection(name="my_collection")
    collection.add(
        documents=[
            "我是一个中国人",
            "我家在广州"
        ],
        ids=["id1", "id2"]
    )
else:
    collection = chroma_client.get_collection(name="my_collection")


query = "有哪些餐厅比较出名"

results = collection.query(
    query_texts=["我的特点"],  # Chroma will embed this for you
    n_results=2  # how many results to return
)

# concat the results
context = " ".join(results["documents"][0])

sampling_params = SamplingParams(temperature=0.8, top_p=0.95, max_tokens=1000)

llm = LLM(model="Qwen/Qwen2.5-1.5B-Instruct", device="cpu")

outputs = llm.generate([f"根据以下上下文，{context}, 帮我回答这个问题: {query}\n\n"], sampling_params=sampling_params)

for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")
