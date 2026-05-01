# Docker + Ansible + CI/CD ile Otomatik Gorev Takip Uygulamasi Dagitimi

## Proje Adi

Docker + Ansible + CI/CD ile Otomatik Gorev Takip Uygulamasi Dagitimi

## Proje Amaci

Bu proje, Flask tabanli basit bir web uygulamasinin Docker ile container haline getirilmesini, GitHub Actions ile Docker image build/push yapilmasini ve Ansible ile Ubuntu Server VM'e deploy edilmesini gosterir.

Bu projede iki ayri ortam vardir:

- GitHub Actions: Docker image build eder ve Docker Hub'a push eder.
- Local VirtualBox Ubuntu VM: Ansible ile local demo deploy icin kullanilir.

## Genel Mimari

```text
Kod -> GitHub -> GitHub Actions -> Docker Hub
                                  |
                                  +-> Local demo: Ansible -> Ubuntu VM -> Docker Container
```

Not: GitHub Actions, kullanicinin bilgisayarindaki VirtualBox VM'e dogrudan baglanamaz. Bu nedenle Ansible deploy local demo olarak calistirilir.

## Kullanilan Teknolojiler

- Python 3.10
- Flask
- Docker
- Docker Hub
- Ansible
- GitHub Actions
- Ubuntu Server VM
- VirtualBox NAT ve port forwarding

## Klasor Yapisi

```text
project/
+-- app/
|   +-- app.py
|   +-- requirements.txt
+-- Dockerfile
+-- .dockerignore
+-- ansible/
|   +-- inventory.ini
|   +-- deploy.yml
+-- .github/
|   +-- workflows/
|       +-- ci-cd.yml
+-- scripts/
|   +-- local-deploy.sh
+-- README.md
```

## Local Docker Test

Image build:

```bash
docker build -t myapp:local .
```

Container calistirma:

```bash
docker run --rm -p 5050:5000 --name myapp-local myapp:local
```

Tarayicida:

```text
http://127.0.0.1:5050
```

Health endpoint:

```text
http://127.0.0.1:5050/health
```

Beklenen JSON:

```json
{"service":"myapp","status":"ok"}
```

## Docker Hub Secrets

GitHub reposunda su secret'lar bulunmalidir:

```text
DOCKER_USER
DOCKER_PASS
SERVER_HOST
SERVER_USER
SSH_KEY
```

Bu projede GitHub Actions icin zorunlu olanlar:

- `DOCKER_USER`: Docker Hub kullanici adi.
- `DOCKER_PASS`: Docker Hub sifresi veya access token.

Local VM bilgileri dokumantasyon ve local deploy icindir:

- `SERVER_HOST`: `127.0.0.1`
- `SERVER_USER`: `gizem`
- `SSH_KEY`: Ubuntu VM'e baglanan private SSH key.

## Ubuntu VM Bilgileri

VirtualBox Ubuntu VM bilgileri:

```text
SERVER_HOST = 127.0.0.1
SERVER_USER = gizem
SSH_PORT = 2222
VM ic IP = 10.0.2.15
Ubuntu kullanici adi = gizem
```

Inventory dosyasi:

```ini
[web]
localvm ansible_host=127.0.0.1 ansible_port=2222 ansible_user=gizem ansible_connection=ssh
```

## SSH Baglantisi

Windows host uzerinden Ubuntu VM'e SSH testi:

```bash
ssh -p 2222 gizem@127.0.0.1
```

Bu baglanti basariliysa Windows host, VirtualBox port forwarding ile VM'e ulasabiliyor demektir.

## GitHub Actions CI/CD Akisi

Workflow dosyasi:

```text
.github/workflows/ci-cd.yml
```

`main` branch'e push yapilinca su islemler otomatik calisir:

1. Repository checkout edilir.
2. Docker Hub'a `DOCKER_USER` ve `DOCKER_PASS` secret'lari ile login olunur.
3. Docker image build edilir.
4. Image iki tag ile etiketlenir:
   - `DOCKER_USER/myapp:latest`
   - `DOCKER_USER/myapp:GITHUB_COMMIT_SHA`
5. Iki tag Docker Hub'a push edilir.

Deploy adimi pipeline'i bozmasin diye otomatik calistirilmaz. Workflow icinde su not vardir:

```text
Local VirtualBox VM 127.0.0.1:2222 GitHub-hosted runner tarafindan erisilemez.
Gercek deploy icin public IP'li bir sunucu gerekir.
```

## Ansible Deploy Akisi

Ansible local VM'e SSH ile baglanir:

```text
127.0.0.1:2222 -> VirtualBox port forwarding -> Ubuntu VM SSH
```

Playbook sunucuda sunlari yapar:

1. `docker.io` ve `curl` paketlerini kurar.
2. Docker servisini enabled ve started yapar.
3. Docker Hub'dan `DOCKER_USER/myapp:latest` image'ini pull eder.
4. Eski `myapp` container'i varsa siler.
5. Yeni container'i calistirir:

```bash
docker run -d --restart unless-stopped -p 80:5000 --name myapp IMAGE
```

6. Container durumunu kontrol eder.
7. `curl http://localhost/health` ile healthcheck yapar.

## Local Deploy Calistirma

Once GitHub Actions ile image Docker Hub'a push edilmis olmali. Sonra local deploy calistirilir.

WSL, Git Bash veya Ubuntu VM icinden:

```bash
chmod +x scripts/local-deploy.sh
./scripts/local-deploy.sh DOCKERHUB_USERNAME
```

Ornek:

