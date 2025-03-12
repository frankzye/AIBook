from transformers import AutoTokenizer, AutoModelForCausalLM, DataCollatorForLanguageModeling
from peft import LoraConfig, get_peft_model
import torch.optim as optim
import torch.nn as nn
import torch
from datasets import Dataset
from torch.utils.data import DataLoader
from transformers import Trainer
from transformers import TrainingArguments

# 加载 Qwen 模型和分词器
model_name = "Qwen/Qwen2.5-0.5B"  # 根据实际情况选择模型大小
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# 定义 LoRA 配置
lora_config = LoraConfig(
    r=8,  # 低秩矩阵的秩
    lora_alpha=16,  # 缩放因子
    target_modules=["q_proj", "v_proj"],  # 需要微调的模块
    lora_dropout=0.1,  # Dropout 概率
    bias="none",  # 是否微调偏置项
)

# 将 LoRA 应用到模型中
model = get_peft_model(model, lora_config)

# load_dataset
data = {
    "input": ["我的名字叫什么", "我在什么地方"], "output": ["我的名字叫小艺", "我在宇宙的中心"], "weight": [3.0, 1.0]
}

dataset = Dataset.from_dict(data)


def preprocess(example):
    # 输入文本处理
    model_inputs = tokenizer(
        example["input"],
        padding="max_length",
        truncation=True,
        max_length=32  # 根据任务调整
    )
    
    # 输出文本处理（标签）
    labels = tokenizer(
        example["output"],
        padding="max_length",
        truncation=True,
        max_length=32
    )["input_ids"]
    
    # 添加权重列
    model_inputs["weight"] = example["weight"]
    model_inputs["labels"] = labels  # 必须包含标签
    
    return model_inputs


# 对数据集进行预处理
tokenized_ds = dataset.map(preprocess, batched=True, remove_columns=["input", "output"])

training_args = TrainingArguments(
    output_dir="./results",          # 输出目录
    per_device_train_batch_size=4,  # 每个设备的 batch size
    num_train_epochs=1000,              # 训练轮数
    logging_dir="./logs",            # 日志目录
    save_steps=500,                 # 保存模型的步数
    save_total_limit=2,             # 最多保存的模型数量
    learning_rate=5e-5,             # 学习率
    fp16=True,                      # 使用混合精度训练
    push_to_hub=False,               # 是否上传到 Hugging Face Hub
    remove_unused_columns=False
)


class WeightedGenerationTrainer(Trainer):
    def compute_loss(self, model, inputs, return_outputs=False, num_items_in_batch=None):
        # 提取权重
        weights = inputs.pop("weight").to(self.args.device)

        # 前向传播
        outputs = model(**inputs)
        logits = outputs.logits

        # 计算加权损失
        labels = inputs.get("labels")
        shift_logits = logits[..., :-1, :].contiguous()
        shift_labels = labels[..., 1:].contiguous()

        # 扩展权重到每个token
        token_weights = weights.unsqueeze(-1).repeat(1, shift_labels.size(1))
        token_weights = token_weights.view(-1).contiguous()

        loss_fct = torch.nn.CrossEntropyLoss(reduction="none")
        loss = loss_fct(
            shift_logits.view(-1, shift_logits.size(-1)),
            shift_labels.view(-1)
        )
        weighted_loss = (loss * token_weights).mean()  # 对每个token的损失加权

          # 使用 num_items_in_batch 归一化
        if num_items_in_batch is not None:
            weighted_loss = weighted_loss / num_items_in_batch
        
        return (weighted_loss, outputs) if return_outputs else weighted_loss


trainer = WeightedGenerationTrainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_ds,
    data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False, return_tensors="pt")
)

# 开始训练
trainer.train()
