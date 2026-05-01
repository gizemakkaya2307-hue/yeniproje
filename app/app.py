from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

ARCHITECTURE_FLOW = [
    "Developer",
    "GitHub",
    "GitHub Actions",
    "Docker Hub",
    "Ansible",
    "Ubuntu Server",
    "Docker Container",
]

DEPLOY_STEPS = [
    "Kod GitHub'a push edilir",
    "GitHub Actions pipeline calisir",
    "Docker image build edilir",
    "Image Docker Hub'a push edilir",
    "Ansible sunucuya SSH ile baglanir",
    "Container deploy edilir",
]

IP_CARDS = [
    {
        "title": "Public IP",
        "tag": "Internet",
        "example": "Ornek: 8.8.8.8",
        "text": "Internete acik, ISP tarafindan verilen ve dis dunyadan erisilebilen IP adresidir.",
    },
    {
        "title": "Private IP",
        "tag": "Local Network",
        "example": "Ornek: 192.168.1.10 / 10.0.2.15",
        "text": "Yerel ag icinde kullanilan, dogrudan internetten erisilemeyen IP adresidir.",
    },
]

DATA_CARDS = [
    {
        "title": "Data Warehouse",
        "tag": "Analize Hazir",
        "text": "Temizlenmis, duzenlenmis ve analiz icin hazir verilerin tutuldugu yapidir.",
        "usage": "Raporlama, BI dashboard ve karar destek sistemleri icin kullanilir.",
    },
    {
        "title": "Data Lake",
        "tag": "Ham Veri",
        "text": "Ham verilerin saklandigi, ihtiyac oldukca islendigi veri depolama yaklasimidir.",
        "usage": "Log, dosya, medya, veri bilimi ve makine ogrenmesi icin uygundur.",
    },
    {
        "title": "Data Mesh",
        "tag": "Domain Odakli",
        "text": "Verinin merkezi tek ekip yerine domain ekipleri tarafindan veri urunu olarak yonetildigi yaklasimdir.",
        "usage": "Satis, pazarlama ve finans gibi ekiplerin kendi veri urunlerini sahiplenmesini saglar.",
    },
]

