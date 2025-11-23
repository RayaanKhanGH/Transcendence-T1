# Transcendence T1 - Setup Guide

## ✅ Successfully Removed Conflicts

The following unnecessary packages have been removed:

- ❌ TensorFlow (not used in the codebase)
- ❌ tf-keras (not needed)
- ❌ Keras (not needed)
- ❌ tensorboard (not needed)

**Protobuf version locked to 4.21.0-4.25.8** to avoid conflicts with google-genai and transformers.

---

## 🚀 CLI is Now Functional!

The interactive CLI (`cli.py`) is working successfully with:

- ✅ Google Gemini AI for intelligent URL planning
- ✅ Real web scraping with BeautifulSoup
- ✅ Sentence Transformers for embeddings
- ✅ Full intelligence processing pipeline

### How to Run:

```bash
python cli.py
```

---

## 📊 Optional: Database Setup

### PostgreSQL (Optional)

If you want to store intelligence in PostgreSQL:

1. Create a database:

```sql
CREATE DATABASE transcendence;
```

2. Create the intelligence table:

```sql
CREATE TABLE intelligence (
    id SERIAL PRIMARY KEY,
    source_url TEXT,
    content TEXT,
    summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

3. Update your `.env`:

```
POSTGRES_URI=postgresql://username:password@localhost:5432/transcendence
```

### Pinecone (Optional)

If you want to use vector search:

1. Go to [pinecone.io](https://www.pinecone.io/) and create an account
2. Create a new index named `transcendence-index` with:
   - **Dimensions**: 384 (for all-MiniLM-L6-v2 model)
   - **Metric**: cosine
3. Get your API key and update `.env`:

```
PINECONE_API_KEY=your_api_key_here
```

---

## 🎯 Current Status

### Working Components:

- ✅ AI-powered research planning (Gemini)
- ✅ Web scraping and data ingestion
- ✅ Text preprocessing
- ✅ Semantic embeddings (Sentence Transformers)
- ✅ AI summarization (Gemini)
- ✅ Interactive CLI

### Optional Components (work without them):

- ⏳ PostgreSQL storage (gracefully fails if not configured)
- ⏳ Pinecone vector DB (gracefully fails if not configured)

---

## 📝 Example Usage

```bash
$ python cli.py

Enter your research prompt (or 'exit' to quit):
>> latest cybersecurity threats in 2024

🤖 Analyzing prompt: 'latest cybersecurity threats in 2024'...
✓ Plan generated. Target URLs:
  - https://www.cisa.gov/news-events/cybersecurity-advisories
  - https://thehackernews.com/

Proceed with scraping? [y/n] (y): y

🕷️  Starting scraping job...
✓ Successfully scraped 2/2 sources.

🧠 Processing intelligence...
Processing: https://www.cisa.gov/news-events/cybersecurity-advisories
Summary: [AI-generated summary of the content]

✓ Intelligence cycle complete!
```

---

## 🔧 Troubleshooting

### If you get protobuf errors:

```bash
pip install "protobuf>=4.21.0,<5.0.0"
```

### If you get import errors:

```bash
pip install -r requirements.txt
```

---

**Last Updated:** 2025-11-23  
**Status:** Fully Functional ✅
