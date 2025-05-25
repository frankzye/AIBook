from openai import OpenAI
import base64
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GPT_IMAGE_KEY"),  # 换成你在后台生成的 Key "sk-***"
    base_url="https://aihubmix.com/v1"
)

prompt = """redesign poster of the movie [Black Swan], 3D cartoon, smooth render, bright tone, 2:3 portrait."""

result = client.images.edit(
    model="gpt-image-1",
    image=open("yourpath/edit.jpg", "rb"),  # 多参考图应使用 [列表，]
    n=2,  # 单次数量
    prompt=prompt,
    size="1024x1536",  # 1024x1024 (square), 1536x1024 (3:2 landscape), 1024x1536 (2:3 portrait), auto (default)
    # moderation="low", # edit 不支持 moderation
    quality="high"  # high, medium, low, auto (default)
)

print(result.usage)

# 定义文件名前缀和保存目录
output_dir = "."  # 可以指定其他目录
file_prefix = "image_edit"  # 修改文件名前缀

# 确保输出目录存在
os.makedirs(output_dir, exist_ok=True)

# --- 遍历 API 返回的每张图片数据 ---
for i, image_item in enumerate(result.data):
    image_base64 = image_item.b64_json
    if image_base64 is None:
        print(f"警告：第 {i+1} 张图片没有返回 base64 数据，跳过保存。")
        continue  # 如果没有 b64_json 数据，跳到下一张图片

    image_bytes = base64.b64decode(image_base64)

    # --- 为当前图片寻找不冲突的文件名 ---
    current_index = 0  # 每次都从 0 开始检查，或者维护一个全局递增的索引
    while True:
        # 构建带自增序号的文件名
        file_name = f"{file_prefix}_{current_index}.png"
        file_path = os.path.join(output_dir, file_name)  # 构建完整文件路径

        # 检查文件是否存在
        if not os.path.exists(file_path):
            break  # 文件名不冲突，跳出内部循环

        # 文件名冲突，增加序号
        current_index += 1

    # 使用找到的唯一 file_path 保存当前图片到文件
    try:
        with open(file_path, "wb") as f:
            f.write(image_bytes)
        print(f"第 {i+1} 张编辑后的图片已保存至：{file_path}")
    except Exception as e:
        print(f"保存第 {i+1} 张图片时出错 ({file_path}): {e}")
