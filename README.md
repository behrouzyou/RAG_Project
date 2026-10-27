# 🔍 Similarity Search — Semantic Retrieval over Persian Documents

A minimal, hands-on implementation of **semantic similarity search** using text embeddings and cosine similarity. Documents are embedded once, and user queries are matched against them in real time — returning the top‑K most relevant results.

This project is a small, self-contained example of the core idea behind **RAG (Retrieval-Augmented Generation)** pipelines.

---

## 📌 Features

- 🧠 **Embedding-based retrieval** — no keyword matching, pure semantic similarity
- 🌐 **Multilingual** — works out of the box with Persian (فارسی) queries and documents
- 📄 **Metadata support** — each document carries a `category` (account / shipping / support)
- 📊 **Scored results** — every match is returned with its cosine similarity score
- 🖥️ **Interactive CLI** — ask queries in a loop, exit with `exit` / `quit` / `خروج`
- 🪶 **Tiny & readable** — a single `main.py`, no frameworks, no boilerplate

---

## 🗂️ Repository Structure
similarity-search/
├── main.py # Main script
├── .env # Local secrets (NOT committed)
├── .env.example # Template for required env vars
├── .gitignore
├── requirements.txt
└── README.md

text

---

## ⚙️ Requirements

- Python **3.9+**
- [`openai`](https://pypi.org/project/openai/) SDK (v1.x)
- [`python-dotenv`](https://pypi.org/project/python-dotenv/)
- [`scikit-learn`](https://scikit-learn.org/) (for `cosine_similarity`)

Install:

```bash
pip install openai python-dotenv scikit-learn
Or:

bash
pip install -r requirements.txt
🔐 Environment Setup
Create a .env file in the project root:

env
HF_TOKEN=your_api_key_here
The script reads this variable at startup and exits with an error if it's missing — a good safety default.

⚠️ Never commit .env to Git. It is listed in .gitignore.

🚀 Usage
Clone the repo

bash
git clone https://github.com/behrouzyou/similarity-search.git
cd similarity-search
Set up a virtual environment

bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
pip install -r requirements.txt
Configure the API key

bash
cp .env.example .env
# then edit .env and set HF_TOKEN
Run

bash
python main.py
Ask queries

text
Query: چطور رمز عبورم رو عوض کنم؟
Query: چطور رمز عبورم رو عوض کنم؟
------------
ID: 1
Score: 0.9123
Text: برای تغییر رمز عبور وارد تنظیمات حساب شوید.
------------
ID: 2
Score: 0.8712
Text: اگر پسورد خود را فراموش کرده‌اید، از گزینه بازیابی حساب استفاده کنید.
Type exit, quit, or خروج to stop.

🧠 How It Works
1. Embedding model
python
model="gemini-embedding-001"
Each document and query is converted to a vector via the embeddings.create endpoint (OpenAI-compatible API at https://api.gapgpt.app/v1).

2. Document indexing
At startup, every document in the documents list is embedded once and stored alongside its metadata:

python
indexed_documents = [
    {"id": ..., "text": ..., "metadata": ..., "embedding": [...]},
    ...
]
3. Query-time retrieval
For each user query:

The query is embedded.

Cosine similarity is computed against every document embedding.

Results are sorted descending by score.

The top‑2 matches are printed with their scores.

4. Cosine similarity
text
        A · B
cos = -----------
      ||A|| ||B||
sklearn.metrics.pairwise.cosine_similarity handles this efficiently, and the score is bounded to [-1, 1] (in practice, [0, 1] for text embeddings).

📚 Sample Dataset
Five Persian documents across three categories:

ID	Category	Content (summary)
1	account	How to change your password
2	account	Recovering a forgotten password
3	shipping	Delivery time inside Tehran (1–2 business days)
4	shipping	Shipping cost calculation
5	support	Cancelling an order before shipment
Easily replaceable — just edit the documents list in main.py.

⚠️ Notes & Limitations
Truncated embeddings: response.data[0].embedding[:5] keeps only the first 5 dimensions of each vector. This is enough for a demo but will significantly reduce retrieval quality. Remove [:5] for real use.

No persistence: embeddings are recomputed on every run. For a larger corpus, cache them (e.g., numpy.save, pickle, or a vector DB).

Linear scan: every query is compared against every document — fine for 5 documents, slow for millions. For scale, use FAISS, Chroma, Qdrant, or pgvector.

No thresholding: low-scoring matches are still returned. Consider filtering by a minimum score.

No streaming / UI: it's a plain CLI loop by design.

🛠️ Possible Improvements
□ Remove [:5] truncation for full-dimensional embeddings
□ Cache embeddings to disk to avoid recomputation
□ Replace linear scan with FAISS / Chroma / Qdrant
□ Add a min_score threshold to drop weak matches
□ Support top‑K as a CLI argument
□ Filter by metadata (e.g., only category == "shipping")
□ Add a small RAG demo: feed top results into an LLM for a grounded answer
□ Unit tests for the retrieval pipeline
📄 License
Released for educational and personal use. Modify freely.

🙏 Acknowledgements
OpenAI Python SDK

python-dotenv

scikit-learn

gapgpt.app — OpenAI-compatible API provider

Author: behrouzyou