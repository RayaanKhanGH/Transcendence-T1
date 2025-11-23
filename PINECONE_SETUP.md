# Pinecone Index Setup Instructions

## Option 1: Sentence Transformers (Recommended - Current Setup)

**Create index with these settings:**

- **Index Name**: `transcendence-index`
- **Dimensions**: `384`
- **Metric**: `cosine`
- **Cloud**: AWS
- **Region**: us-east-1 (or your preferred)

**Pros:**

- ✅ Free (no API costs)
- ✅ Fast (local processing)
- ✅ Private (data stays local)
- ✅ Already implemented in the code

---

## Option 2: OpenAI text-embedding-3-large (Alternative)

**Create index with these settings:**

- **Index Name**: `transcendence-index`
- **Dimensions**: `3072`
- **Metric**: `cosine`
- **Cloud**: AWS
- **Region**: us-east-1 (or your preferred)

**Additional Requirements:**

1. Add to `.env`:

   ```
   OPENAI_API_KEY=your_openai_key_here
   ```

2. Install OpenAI SDK:

   ```bash
   pip install openai
   ```

3. Update embedder to use OpenAI (requires code changes)

**Pros:**

- Higher quality embeddings
- Better semantic understanding

**Cons:**

- ❌ Costs ~$0.13 per 1M tokens
- ❌ API latency
- ❌ Data sent to OpenAI
- ❌ Requires code modifications

---

## 🎯 My Recommendation

**Use Sentence Transformers (Option 1)** because:

1. It's already implemented and working
2. Zero cost
3. Fast and private
4. 384 dimensions is sufficient for most OSINT use cases
5. You can always migrate to OpenAI later if needed

---

## Quick Setup (Sentence Transformers)

1. Go to [pinecone.io](https://app.pinecone.io/)
2. Create a new index:
   - Name: `transcendence-index`
   - Dimensions: `384`
   - Metric: `cosine`
3. Copy your API key
4. Add to `.env`:
   ```
   PINECONE_API_KEY=pcsk_xxxxx_xxxxx
   ```
5. Run the CLI again - it will automatically connect!

---

**Note:** If you still want OpenAI embeddings, let me know and I'll update the code to support it as an option.
