# 🚀 Hyper-Converged KV-Cache Offloading for Cost-Efficient LLM Inference

## 📜 Description

This project focused on **System Architecture and Performance Engineering** for Large Language Model (LLM) inference, specifically addressing the costly memory constraints of GPU High Bandwidth Memory (HBM). We designed, provisioned, and benchmarked a **Hyper-Converged KV-Cache Offloading pipeline** utilizing vLLM, LMCache, and the **KVRocks** key-value store. The core goal was to establish the optimal technical stack and performance baselines necessary to guide next-generation deployment strategies for high-throughput architectures like **Dynamo** and **LLMD**.

## 🛠️ Technology Stack & Environment

| Component | Purpose | Details |
| :--- | :--- | :--- |
| **LLM Framework** | vLLM (Continuous Batching) | Used for high-throughput inference serving. |
| **Cache Offloading** | LMCache + **KVRocks** | LMCache managed the offloading logic; KVRocks provided robust, fast key-value persistence. |
| **Hardware** | NVIDIA GPUs (L4/A100), Dual NVMe SSDs | Target environment included setting up **RAID0** arrays on NVMe SSDs for maximized I/O bandwidth. |
| **Tools & Optimization** | Python Benchmarking (Custom Script), RocksDB | Custom Python script enhanced for accuracy; RocksDB/vLLM flags tuned for $1.5\times$ improvement. |

---

## 🎯 Key Achievements & Impact

| Achievement | Technical Detail | Performance KPI |
| :--- | :--- | :--- |
| **Infrastructure Foundation** | Provisioned the robust, Hyper-Converged **KVRocks** setup and built the high-throughput **RAID0** array. | Provided the stability required for **Dynamo and LLMD deployments**. |
| **Pipeline Stabilization** | Executed and stabilized the seamless GPU HBM $\rightarrow$ SSD KV-cache offloading pipeline integration. | Enabled consistent execution across the full technical stack. |
| **System Optimization** | Optimized RocksDB parameters and **vLLM flags** via **System-Level Tuning**. | Achieved an overall **$\mathbf{1.5\times}$ improvement in TPS/RPS** of the KVrocks pipeline. |
| **Performance Baseline** | Conducted full benchmarking comparing the final **KVRocks** (SSD) configuration against DRAM caching. | Identified DRAM as approximately **$\mathbf{2.5\times}$ faster in TPS/RPS**, providing clear cost-performance trade-offs. |

---

## 📝 Detailed Responsibilities (8 Points)

1.  **Provisioned the foundational, robust Hyper-Converged KVRocks infrastructure** by building a high-throughput **RAID0** array. This configuration **provided the stability required for Dynamo and LLMD deployments**.
2.  **Executed and stabilized** the seamless GPU HBM $\rightarrow$ SSD KV-cache offloading pipeline, integrating vLLM, LMCache, and KVRocks.
3.  **Enhanced the Python benchmarking script** by implementing timeout exception handling to filter data skew and ensure accurate TPS metrics.
4.  Optimized core RocksDB parameters (compression, block cache) and vLLM flags through system-level tuning, resulting in an overall **$\mathbf{1.5\times}$ improvement in TPS/RPS**.
5.  **Calculated precise concurrency limits** by modeling HBM saturation relative to token size, determining the maximum number of parallel clients for the vLLM server.
6.  **Conducted full benchmarking** of vLLM + **KVRocks** (SSD) vs. DRAM caching, identifying DRAM as approximately **$\mathbf{2.5\times}$ faster in TPS/RPS** than the SSD configuration.
7.  **Synthesized benchmark data into performance graphs**, identifying network serialization as the dominant bottleneck and providing actionable architectural insights.
8.  **Established optimal configuration patterns and best practices for the vLLM + LMCache + KVRocks stack, enabling consistent system stability and performance across team deployments.**

---

## 🧠 Conclusion & Future Direction

The project successfully defined the technical limits and opportunities within the Hyper-Converged offloading architecture. The primary architectural insight provided was that **network serialization** remains the dominant bottleneck, guiding future research toward network/communication optimization rather than solely storage tuning.

---