PAGE_TEMPLATE = """
<!doctype html>
<html lang="tr">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Docker + Ansible + CI/CD Deploy Demo</title>
    <style>
      :root {
        font-family: Arial, sans-serif;
        color: #e5edf7;
        background: #0f172a;
      }

      * {
        box-sizing: border-box;
      }

      body {
        margin: 0;
        min-height: 100vh;
        background:
          radial-gradient(circle at top left, rgba(37, 99, 235, 0.25), transparent 34%),
          linear-gradient(135deg, #0f172a 0%, #111827 55%, #132033 100%);
        padding: 32px 16px;
      }

      main {
        width: min(1120px, 100%);
        margin: 0 auto;
      }

      header {
        padding: 34px 0 24px;
      }

      .eyebrow {
        color: #93c5fd;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 12px;
      }

      h1 {
        margin: 0;
        font-size: clamp(30px, 5vw, 54px);
        line-height: 1.05;
      }

      .summary {
        max-width: 820px;
        margin-top: 16px;
        color: #b8c4d6;
        font-size: 17px;
        line-height: 1.65;
      }

      section {
        margin-top: 22px;
        padding: 24px;
        background: rgba(15, 23, 42, 0.78);
        border: 1px solid rgba(148, 163, 184, 0.24);
        border-radius: 8px;
      }

      h2 {
        margin: 0 0 16px;
        font-size: 24px;
      }

      p {
        margin: 0;
        color: #b8c4d6;
        line-height: 1.6;
      }

      .flow {
        display: grid;
        grid-template-columns: repeat(7, minmax(0, 1fr));
        gap: 10px;
        align-items: stretch;
      }

      .flow-step {
        min-height: 84px;
        display: grid;
        place-items: center;
        text-align: center;
        padding: 12px;
        border: 1px solid rgba(96, 165, 250, 0.45);
        border-radius: 8px;
        background: linear-gradient(180deg, rgba(30, 64, 175, 0.42), rgba(15, 23, 42, 0.92));
        color: #dbeafe;
        font-weight: 700;
      }

      .steps {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 12px;
        counter-reset: deploy;
      }

      .deploy-step {
        position: relative;
        min-height: 96px;
        padding: 18px 16px 16px 56px;
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-radius: 8px;
        background: rgba(30, 41, 59, 0.78);
        color: #e2e8f0;
      }

      .deploy-step::before {
        counter-increment: deploy;
        content: counter(deploy);
        position: absolute;
        left: 16px;
        top: 16px;
        width: 28px;
        height: 28px;
        display: grid;
        place-items: center;
        border-radius: 50%;
        background: #22c55e;
        color: #052e16;
        font-weight: 800;
      }

      .grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 14px;
      }

      .grid.three {
        grid-template-columns: repeat(3, minmax(0, 1fr));
      }

      .card {
        padding: 18px;
        border: 1px solid rgba(148, 163, 184, 0.24);
        border-radius: 8px;
        background: rgba(30, 41, 59, 0.72);
      }

      .card h3 {
        margin: 0 0 10px;
        font-size: 20px;
      }

      .tag {
        display: inline-block;
        margin-bottom: 12px;
        padding: 5px 9px;
        border-radius: 999px;
        background: rgba(59, 130, 246, 0.18);
        color: #93c5fd;
        font-size: 12px;
        font-weight: 700;
      }

      .example {
        margin-top: 12px;
        color: #86efac;
        font-weight: 700;
      }

      .note {
        margin-top: 14px;
        padding: 16px;
        border-left: 4px solid #f59e0b;
        border-radius: 8px;
        background: rgba(245, 158, 11, 0.12);
        color: #fde68a;
      }

      footer {
        padding: 26px 4px 12px;
        color: #94a3b8;
        text-align: center;
      }

      @media (max-width: 900px) {
        .flow,
        .steps,
        .grid,
        .grid.three {
          grid-template-columns: 1fr;
        }

        section {
          padding: 20px;
        }
      }
    </style>
  </head>
  <body>
    <main>
      <header>
        <div class="eyebrow">Flask + Docker + Ansible + GitHub Actions</div>
        <h1>Docker + Ansible + CI/CD Deploy Demo</h1>
        <p class="summary">
          Bu uygulama, kodun GitHub'a gonderilmesinden Docker image'in Docker Hub'a push edilmesine
          ve Ubuntu VM uzerinde container olarak calismasina kadar olan CI/CD surecini ogrenci
          projesi formatinda gosterir.
        </p>
      </header>

      <section>
        <h2>Proje Mimarisi</h2>
        <div class="flow">
          {% for item in architecture_flow %}
          <div class="flow-step">{{ item }}</div>
          {% endfor %}
        </div>
      </section>

      <section>
        <h2>CI/CD Akisi</h2>
        <div class="steps">
          {% for item in deploy_steps %}
          <div class="deploy-step">{{ item }}</div>
          {% endfor %}
        </div>
      </section>

      <section>
        <h2>Public IP vs Private IP</h2>
        <div class="grid">
          {% for item in ip_cards %}
          <article class="card">
            <span class="tag">{{ item.tag }}</span>
            <h3>{{ item.title }}</h3>
            <p>{{ item.text }}</p>
            <p class="example">{{ item.example }}</p>
          </article>
          {% endfor %}
        </div>
        <p class="note">
          NAT: Private IP'li cihazlar internete router/NAT uzerinden cikar. Bu projede Ubuntu VM
          NAT icinde 10.0.2.15 IP'sini aldi; Windows host 127.0.0.1:2222 ile SSH baglantisi kurdu
          ve web uygulamasi 127.0.0.1:8080 uzerinden goruntulendi. GitHub Actions bulutta
          calistigi icin 127.0.0.1 onun icin bizim bilgisayarimiz degil, GitHub runner'dir.
        </p>
      </section>

      <section>
        <h2>Data Warehouse vs Data Lake vs Data Mesh</h2>
        <div class="grid three">
          {% for item in data_cards %}
          <article class="card">
            <span class="tag">{{ item.tag }}</span>
            <h3>{{ item.title }}</h3>
            <p>{{ item.text }}</p>
            <p class="example">{{ item.usage }}</p>
          </article>
          {% endfor %}
        </div>
      </section>

      <footer>/health endpoint'i calisiyor: {"status": "ok", "service": "myapp"}</footer>
    </main>
  </body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(
        PAGE_TEMPLATE,
        architecture_flow=ARCHITECTURE_FLOW,
        deploy_steps=DEPLOY_STEPS,
        ip_cards=IP_CARDS,
        data_cards=DATA_CARDS,
    )


@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "myapp"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
