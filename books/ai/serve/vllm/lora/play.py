from peft import LoraConfig, get_peft_model
from transformers import AutoTokenizer, AutoModelForCausalLM, DataCollatorForLanguageModeling
from vllm import LLM, SamplingParams
from vllm.lora.request import LoRARequest
# 加载基础


llm = LLM(
    model="Qwen/Qwen2.5-0.5B",
    enable_lora=True,       # 启用LoRA支持
    max_num_seqs=8,         # 最大并发请求数
    tensor_parallel_size=1,  # GPU数量
)

sampling_params = SamplingParams(
    temperature=0.7,
    top_p=0.95,
    top_k=-1,
    max_tokens=512
)


while True:
    prompt = input("Enter promopt")
    outputs = llm.generate(
        prompt,
        sampling_params,
        lora_request=LoRARequest("adapter1", 1, "./results/checkpoint-1000")
    )

    for output in outputs:
        prompt = output.prompt
        generated_text = output.outputs[0].text
        print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")
