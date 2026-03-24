```
██████╗  █████╗ ████████╗ █████╗     ██████╗ ██╗██████╗ ███████╗██╗     ██╗███╗   ██╗███████╗
██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗    ██╔══██╗██║██╔══██╗██╔════╝██║     ██║████╗  ██║██╔════╝
██║  ██║███████║   ██║   ███████║    ██████╔╝██║██████╔╝█████╗  ██║     ██║██╔██╗ ██║█████╗  
██║  ██║██╔══██║   ██║   ██╔══██║    ██╔═══╝ ██║██╔═══╝ ██╔══╝  ██║     ██║██║╚██╗██║██╔══╝  
██████╔╝██║  ██║   ██║   ██║  ██║    ██║     ██║██║     ███████╗███████╗██║██║ ╚████║███████╗
╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝    ╚═╝     ╚═╝╚═╝     ╚══════╝╚══════╝╚═╝╚═╝  ╚═══╝╚══════╝
```

<div align="center">

# 🚀 AWS Data Ingestion Pipeline
### S3 → RDS (MySQL) with AWS Glue Fallback | Dockerized Python Application

---

![Python](https://img.shields.io/badge/Python-3.9-blue?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-Cloud-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)
![RDS](https://img.shields.io/badge/Amazon_RDS-MySQL-527FFF?style=for-the-badge&logo=amazonrds&logoColor=white)
![S3](https://img.shields.io/badge/Amazon_S3-Storage-569A31?style=for-the-badge&logo=amazons3&logoColor=white)
![Glue](https://img.shields.io/badge/AWS_Glue-Fallback-8C4FFF?style=for-the-badge&logo=amazonaws&logoColor=white)

**Author:** Arkan Tandel &nbsp;|&nbsp; **Batch:** 28 July &nbsp;|&nbsp; **Course:** MCA &nbsp;|&nbsp; **Organization:** Fortune Cloud Technologies

</div>

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Architecture Diagram](#-architecture-diagram)
- [Project Structure](#-project-structure)
- [AWS Services Used](#-aws-services-used)
- [Step-by-Step Setup Guide](#-step-by-step-setup-guide)
- [Running the Project](#-running-the-project)
- [Output / Results](#-output--results)
- [Challenges & Solutions](#-challenges--solutions)

---

## 📖 Overview

This project builds a **fault-tolerant, cloud-native data pipeline** using AWS services and Docker.

The pipeline does the following automatically:

> 📥 **Reads** a CSV file stored in **Amazon S3**  
> 📤 **Inserts** the data into **Amazon RDS (MySQL)** database  
> ⚠️ **Falls back** to **AWS Glue Data Catalog** if RDS is unavailable  
> 🐳 Everything runs inside a **Docker container** — portable and consistent

This simulates a real-world DevOps/Cloud scenario where data must always be ingested — even when the primary database is down.

---

## 🏗️ Architecture Diagram

```
╔══════════════════════════════════════════════════════════════════════════════════╗
║                        AWS DATA INGESTION PIPELINE                             ║
║                         Arkan Tandel | 28 July Batch                           ║
╚══════════════════════════════════════════════════════════════════════════════════╝

  ┌─────────────────┐
  │   sample_data   │
  │     .csv file   │
  └────────┬────────┘
           │  upload
           ▼
  ┌─────────────────────────────────────┐
  │          AMAZON S3 BUCKET           │
  │   📦 my--data-pipeline-bucket       │
  │   📄 data.csv  ←── stored here      │
  └────────┬────────────────────────────┘
           │
           │  boto3.get_object()
           │  reads CSV via pandas
           ▼
  ╔═════════════════════════════════════╗
  ║       🐳 DOCKER CONTAINER           ║
  ║   ┌─────────────────────────────┐   ║
  ║   │        app.py               │   ║
  ║   │  1. read_from_s3()          │   ║
  ║   │  2. upload_to_rds()  ──┐    │   ║
  ║   │  3. fallback_to_glue() │    │   ║
  ║   └────────────────────────┼────┘   ║
  ║   Python 3.9 | boto3       │        ║
  ║   pandas | sqlalchemy      │        ║
  ╚═══════════════════════════╪═════════╝
                              │
             ┌────────────────┴──────────────────┐
             │                                   │
             │ ✅ RDS Available?                  │ ❌ RDS Fails?
             ▼                                   ▼
  ┌──────────────────────┐          ┌──────────────────────────┐
  │   AMAZON RDS MySQL   │          │      AWS GLUE CATALOG    │
  │ ┌──────────────────┐ │          │  ┌─────────────────────┐ │
  │ │ Database: testdb │ │          │  │ Database: my_glue_db│ │
  │ │ Table: mytable   │ │          │  │ Table: my_glue_table│ │
  │ │ ──────────────── │ │          │  │ Location: S3 path   │ │
  │ │ id | name | age  │ │          │  │ Type: EXTERNAL_TABLE│ │
  │ │  1 | Arkan| 22   │ │          │  └─────────────────────┘ │
  │ │  2 | Rahul| 25   │ │          │                          │
  │ │  3 | Amit | 28   │ │          │  Points back to S3 ✅    │
  │ └──────────────────┘ │          └──────────────────────────┘
  └──────────────────────┘
        ✅ PRIMARY PATH                    ⚡ FALLBACK PATH
      Data inserted into DB             Dataset registered in Glue

═══════════════════════════════════════════════════════════════════════════
  RESULT:   ✅ Data read from S3    +    ✅ Data inserted into RDS
═══════════════════════════════════════════════════════════════════════════
```

---

## 📁 Project Structure

```
aws-pipeline/
│
├── 🐍 app.py                  ← Main Python script (core logic)
│   ├── read_from_s3()         │   Reads CSV from S3 using boto3
│   ├── upload_to_rds()        │   Inserts data into RDS MySQL
│   └── fallback_to_glue()     │   Creates Glue table if RDS fails
│
├── 🐳 Dockerfile              ← Container configuration
│   ├── FROM python:3.9        │   Base image
│   ├── COPY requirements.txt  │   Install dependencies
│   └── CMD python app.py      │   Run on container start
│
├── 📦 requirements.txt        ← Python dependencies
│   ├── boto3                  │   AWS SDK
│   ├── pandas                 │   CSV parsing
│   ├── sqlalchemy             │   Database ORM
│   ├── pymysql                │   MySQL driver
│   └── cryptography           │   Secure connections
│
├── 📄 sample_data.csv         ← Test dataset uploaded to S3
│   └── id, name, age
│
└── 📘 README.md               ← This file
```

---

## ☁️ AWS Services Used

| Service | Icon | Purpose |
|---------|------|---------|
| **Amazon S3** | 📦 | Stores source CSV file — acts as the data source |
| **Amazon RDS (MySQL)** | 🗄️ | Primary database where data gets inserted |
| **AWS Glue** | 🔗 | Fallback — registers the dataset if RDS is down |
| **AWS EC2 (Ubuntu)** | 💻 | Server where Docker container is run |
| **Docker** | 🐳 | Packages the app for consistent, portable deployment |

---

## 🛠️ Step-by-Step Setup Guide

### ✅ Step 1 — Create an S3 Bucket and Upload CSV

```
AWS Console → S3 → Create Bucket
Bucket Name : my--data-pipeline-bucket
Region      : us-east-1
```

Upload `sample_data.csv` to the bucket.

```csv
id,name,age
1,Arkan,22
2,Rahul,25
3,Amit,28
```

> 💡 **Why?** S3 acts as the source of truth for our data. The Python app will read this file.

---

### ✅ Step 2 — Launch RDS MySQL Instance

```
AWS Console → RDS → Create Database
Engine      : MySQL
Template    : Free Tier
DB Name     : testdb
Username    : admin
Password    : your-password
Public      : Yes (for testing)
```

Note down the **endpoint URL** — you'll need it later.

> 💡 **Why?** RDS is our primary destination. All CSV data will be inserted here as a table.

---

### ✅ Step 3 — Create AWS Glue Database

```
AWS Console → Glue → Databases → Add Database
Name : my_glue_db
```

> 💡 **Why?** Glue is the fallback. If RDS fails, the app creates a table here pointing to the S3 data.

---

### ✅ Step 4 — Launch EC2 Ubuntu Instance

```
AWS Console → EC2 → Launch Instance
OS     : Ubuntu 22.04
Type   : t2.micro (Free Tier)
Key    : Create or use existing .pem key
```

SSH into the instance:
```bash
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

---

### ✅ Step 5 — Install Docker on EC2

```bash
sudo apt update
sudo apt install docker.io -y
sudo usermod -aG docker ubuntu
newgrp docker
docker --version
```

> 💡 **Why?** Docker lets us run our app in an isolated container without worrying about the host environment.

---

### ✅ Step 6 — Clone the Project

```bash
git clone https://github.com/YOUR_USERNAME/aws-pipeline.git
cd aws-pipeline
```

Or manually create the files:
```bash
mkdir aws-pipeline && cd aws-pipeline
nano app.py         # paste the Python script
nano Dockerfile     # paste the Dockerfile
nano requirements.txt
```

---

### ✅ Step 7 — Build the Docker Image

```bash
docker build -t data-pipeline .
```

What this does:
```
[1/3] Pull python:3.9 base image from Docker Hub
[2/3] Install all packages from requirements.txt
[3/3] Copy app.py into the container
→ Image "data-pipeline" is ready ✅
```

> 💡 **Why?** Building creates a self-contained image with Python + all libraries bundled in.

---

### ✅ Step 8 — Run the Docker Container

```bash
docker run \
  -e AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY \
  -e AWS_SECRET_ACCESS_KEY=YOUR_SECRET_KEY \
  -e AWS_DEFAULT_REGION=us-east-1 \
  -e S3_BUCKET=my--data-pipeline-bucket \
  -e S3_KEY=data.csv \
  -e RDS_HOST=your-rds-endpoint.rds.amazonaws.com \
  -e RDS_USER=admin \
  -e RDS_PASSWORD=your-password \
  -e RDS_DB=testdb \
  -e RDS_TABLE=mytable \
  -e GLUE_DB=my_glue_db \
  -e GLUE_TABLE=my_glue_table \
  -e GLUE_S3_PATH=s3://my--data-pipeline-bucket/ \
  data-pipeline
```

> 💡 **Why env variables?** Credentials are never hardcoded. This is a security best practice in DevOps.

---

## ▶️ Running the Project

**Expected output when RDS is available (Primary Path):**
```
✅ Data read from S3
✅ Data inserted into RDS
```

**Expected output when RDS is unavailable (Fallback Path):**
```
✅ Data read from S3
❌ RDS Failed: connection error...
⚠️ Falling back to AWS Glue...
✅ Glue Table Created
```

---

## 📸 Output / Results

### Docker Execution (Successful RDS Insert)

The container ran on AWS EC2 and produced the following output:

```
ubuntu@ip-172-31-30-219:~/aws-pipeline$ docker run [env vars] data-pipeline

✅ Data read from S3
✅ Data inserted into RDS
```

Both primary steps completed successfully — data was read from S3 and written to the RDS MySQL table.

---

## ⚡ Challenges & Solutions

| # | Challenge | Solution |
|---|-----------|----------|
| 1 | Passing AWS credentials securely into Docker | Used `-e` environment variables at runtime. Nothing is hardcoded in the image. |
| 2 | RDS not accessible from Docker container | Opened port 3306 in the RDS Security Group for the EC2 instance IP |
| 3 | Glue fallback only triggering when needed | Wrapped RDS code in `try/except` — Glue is only called if an exception is raised |
| 4 | Dependency issues inside container | Listed all packages in `requirements.txt` and used `pip install -r` in Dockerfile |

---

<div align="center">

---

Made with ☁️ by **Arkan Tandel** &nbsp;|&nbsp; 28 July Batch &nbsp;|&nbsp; MCA Internship &nbsp;|&nbsp; Fortune Cloud Technologies

</div>
