---

# 🚀 Hyper-Converged KV-Cache Offloading for Cost-Efficient LLM Inference

## 📖 Overview

This project explores **System Architecture and Performance Engineering** for Large Language Model (LLM) inference, addressing the high cost and limited capacity of GPU High Bandwidth Memory (HBM). It delivers a **Hyper-Converged KV-Cache Offloading pipeline** leveraging **vLLM**, **LMCache**, and **KVRocks** to redirect KV-cache data from GPU memory to high-throughput SSDs, establishing performance baselines and insights for high-throughput architectures.

---

## 🎯 Project Goals

* Design and implement a robust PoC for LLM inference offloading.
* Evaluate performance and cost-efficiency of two KV-Cache serving architectures:

  1. **Baseline:** DRAM-bound KV-Cache serving.
  2. **Proposed:** SSD-based KV-Cache Offloading via Hyper-Converged Architecture.

---

## 🛠️ Technology Stack & Environment

| Component                | Purpose                   | Details                                         |
| :----------------------- | :------------------------ | :---------------------------------------------- |
| **LLM Framework**        | High-throughput inference | vLLM (Continuous Batching)                      |
| **Cache Offloading**     | KV flow management        | LMCache + **KVRocks**                           |
| **Hardware**             | Compute & storage         | NVIDIA L4/A100 GPUs, Dual NVMe SSDs (**RAID0**) |
| **Tools & Optimization** | Benchmarking & tuning     | RocksDB, vLLM flags tuning                      |

---

## ⚡ Key Achievements (Highlighting KPIs)

* **Infrastructure Foundation:** Provisioned the robust Hyper-Converged **KVRocks** setup and built the **high-throughput RAID0 NVMe SSD array**. This configuration provided the stability required for **Dynamo and LLMD deployments**.
* **System Optimization Success:** Optimized core RocksDB parameters and vLLM flags through **system-level tuning**, resulting in an overall **$\mathbf{1.5\times}$ improvement in TPS/RPS**.
* **Performance Baseline Established:** Conducted benchmarking and quantified DRAM caching as approximately **$\mathbf{2.5\times}$ faster in TPS/RPS** than the SSD configuration, informing cost-performance decisions.
* **Architectural Insight:** Identified **network serialization** as the dominant system bottleneck, not disk I/O.
* **Knowledge Transfer:** Established **optimal configuration patterns and best practices** for team deployments.

---

📈 Performance Visualization

Figure 1: DRAM vs KVRocks Initial Benchmark
Blue line: DRAM | Green/Purple line: KVRocks
Illustrates the original $\mathbf{2.5\times}$ TPS/RPS difference.

<img width="1544" height="814" alt="image" src="https://github.com/user-attachments/assets/b7d88f94-6840-4c3d-8c1d-835b90b5b3c9" />

Figure 2: KVRocks Optimization (Before vs. After Tuning)
Baseline (green) vs Tuned (purple)
Highlights $\mathbf{1.5\times}$ improvement achieved through system-level tuning.

<img width="1544" height="814" alt="image" src="https://github.com/user-attachments/assets/bfe9b687-5c6f-4418-a0f7-ea1fe689d3f2" />

---

## 📝 Detailed Project Contributions (8 Steps)

1. **Provisioned the foundational Hyper-Converged KVRocks infrastructure**, building a high-throughput **RAID0** array for stable deployment.
2. **Executed and stabilized** the GPU HBM $\rightarrow$ SSD KV-cache offloading pipeline with vLLM, LMCache, and KVRocks.
3. **Enhanced Python benchmarking scripts** with timeout handling for reliable metrics.
4. **Optimized RocksDB parameters and vLLM flags**, achieving **$\mathbf{1.5\times}$ TPS/RPS improvement**.
5. **Modeled HBM saturation** to calculate safe parallelism limits.
6. **Benchmarked vLLM + KVRocks vs DRAM**, confirming **$\mathbf{2.5\times}$ faster TPS/RPS** for DRAM.
7. **Synthesized performance results** into actionable insights for architecture decisions.
8. **Established best practices** and optimal configuration patterns for consistent team deployment.

---

## 📊 Performance Insights

* **Latency & Bottlenecks:** Network serialization dominates over disk I/O.
* **Chunk Size Trade-off:** Larger cache chunks reduce hit rate (77% $\rightarrow$ 69%), requiring balance.
* **Baseline Comparison:** DRAM caching outperforms SSD offloading, guiding cost-performance trade-offs.

---

## 🧠 Conclusion

This project establishes a **robust, high-throughput offloading architecture** for LLM inference, identifies system bottlenecks, and provides clear guidance for future performance research and optimization.

---
