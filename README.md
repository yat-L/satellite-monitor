# Satellite Monitor 📡

**Satellite Monitor** is a data engineering and analytics project designed to ingest, transform, and analyze real-time telemetry from NASA's Deep Space Network (DSN).

This project moves beyond simple "live status" checks by archiving transient XML streams into a structured **AWS Data Lakehouse**. This enables historical analysis of signal degradation, antenna utilization, and the efficiency of deep-space communication protocols.

---

## 📖 Table of Contents

* [Project Overview](https://www.google.com/search?q=%23-project-overview)
* [Architecture](https://www.google.com/search?q=%23-architecture)
* [Data Model](https://www.google.com/search?q=%23-data-model)
* [Repository Structure](https://www.google.com/search?q=%23-repository-structure)
* [Getting Started](https://www.google.com/search?q=%23-getting-started)
* [Analytics & Insights](https://www.google.com/search?q=%23-analytics--insights)

---

## 🔭 Project Overview

NASA's DSN operates 24/7, generating valuable data about the physics of the solar system and the health of our spacecraft. However, the public feed is ephemeral (real-time only).

**Satellite Monitor** solves this by:

1. **Extracting** live XML data every 5 seconds.
2. **Loading** raw data into an immutable Data Lake (S3 Bronze Layer).
3. **Transforming** data into a Kimball Dimensional Model (Gold Layer).
4. **Analyzing** long-term trends in X-Band vs. Ka-Band performance, weather impacts, and mission latency.

---

## 🏗 Architecture

The project follows a **Medallion Architecture (Lakehouse)** pattern using AWS services.

| Layer | Storage | Description |
| --- | --- | --- |
| **Bronze (Raw)** | AWS S3 | Raw XML files partitioned by `YYYY/MM/DD`. Immutable and full fidelity. |
| **Gold (Curated)** | Data Warehouse | Dimensional Model (Star Schema) ready for BI tools (Tableau/PowerBI). |

---

## 📊 Data Model

The core analytics engine relies on a **Kimball Star Schema**. This design minimizes join complexity and maximizes query performance for time-series analysis.

### Fact Table: `Fact_Communication_Link`

*Granularity: One row per heartbeat per antenna-spacecraft link.*

| Metric | Description |
| --- | --- |
| `Signal_Power_dBm` | Received signal strength (e.g., -150.5 dBm). |
| `SNR_dB` | Signal-to-Noise Ratio (Data quality metric). |
| `Data_Rate_kbps` | Current telemetry throughput. |
| `RTLT_Sec` | Round-Trip Light Time (Latency). |

### Dimensions

* **`Dim_Spacecraft`**: Attributes of the asset (e.g., Voyager 2, Perseverance, Mission Type).
* **`Dim_Antenna`**: Ground station metadata (e.g., DSS-14, 70m Diameter, Goldstone Complex).
* **`Dim_Frequency_Band`**: Spectrum details (S, X, Ka, Optical).
* **`Dim_Time`**: Standard temporal axis with day/night cycles.

---

## 📈 Analytics & Insights

Once the data is modeled, we can answer questions such as:

1. **Efficiency Frontier Analysis:**
> "How much data rate is lost per Astronomical Unit (AU) of distance?"


2. **Atmospheric Sensitivity:**
> "Correlating `SNR_dB` drops with local weather at the Canberra Deep Space Communication Complex."


3. **Network Capacity Planning:**
> "Identifying contention windows where 70m antenna demand exceeds availability."



---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.

*Data Source: NASA Eyes on the Deep Space Network (Public XML Feed).*
