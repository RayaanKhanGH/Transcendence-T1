# Transcendence T1 Pipeline: Resource Consumption Brief

This document outlines the resource consumption profile of the Transcendence T1 OSINT pipeline, optimized for single-core execution (Alpha v0.1.0).

## 1. Pipeline Overview

The pipeline operates in four distinct stages, each with a unique resource signature:

| Stage             | Operation              | Primary Resource  | Type                  |
| :---------------- | :--------------------- | :---------------- | :-------------------- |
| **1. Planning**   | Discovery & Strategy   | **Network I/O**   | `Latency-Bound`       |
| **2. Ingestion**  | Fetching Content       | **Network I/O**   | `Throughput-Bound`    |
| **3. Processing** | Cleaning & Summarizing | **CPU & Network** | `Compute` + `Latency` |
| **4. Storage**    | Vector Database Upsert | **Network I/O**   | `Latency-Bound`       |

---

## 2. Detailed Resource Breakdown

### 🟢 Stage 1: Planning (Source Discovery)

**What it does:** Uses Selenium to search DuckDuckGo or web sources for relevant URLs.

- **CPU:** **Low**. Mostly waiting for browser navigation.
- **RAM:** **Moderate**. launching a headless browser instance consumes ~50-100MB.
- **Bottleneck:** **External Website Latency**. We are at the mercy of how fast the search engine responds.

### 🟡 Stage 2: Ingestion (Mass Parallel Fetching)

**What it does:** Downloads HTML content from 8-10 identified URLs simultaneously using `asyncio` & `aiohttp`.

- **CPU:** **Very Low (< 5%)**. The CPU only coordinates the requests.
- **RAM:** **Low**. Buffers small HTML text strings.
- **Bottleneck:** **Network Bandwidth**. This is the fastest stage thanks to asynchronous parallelism.

### 🔴 Stage 3: Processing (The Workhorse)

**What it does:** This stage runs a parallel loop for every article:

1.  **Preprocessing (CPU):** Cleans text, removes HTML tags, normalizes whitespace.
2.  **Summarization (Network/CPU):** Sends text to Gemini LLM for analysis.
3.  **Vector Tuple Generation (CPU):** Generates UUIDs and structures data.

- **CPU:** **Moderate-High (Peaking ~70-90% of 1 Core)**. Text parsing and JSON handling are the most compute-intensive parts of the Python process.
- **RAM:** **Low**. Text processing is memory efficient.
- **Bottleneck:** **API Latency (Gemini)**. Even with parallelism, we wait for the LLM to generate tokens.

### 🟢 Stage 4: Storage (Vector Upsert)

**What it does:** Sends batches of processed vectors to Pinecone.

- **CPU:** **Negligible**.
- **RAM:** **Low**.
- **Bottleneck:** **Network Latency**. Waiting for Pinecone's HTTP 200 OK response.

---

## 3. Optimization Summary (v0.1.1)

To ensure stability and respect hardware constraints, the following optimizations are strictly enforced:

- **Hardware Lock:** Process is physically bound to **CPU Core 0 Only**.
- **Single-Threaded Math:** `NumPy`, `Torch`, and `OpenMP` are forced to run on 1 thread to prevent "silent" multi-core usage.
- **Asynchronous I/O:** All network waits (Ingestion & Analysis) are parallelized, reducing total runtime by ~35% without increasing CPU cost.
