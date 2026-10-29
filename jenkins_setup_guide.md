# Jenkins Installation & Configuration Guide (Steps 5, 6, 7)

This guide documents the exact procedure for installing, configuring, and running Jenkins to execute the MLOps POE CI/CD pipeline.

---

## 1. Step 5: Install & Configure Jenkins

You can run Jenkins using **Method A (Docker - Recommended)** or **Method B (Homebrew / Native)**.

### Method A: Running Jenkins via Docker (Recommended & Isolated)

1. **Pull and Run Jenkins LTS image with Docker socket access**:
   ```bash
   docker run -d \
     --name jenkins \
     -p 8080:8080 \
     -p 50000:50000 \
     -v jenkins_home:/var/jenkins_home \
     -v /var/run/docker.sock:/var/run/docker.sock \
     jenkins/jenkins:lts
   ```

2. **Retrieve the Initial Admin Password**:
   ```bash
   docker exec -it jenkins cat /var/jenkins_home/secrets/initialAdminPassword
   ```

---

### Method B: Native Installation on macOS (Homebrew)

1. **Install Jenkins LTS via Brew**:
   ```bash
   brew install jenkins-lts
   ```

2. **Start the Jenkins service**:
   ```bash
   brew services start jenkins-lts
   ```
   *(Or run manually in foreground: `jenkins-lts`)*

3. **Retrieve initial administrator password**:
   ```bash
   cat ~/.jenkins/secrets/initialAdminPassword
   ```

---

## 2. Initial Setup Wizard (Web UI)

1. Open your browser and navigate to: **`http://localhost:8080`**
2. Paste the administrator password retrieved above and click **Continue**.
3. Select **"Install suggested plugins"** (this automatically installs Git, Pipeline, Workspace Cleanup, and SSH plugins).
4. Create the First Admin User:
   - **Username**: `admin`
   - **Password**: `admin123` (or your choice)
   - **Full Name**: `MLOps Team`
   - **E-mail**: `team@mlops.local`
5. Confirm Jenkins URL as `http://localhost:8080/` and click **Save and Finish**.

---

## 3. Step 6: Configure Jenkins to Pull Code from GitHub

1. **Install Required Plugins** (if not already installed):
   - Navigate to: `Manage Jenkins` > `Plugins` > `Available Plugins`
   - Ensure the following plugins are active:
     - *Git plugin*
     - *Pipeline*
     - *Docker Pipeline*

2. **Create a New Pipeline Job**:
   - On the Jenkins Dashboard, click **New Item**.
   - Enter job name: `mlops-internal-poe-pipeline`.
   - Select **Pipeline** and click **OK**.

3. **Configure Source Code Management (SCM)**:
   - Scroll down to the **Pipeline** section.
   - Change **Definition** from *Pipeline script* to:
     `Pipeline script from SCM`
   - **SCM**: Select `Git`
   - **Repository URL**: Enter your GitHub repository URL:
     `https://github.com/ShivPardeshi/MLDev-Ops-POE.git`
   - **Credentials**:
     - For public repositories, leave as *None*.
     - For private repositories, click **Add > Jenkins** and provide your GitHub Personal Access Token (PAT).
   - **Branch Specifier**: `*/main` (or `*/master`)
   - **Script Path**: `Jenkinsfile`
   - Click **Save**.

---

## 4. Step 7: Run Jenkins Job

1. From the job page (`http://localhost:8080/job/mlops-internal-poe-pipeline/`), click **Build Now** on the left menu.
2. Under **Build History**, click on `#1` (the running build).
3. Click **Console Output** to monitor real-time execution:
   - Jenkins clones your GitHub repository.
   - Sets up Python virtual environment and installs dependencies.
   - Executes pytest and prints test outputs.
   - Builds lightweight Docker container (`python:3.11-alpine`).
   - Executes `hello.py` inside Docker.
   - Runs `evidently_monitor.py` and archives the reports.
4. **Stage View** will display all green checkmarks:
   - `[✓] Checkout SCM`
   - `[✓] Install Dependencies`
   - `[✓] Run Pytest`
   - `[✓] Docker Build`
   - `[✓] Docker Run`
   - `[✓] Evidently AI Monitoring`
