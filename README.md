# 🚀 Hyper-Converged KV-Cache Offloading for Cost-Efficient LLM Inference

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Tech Stack](https://img.shields.io/badge/Stack-vLLM%20%7C%20Kvrocks%20%7C%20LMCache-green)]()
[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)](https://www.python.org/)

## 📖 Overview

This project explores **System Architecture and Performance Engineering** for Large Language Model (LLM) inference, addressing the high cost and limited capacity of GPU High Bandwidth Memory (HBM). It delivers a **Hyper-Converged KV-Cache Offloading pipeline** leveraging **vLLM**, **LMCache**, and **Kvrocks** to redirect KV-cache data from GPU memory to high-throughput SSDs.

## ⚠️ Project Status & IP Notice

> **Type:** Research Documentation & Portfolio Artifact  
> **Status:** Completed PoC (Internal)

This repository serves as **documentation** for a research project conducted at **Pliops**.
Due to Intellectual Property (IP) restrictions, the full source code and proprietary benchmarking tools are not publicly available. This repository provides:
* High-level **System Architecture**.
* **Infrastructure Configuration** (IaC patterns).
* **Performance Analysis** and research methodology.
  
### 🎯 Project Goals
* **Design and implement** a robust PoC for LLM inference offloading.
* **Evaluate performance and cost-efficiency** of two architectures:
    * **Baseline:** DRAM-bound KV-Cache serving.
    * **Proposed:** SSD-based KV-Cache Offloading via Hyper-Converged Architecture.

---

## 🛠️ Technology Stack & Environment

| Component | Purpose | Details |
|-----------|---------|---------|
| **LLM Framework** | High-throughput inference | **vLLM** (Continuous Batching) |
| **Cache Offloading** | KV flow management | **LMCache** + **Kvrocks** |
| **Hardware** | Compute & Storage | NVIDIA GPUs, **Dual NVMe SSDs (RAID0)** |
| **Optimization** | Tuning | RocksDB compaction, vLLM flags |

---

## ⚡ Key Achievements

* **Infrastructure Foundation:** Provisioned a robust Hyper-Converged Kvrocks setup on a **RAID0 NVMe SSD array**, ensuring stability for high-throughput deployments.
* **System Optimization:** Tuned core RocksDB parameters and vLLM flags, resulting in a **1.5× improvement** in TPS/RPS (Transactions/Requests Per Second).
* **Performance Baseline:** Quantified DRAM caching as approx. **2.5× faster** than the SSD configuration, providing critical data for cost-performance trade-off decisions.
* **Architectural Insight:** Identified **network serialization** as the dominant bottleneck rather than disk I/O.

---

## 📋 Prerequisites

### Hardware Requirements
- NVIDIA GPU (L4/A100 or equivalent)
- Dual NVMe SSDs (for RAID0 configuration)
- Minimum 64GB system RAM

### Software Requirements
- Python 3.10+
- CUDA 11.8+
- vLLM 0.x.x
- RocksDB 7.x (via Kvrocks)
- Linux kernel with RAID support

### System Setup
```bash
# Create RAID0 array (example)
sudo mdadm --create /dev/md0 --level=0 --raid-devices=2 /dev/nvme0n1 /dev/nvme1n1

# Format and mount
sudo mkfs.xfs /dev/md0
sudo mount -o noatime /dev/md0 /mnt/nvme_raid
```

---

## 🏗️ Architecture & Installation

This section details the **Single-Node** architecture optimized for speed and simplicity.

```mermaid
graph LR
    A[User Request] --> B(vLLM Inference Engine)
    B -- KV-Cache Data --> C{LMCache Connector}
    C -- Redis Protocol --> D[Kvrocks Database]
    D -- Persist --> E[(Local NVMe SSD)]
```

### 1. Build and Run Kvrocks

Kvrocks is used as the storage engine. We build it from source to ensure optimal performance.

```bash
# Clone and Build
git clone https://github.com/apache/kvrocks.git
cd kvrocks
./x.py build -DENABLE_LUA=ON

# Run Kvrocks
# Ensure your kvrocks.conf points 'dir' to your SSD mount point
./build/kvrocks -c configs/kvrocks.conf
```

**Key Configuration (`configs/kvrocks.conf`):**

```ini
bind 0.0.0.0
port 6666
dir /mnt/nvme_raid/kvrocks_data  # Pointing to fast storage
daemonize yes
```

### 2. Connect vLLM to Kvrocks

Configure vLLM to offload cache to the local Kvrocks instance using LMCache.

**Configuration (`configs/lmcache_kvrocks.yaml`):**

```yaml
chunk_size: 1024
remote_url: "redis://127.0.0.1:6666"
kv_connector: "LMCacheConnectorV1"
kv_role: "kv_both"
```

### 🔧 Key Optimization Parameters

To achieve the **1.5× performance improvement**, specific tuning was applied:

**RocksDB Configuration:**
```ini
# Additional tuning in kvrocks.conf
rocksdb.compression = lz4
rocksdb.write_buffer_size = 268435456  # 256MB - optimized for large KV chunks
rocksdb.max_background_jobs = 8        # parallel compaction for higher throughput
rocksdb.block_cache_size = 8589934592  # 8GB - aggressive caching
```

**vLLM Launch Flags:**
```bash
vllm serve meta-llama/Llama-3-8B \
  --gpu-memory-utilization 0.9 \
  --max-num-seqs 256 \
  --enable-prefix-caching \
  --kv-cache-dtype auto
```

**Storage Configuration:**
- **RAID Level:** RAID0 (striping for maximum throughput)
- **Filesystem:** XFS with `noatime` mount option
- **I/O Scheduler:** `none` (for NVMe devices)

---

## 📈 Performance Visualization

> **Note:** The graphs below illustrate the performance delta and optimization impact.

### Figure 1: DRAM vs Kvrocks Initial Benchmark
![DRAM vs Kvrocks Benchmark](assets/dram_vs_kvrocks.png)
*Blue line: DRAM | Pink line: Kvrocks — Illustrates the 2.5× TPS difference.*

<br>

### Figure 2: Kvrocks Optimization (Before vs. After Tuning)
![Kvrocks Optimization](assets/optimization_tuning.png)
*Purple line: Baseline | Pink line: Tuned — Highlights the 1.5× improvement.*

---

## 📊 Performance Insights

1. **Latency & Bottlenecks:** Network serialization dominates over disk I/O - optimization focus should be on protocol efficiency.
2. **Chunk Size Trade-off:** Larger cache chunks reduce hit rate (77% → 69%), requiring careful balance between memory efficiency and cache effectiveness.
3. **Baseline Comparison:** DRAM caching outperforms SSD offloading by 2.5×, but at 3.75× higher memory cost - critical for cost-performance trade-off analysis.
4. **Throughput vs Cost:** SSD offloading enables 3-4× more concurrent users per GPU compared to DRAM-only configurations.

---

## 📝 Disclaimer

The benchmarking code, internal datasets, and specific proprietary performance metrics are **Intellectual Property (IP) of Pliops** and are not included in this repository. This repository serves as a reference implementation for the open-source infrastructure setup.

---

## 📧 Contact

Created by **Nechama Krashinski** as part of research at Pliops.  
Questions or collaboration? Feel free to open an issue or reach out!

---

## 🙌 Acknowledgments

* **Pliops** for the mentorship and resources.
* **KamaTech** for the bootcamp platform.
* **vLLM**, **LMCache**, and **Kvrocks** communities for their excellent open-source tools.