```bash
./scripts/local-deploy.sh gizemakkaya
```

Script su komutu calistirir:

```bash
ansible-playbook -i ansible/inventory.ini ansible/deploy.yml --extra-vars "docker_user=DOCKERHUB_USERNAME" --ask-become-pass
```

Windows PowerShell kullanirken Ansible yuku degilse iki pratik secenek vardir:

1. WSL icine Ansible kurup komutu WSL terminalinden calistirin.
2. Ubuntu VM icinde projeyi clone edip VM'e uygun inventory ile Ansible komutunu calistirin.

WSL icin ornek kurulum:

```bash
sudo apt update
sudo apt install ansible -y
```

PowerShell uzerinden WSL ile calistirma ornegi:

```powershell
wsl bash scripts/local-deploy.sh DOCKERHUB_USERNAME
```

Ubuntu VM icinden calistiracaksaniz `127.0.0.1:2222` yerine VM'in kendi SSH erisimini kullanacak ayri bir inventory gerekir. Bu repodaki varsayilan inventory Windows host veya WSL tarafindan VirtualBox port forwarding uzerinden baglanmak icindir.

## Public IP vs Private IP

Public IP:

- Internete aciktir.
- Genellikle ISP veya cloud provider tarafindan verilir.
- Dis dunyadan erisilebilir.
- GitHub Actions gibi bulut sistemlerinden erisilebilir olmasi icin sunucunun public IP'si gerekir.

Private IP:

- Yerel ag icinde kullanilir.
- Dogrudan internetten erisilemez.
- Ornek araliklar: `10.x.x.x`, `172.16.x.x`, `192.168.x.x`.

Bu projede Ubuntu VM'in ic IP adresi:

```text
10.0.2.15
```

Windows host uzerinden SSH baglantisi ise VirtualBox port forwarding ile yapilir:

```text
127.0.0.1:2222 -> Ubuntu VM:22
```

## Data Warehouse vs Data Lake vs Data Mesh

Data Warehouse:

- Temizlenmis ve organize edilmis veri saklanir.
- Analiz, raporlama ve BI dashboard icin uygundur.

Data Lake:

- Ham veri saklanir.
- Veri ihtiyac oldukca islenir.
- Log, dosya, medya ve veri bilimi senaryolari icin uygundur.

Data Mesh:

- Veri merkezi tek bir ekip yerine domain ekipleri tarafindan sahiplenilir.
- Satis, pazarlama, finans gibi ekipler veriyi veri urunu olarak yonetir.

## Onemli Not: GitHub Actions Neden Local VM'e Baglanamaz?

GitHub Actions GitHub'in bulut runner'larinda calisir. Bu yuzden workflow icinde `127.0.0.1` yazildiginda bu adres senin Windows bilgisayarini veya VirtualBox VM'ini degil, GitHub runner makinesini ifade eder.

Senin local SSH baglantin:

```bash
ssh -p 2222 gizem@127.0.0.1
```

Windows host uzerinde calisir, cunku VirtualBox port forwarding sadece senin bilgisayarinda gecerlidir.

GitHub Actions tarafindan gercek deploy yapmak icin:

- Public IP'li bir VPS/cloud sunucu gerekir.
- 22 veya belirlenen SSH portu internetten erisilebilir olmalidir.
- Firewall/security group ayarlari SSH ve HTTP trafigine izin vermelidir.

## Demo Senaryosu

1. Kodu GitHub'a push et.
2. GitHub Actions Docker image'i build eder.
3. Image Docker Hub'a `latest` ve commit SHA tag ile push edilir.
4. Local bilgisayarda veya WSL'de Ansible komutunu calistir:

```bash
./scripts/local-deploy.sh DOCKERHUB_USERNAME
```

5. VM icinde container calisir.
6. Windows host veya VM icinden uygulama test edilir.

VM icinden:

```bash
curl http://localhost/health
```

Eger VirtualBox HTTP port forwarding eklediysen Windows host uzerinden de ilgili port ile test edebilirsin.

## Sik Hatalar ve Cozumleri

### Docker Hub login hatasi

Sebep: `DOCKER_USER` veya `DOCKER_PASS` hatali olabilir.

Cozum: Docker Hub access token olusturup `DOCKER_PASS` secret'ina ekleyin.

### GitHub Actions local VM'e baglanamiyor

Sebep: `127.0.0.1`, GitHub runner'in kendisidir.

Cozum: Local VM deploy'u GitHub Actions'ta otomatik calistirmayin. Local deploy icin `scripts/local-deploy.sh` kullanin.

### SSH permission denied

Sebep: SSH key, kullanici veya port hatali olabilir.

Cozum:

```bash
ssh -p 2222 gizem@127.0.0.1
```

komutunu test edin.

### Ansible sudo sifresi istiyor

Sebep: Playbook `become: yes` kullaniyor.

Cozum: Komutu `--ask-become-pass` ile calistirin. Script bunu otomatik ekler.

### 80 portu calismiyor

Sebep: VM icinde baska servis 80 portunu kullaniyor olabilir veya port forwarding yoktur.

Cozum:

```bash
sudo ss -tulpn | grep :80
docker ps
```

### Healthcheck basarisiz

Sebep: Container calismiyor veya Flask uygulamasi cevap vermiyor olabilir.

Cozum:

```bash
docker logs myapp
curl http://localhost/health
```

### Ansible Windows PowerShell'de yok

Sebep: Ansible Windows'ta native olarak kolay calismayabilir.

Cozum: WSL veya Ubuntu VM icinde Ansible calistirin.
