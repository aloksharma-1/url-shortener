# 🔗 URL Shortener – FastAPI + GKE + Cloud Build

A scalable, containerized URL shortener API built with **FastAPI**, containerized using **Docker**, and deployed to **Google Kubernetes Engine (GKE)** via **Cloud Build** and **Artifact Registry**.

---

## 📌 Overview

This project demonstrates a complete DevOps workflow on Google Cloud Platform (GCP), including:

- API built with [FastAPI](https://fastapi.tiangolo.com/)
- CI/CD pipeline with [Cloud Build](https://cloud.google.com/build)
- Container image hosted in [Artifact Registry](https://cloud.google.com/artifact-registry)
- Deployed to [Google Kubernetes Engine](https://cloud.google.com/kubernetes-engine)
- Exposed via a LoadBalancer with public access

---

## 🧱 Tech Stack

| Layer            | Technology              |
|------------------|--------------------------|
| Backend API      | Python 3.10, FastAPI      |
| Containerization | Docker                   |
| CI/CD            | Cloud Build              |
| Registry         | Artifact Registry        |
| Orchestration    | Google Kubernetes Engine |
| Deployment       | `kubectl` & YAML         |

---

## 📁 Project Structure

url-shortener/
├── main.py # FastAPI application logic
├── requirements.txt # Python dependencies
├── Dockerfile # Build definition for the app
├── cloudbuild.yaml # Cloud Build pipeline
├── deployment.yaml # Kubernetes deployment config
└── service.yaml # Kubernetes service (LoadBalancer)

yaml
Copy
Edit

---

## 🚀 Getting Started

### ✅ Prerequisites

Ensure the following tools are installed and configured:

- Python 3.10+
- Docker
- [Google Cloud SDK](https://cloud.google.com/sdk)
- `kubectl`
- GCP project with billing enabled

---

## 🔧 Setup & Deployment

### 1. Set Your Project & Zone

```bash
gcloud config set project vibrant-keyword-460710-a5
gcloud config set compute/zone us-central1-a
2. Enable Required APIs
bash
Copy
Edit
gcloud services enable \
  container.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com
3. Create Artifact Registry (if not exists)
bash
Copy
Edit
gcloud artifacts repositories create url-shortener-repo \
  --repository-format=docker \
  --location=us-central1 \
  --description="Docker repo for URL Shortener"
🛠️ Build and Push with Cloud Build
cloudbuild.yaml
yaml
Copy
Edit
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'us-central1-docker.pkg.dev/vibrant-keyword-460710-a5/url-shortener-repo/url-shortener', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'us-central1-docker.pkg.dev/vibrant-keyword-460710-a5/url-shortener-repo/url-shortener']

images:
  - 'us-central1-docker.pkg.dev/vibrant-keyword-460710-a5/url-shortener-repo/url-shortener'

options:
  logging: CLOUD_LOGGING_ONLY
Submit Build
bash
Copy
Edit
gcloud builds submit --config cloudbuild.yaml .
☸️ Deploy to GKE
1. Create a Kubernetes Cluster
bash
Copy
Edit
gcloud container clusters create url-shortener-cluster \
  --num-nodes=1 \
  --enable-ip-alias
2. Authenticate kubectl with Cluster
bash
Copy
Edit
gcloud container clusters get-credentials url-shortener-cluster
3. Deploy Application
bash
Copy
Edit
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
4. Get External IP
bash
Copy
Edit
kubectl get service url-shortener-service
Visit http://<EXTERNAL-IP> in your browser once the LoadBalancer is provisioned.

🧪 Example API Usage
Shorten a URL
http
Copy
Edit
POST /shorten
Content-Type: application/json

{
  "long_url": "https://example.com"
}
Redirect
http
Copy
Edit
GET /<short_code>
🧹 Cleanup Resources
bash
Copy
Edit
gcloud container clusters delete url-shortener-cluster
Optionally delete the Artifact Registry repo:

bash
Copy
Edit
gcloud artifacts repositories delete url-shortener-repo --location=us-central1
📜 License
Licensed under the MIT License.

👤 Author
Developed by Your Name
Email: your.email@example.com

yaml
Copy
Edit

---

### ✅ Suggestions:
- Rename `url-shortener-repo`, `vibrant-keyword-460710-a5`, and links as needed for your own project.
- You can add a `LICENSE` and `.gitignore` file to complete the professional setup.

Let me know if you want me to export this as a file or help create deployment/service YAML files!
