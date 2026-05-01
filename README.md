# Docker + Ansible + CI/CD ile Otomatik Gorev Takip Uygulamasi Dagitimi

## Proje Adi

Docker + Ansible + CI/CD ile Otomatik Gorev Takip Uygulamasi Dagitimi

## Proje Amaci

Bu proje, Flask tabanli basit bir web uygulamasinin Docker ile container haline getirilmesini, GitHub Actions ile Docker image build/push surecinin otomatiklestirilmesini ve Ansible ile Ubuntu VM uzerinde container deploy edilmesini gosterir.

Proje bir ogrenci sunumu/odevi olarak CI/CD mantigini uc ana parca ile anlatir:

- Uygulama gelistirme: Flask web uygulamasi.
- Paketleme ve yayinlama: Docker image ve Docker Hub.
- Deploy otomasyonu: Ansible ile Ubuntu VM uzerinde container calistirma.

## Genel Mimari

```text
Developer
   |
   v
GitHub Repository
   |
   v
GitHub Actions
   |
   v
Docker Hub: brownekadn/myapp:latest
   |
   v
Ansible
   |
   v
Ubuntu VM
   |
   v
Docker Container
```

Bu mimaride GitHub Actions Docker image'i build edip Docker Hub'a push eder. Ubuntu VM tarafinda Ansible, Docker Hub'daki image'i cekip container olarak calistirir.

## Kullanilan Teknolojiler

- Python 3.10
- Flask
- Docker
- Docker Hub
- GitHub Actions
- Ansible
- Ubuntu Server VM
- VirtualBox NAT ve port forwarding

## CI/CD Akisi

GitHub Actions workflow dosyasi:

```text
.github/workflows/ci-cd.yml
```

Pipeline `main` branch'e push yapildiginda calisir:

1. Repository checkout edilir.
2. Docker Hub'a `DOCKER_USER` ve `DOCKER_PASS` secret'lari ile login olunur.
3. Docker image build edilir.
4. Image iki tag ile etiketlenir:
   - `brownekadn/myapp:latest`
   - `brownekadn/myapp:<commit-sha>`
5. Image Docker Hub'a push edilir.

Tamamlanan durum:

- GitHub Actions pipeline basarili calisti.
- Docker image Docker Hub'a push edildi.
- Image adi: `brownekadn/myapp:latest`

## Docker Hub Sureci

Dockerfile, Flask uygulamasini `python:3.10-slim` image'i uzerinde calistirir.

Dockerfile ozeti:

- `WORKDIR /app`
- `COPY app/ .`
- `pip install --no-cache-dir -r requirements.txt`
- `EXPOSE 5000`
- Python tabanli `HEALTHCHECK`
- `CMD ["python", "app.py"]`

Local test:

```bash
docker build -t myapp:local .
docker run --rm -p 5050:5000 --name myapp-local myapp:local
```

Health endpoint:

```text
http://127.0.0.1:5050/health
```

Beklenen sonuc:

```json
{"service":"myapp","status":"ok"}
```

## Ubuntu VM ve SSH Sureci

Ubuntu VM VirtualBox uzerinde NAT modunda calistirildi.

VM bilgileri:

```text
VM ic IP = 10.0.2.15
Ubuntu kullanici adi = gizem
SSH port forwarding = 127.0.0.1:2222 -> VM:22
```

Windows host uzerinden SSH baglantisi:

```bash
ssh -p 2222 gizem@127.0.0.1
```

Tamamlanan durum:

- Ubuntu VM kuruldu.
- SSH baglantisi kuruldu.
- Docker VM'e kuruldu.
- `brownekadn/myapp:latest` image VM'e cekildi.
- Container calistirildi.
- Site `http://127.0.0.1:8080` uzerinden goruntulendi.

## Ansible Deploy Mantigi

Ansible inventory:

```ini
[web]
localvm ansible_host=127.0.0.1 ansible_port=2222 ansible_user=gizem ansible_connection=ssh
```

Ansible playbook su islemleri yapar:

1. Ubuntu VM uzerinde Docker ve curl paketlerini kurar.
2. Docker servisinin started ve enabled olmasini saglar.
3. Docker Hub'dan image ceker:

```text
brownekadn/myapp:latest
```

