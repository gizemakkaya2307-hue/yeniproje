# Docker + Ansible + CI/CD ile Web Uygulamasi Dagitimi

Bu proje, `main` branch'ine push yapildiginda Flask uygulamasini Docker image olarak build eder, Docker Hub'a push eder ve Ansible ile uzak sunucuda container olarak calistirir.

## Proje Yapisi

```text
.
+-- app/
|   +-- app.py
|   +-- requirements.txt
+-- ansible/
|   +-- inventory.ini
|   +-- deploy.yml
+-- .github/workflows/
|   +-- ci-cd.yml
+-- Dockerfile
+-- .dockerignore
```

## Lokal Calistirma

```bash
docker build -t myapp:local .
docker run --rm -p 5000:5000 myapp:local
```

Tarayicida `http://localhost:5000` adresini acin.

## GitHub Secrets

Repository settings icinde `Settings > Secrets and variables > Actions` bolumune su secret'lari ekleyin:

```text
DOCKER_USER
DOCKER_PASS
SERVER_HOST
SERVER_USER
SSH_KEY
```

`SERVER_USER` genellikle Ubuntu sunucular icin `ubuntu` olur. `SSH_KEY`, sunucuya baglanabilen private key icerigidir.

## Deploy Akisi

1. Developer kodu `main` branch'ine push eder.
2. GitHub Actions Docker image build eder.
3. Image Docker Hub'a push edilir.
4. GitHub Actions gecici Ansible inventory dosyasi olusturur.
5. Ansible uzak sunucuda Docker'i kurar/baslatir.
6. Eski container silinir ve yeni image ile container calistirilir.
