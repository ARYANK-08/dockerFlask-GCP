# **Deploying a Flask App to GCP using Docker and CI/CD**

| **Anime Docker** 🐳 | **Website Live** 🌐 |
|:---:|:---:|
| ![Anime Docker](https://github.com/user-attachments/assets/06088f3b-dd19-4798-b7be-2f5358f179eb) | ![Website Live](https://github.com/user-attachments/assets/5130e4fd-c189-4341-80c0-a0760ddec4d0) |

### **Step 1: Create `requirements.txt`**
First, list the dependencies for your Flask application in a `requirements.txt` file:

```
Flask==2.0.3
```

### **Step 2: Create `Dockerfile`**
Next, create a `Dockerfile` to containerize your Flask application. Below is an example:

```dockerfile
FROM python:3.10-slim-buster

# Set the working directory inside the container
WORKDIR /todo-app

# Copy requirements first for caching
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip3 install -r requirements.txt

# Copy all files into the working directory
COPY . .

# Command to run the application
CMD ["python", "app.py"]
```

![image](https://github.com/user-attachments/assets/c147248e-4421-49c8-a43b-24894bfb3ae9)


### **Step 3: Update Flask App to Listen on Port 8080**
In your `app.py`, ensure your Flask app listens on port `8080`:

```python
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)  # Hardcoded port 8080
```

**Error Handling**: If the port is not configured correctly, you may encounter the following error when deploying:

```
Revision 'flaskimg-00001-nqv' is not ready and cannot serve traffic. The user-provided container failed to start and listen on the port defined provided by the PORT=8080 environment variable within the allocated timeout.
```

Ensure your app is configured to listen on port 8080, as GCP expects it.

### **Step 4: Create a New GCP Project**
Create a new project in GCP, for example, `flaskdeploydocker`. Obtain the project ID for further use.

### **Step 5: Enable Cloud Run API and Cloud Build**
You need to enable Cloud Run and Cloud Build APIs in your project. You can do this in the GCP Console, and ensure billing is enabled.

### **Step 6: Install Google Cloud CLI**
Install the `gcloud` CLI tool and initialize it:

```bash
gcloud init
gcloud config set project flaskdockerdeploy
```

![cmdgcloud](https://github.com/user-attachments/assets/553c4137-fef8-485f-a7d7-d352ec43f93f)


### **Step 7: Create Artifact Repository**
Create a Docker repository in Google Artifact Registry:

```bash
gcloud artifacts repositories create flaskdocker --repository-format=docker --location=europe-west4 --description="FlaskDockerAPP" --immutable-tags --async
```

![Screenshot 2024-12-18 233800](https://github.com/user-attachments/assets/12b36b20-0b96-42fc-8c22-38ed5a45118d)


### **Step 8: Authenticate Docker to GCP**
Authenticate Docker to GCP's Artifact Registry:

```bash
gcloud auth configure-docker europe-west4-docker.pkg.dev
```

### **Step 9: Configure IAM Permissions**
In IAM, assign the `Object Storage Viewer` permission to the service account to allow access to the Artifact Registry.

### **Step 10: Build and Push Docker Image**
Build and push the Docker image to Artifact Registry:

```bash
gcloud builds submit --tag europe-west4-docker.pkg.dev/flaskdockerdeploy/flaskdocker/flaskimg:flasktagnew
```

### **Step 11: Deploy to Cloud Run**
1. Go to the **Cloud Run** console.
2. Select **Deploy Container** -> **Service**.
3. Choose the container image from Artifact Registry.
4. **Allow unauthenticated invocations** if you want your service to be publicly accessible.


![Screenshot 2024-12-18 234639](https://github.com/user-attachments/assets/516cf816-c480-4d43-90be-ea05bfd9f7d0)

![Screenshot 2024-12-18 234413](https://github.com/user-attachments/assets/fcf142e0-170f-4309-8a92-f12d76d295cd)

### **Step 12: Set up CI/CD Pipeline with GitHub**
To automate deployments, connect your GitHub repository to GCP and set up a CI/CD pipeline using Cloud Build to push images to Artifact Registry and deploy them to Cloud Run.

![Screenshot 2024-12-19 025528](https://github.com/user-attachments/assets/a8c26d30-a2fe-4add-9658-cee918947ecd)

### Steps:
1. **Create a Service Account in GCP (if not already):**
   - Go to **IAM & Admin** > **Service Accounts**.
   - Create a new service account.
   - Grant the following roles:
     - `Artifact Registry Writer`
     - `Artifact Registry Create-on-Push Writer`
     - `Cloud Run Admin`
     - `Editor`
     - `Logs Writer`
     - `Service Account User`
     - `Storage Object Viewer`
   
2. **Create and Download Service Account Key:**
   - Go to **IAM & Admin** > **Service Accounts**.
   - Create a key for your service account.
   - Download the key as a JSON file.

3. **Add Service Account Key to GitHub Secrets:**
   - Go to your GitHub repository.
   - Navigate to **Settings** > **Secrets and Variables** > **Actions**.
   - Add a new secret called `GCP_SA_KEY` and paste the JSON key content there.

4. **Create `cicd.yaml` for GitHub Actions:**
   In your GitHub repository, create a file `.github/workflows/cicd.yaml` with the following content:

![image](https://github.com/user-attachments/assets/74b31773-0e33-49c9-acff-0805306bed5a)


### Key Points:
- **Service Account Key (`GCP_SA_KEY`)** is stored as a secret in GitHub.
- The GitHub Action triggers on every push to the `main` branch.
- It builds the Docker image and pushes it to **Google Artifact Registry**.
- Finally, it deploys the image to **Google Cloud Run**.

### Don't Forget To:
1. Replace `your-image-name`, `your-service-name`, and `your-region` with your actual values.
2. Ensure the GCP project ID is stored in GitHub secrets (`GCP_PROJECT_ID`) for better security.
3. This process will automatically deploy your updated Docker image to GCP whenever you push changes to the `main` branch.

This setup is ready to automate your CI/CD workflow with GitHub and GCP.

![Screenshot 2024-12-19 025004](https://github.com/user-attachments/assets/daa47d13-2eae-4fe9-aee7-5e07c2556f23)

---

### **Step 13: Run Locally Using Docker**
If you want to run the application locally using Docker, build and run it using the following commands:

```bash
docker build . --tag europe-west4-docker.pkg.dev/flaskdockerdeploy/flaskdocker/otherimg:othertag
docker run -p 8080:8080 europe-west4-docker.pkg.dev/flaskdockerdeploy/flaskdocker/otherimg:othertag
```

thanks maccha, hope it helps you! :)