4. Eski `myapp` container'i varsa kaldirir.
5. Yeni container'i calistirir:

```bash
docker run -d --restart unless-stopped -p 80:5000 --name myapp brownekadn/myapp:latest
```

6. `curl http://localhost/health` ile healthcheck yapar.

Local deploy komutu:

```bash
ansible-playbook -i ansible/inventory.ini ansible/deploy.yml --extra-vars "docker_user=brownekadn" --ask-become-pass
```

Script ile:

```bash
./scripts/local-deploy.sh brownekadn
```

## Public IP vs Private IP

### Public IP

Public IP internete acik, ISP veya cloud provider tarafindan verilen ve dis dunyadan erisilebilen IP adresidir.

Ornek:

```text
8.8.8.8
```

Public IP, GitHub Actions gibi bulut sistemlerinden erisilecek gercek sunucular icin gereklidir.

### Private IP

Private IP yerel ag icinde kullanilan ve dogrudan internetten erisilemeyen IP adresidir.

Ornek:

```text
192.168.1.10
10.0.2.15
```

Private IP'li cihazlar internete router/NAT uzerinden cikar.

### Bu Projedeki Durum

Ubuntu VM, VirtualBox NAT icinde su IP'yi aldi:

```text
10.0.2.15
```

Windows host, port forwarding ile VM'e SSH baglantisi kurdu:

```text
127.0.0.1:2222 -> Ubuntu VM:22
```

Web uygulamasi su adreste goruntulendi:

```text
http://127.0.0.1:8080
```

Onemli nokta: GitHub Actions bulutta calistigi icin workflow icinde `127.0.0.1` yazmak bizim bilgisayarimizi gostermez. GitHub runner'in kendi makinesini gosterir. Bu nedenle local VM deploy islemi GitHub Actions'ta otomatik calistirilmaz; local demo olarak Ansible ile calistirilir.

## Data Warehouse vs Data Lake vs Data Mesh

### Data Warehouse

Temizlenmis, duzenlenmis ve analiz icin hazir verilerin tutuldugu yapidir.

Kullanim:

- Raporlama
- BI dashboard
- Karar destek sistemleri

Kisa ozet: Veri once temizlenir ve organize edilir, sonra analiz edilir.

### Data Lake

Ham verilerin saklandigi, ihtiyac oldukca islendigi veri depolama yaklasimidir.

Kullanim:

- Log verileri
- Dosyalar
- Medya verileri
- Veri bilimi
- Makine ogrenmesi

Kisa ozet: Veri once ham haliyle saklanir, sonra ihtiyaca gore islenir.

### Data Mesh

Verinin merkezi tek ekip yerine domain ekipleri tarafindan veri urunu olarak yonetildigi yaklasimdir.

Kullanim:

- Satis verisi
- Pazarlama verisi
- Finans verisi
- Domain ekiplerinin kendi veri urunleri

Kisa ozet: Her is alani kendi verisinin sahibi olur ve veriyi kullanilabilir bir urun gibi yonetir.

## Proje Demo Adimlari

Sunumda gosterilebilecek ekranlar:

1. GitHub repository ve proje dosya yapisi.
2. GitHub Actions basarili pipeline ekrani.
3. Docker Hub uzerinde `brownekadn/myapp:latest` image'i.
4. Ubuntu VM SSH baglantisi:

```bash
ssh -p 2222 gizem@127.0.0.1
```

5. VM uzerinde Docker container durumu:

```bash
docker ps
```

6. Health endpoint testi:

```bash
curl http://localhost/health
```

7. Tarayicida calisan uygulama:

```text
http://127.0.0.1:8080
```

8. Web arayuzundeki teknik konu bolumleri:
   - Public IP vs Private IP
   - Data Warehouse vs Data Lake vs Data Mesh

## Sonuc

Bu proje ile Flask uygulamasi Docker image haline getirildi, GitHub Actions ile otomatik build/push sureci kuruldu ve Docker Hub'a image gonderildi. Ubuntu VM uzerinde Docker kuruldu, Ansible ile container deploy edildi ve uygulama `http://127.0.0.1:8080` adresinden basarili sekilde goruntulendi.

Proje hem CI/CD mantigini hem de temel ag/veri mimarisi kavramlarini sade bir ogrenci sunumu formatinda gostermektedir.
