# use chromadb and qwen to build a rag system

## 1. install dependencies

```bash
pip install chromadb
```

## 2. run chroma server
```
chroma run --path /var/folders/db
```

## 3. build the rag system

```bash
python build_rag.py
```

