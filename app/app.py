from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

DEPLOY_FLOW = [
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
        "text": "Internete acik, ISP tarafindan verilen ve dis dunyadan erisilebilen IP adresidir.",
    },
    {
        "title": "Private IP",
        "text": "Yerel ag icinde kullanilir ve dogrudan internetten erisilemez.",
    },
    {
        "title": "Bu Projede",
        "text": "VirtualBox VM ic IP olarak 10.0.2.15 kullanir. Windows host, port forwarding ile 127.0.0.1:2222 uzerinden SSH baglanir.",
    },
]

DATA_CARDS = [
    {
        "title": "Data Warehouse",
        "text": "Temizlenmis, organize edilmis ve analiz icin hazir verinin tutuldugu yapidir.",
    },
    {
        "title": "Data Lake",
        "text": "Ham verinin saklandigi ve ihtiyac oldukca islendigi veri depolama yaklasimidir.",
    },
    {
        "title": "Data Mesh",
        "text": "Verinin domain ekipleri tarafindan veri urunu olarak yonetildigi yaklasimdir.",
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
        color: #172033;
        background: #f4f7fb;
      }

      body {
        margin: 0;
        padding: 32px 16px;
      }

      main {
        width: min(980px, 100%);
        margin: 0 auto;
        background: #fff;
        border: 1px solid #d9e2ef;
        border-radius: 8px;
        box-shadow: 0 18px 45px rgba(23, 32, 51, 0.08);
        overflow: hidden;
      }

      header,
      section,
      footer {
        padding: 28px 32px;
      }

      header {
        border-bottom: 1px solid #e7edf5;
      }

      h1 {
        margin: 0 0 8px;
        font-size: 30px;
      }

      h2 {
        margin: 0 0 18px;
        font-size: 20px;
      }

      p {
        margin: 0;
        color: #5d6b82;
        line-height: 1.55;
      }

      ol {
        margin: 0;
        padding-left: 22px;
      }

      li {
        padding: 8px 0;
      }

      section {
        border-bottom: 1px solid #edf2f7;
      }

      .grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 14px;
      }

      .card {
        border: 1px solid #dce6f1;
        border-radius: 8px;
        padding: 16px;
        background: #fbfdff;
      }

      .card h3 {
        margin: 0 0 10px;
        font-size: 17px;
      }

      .note {
        margin-top: 16px;
        padding: 14px 16px;
        border-left: 4px solid #2563eb;
        background: #eff6ff;
        color: #1e3a8a;
      }

      footer {
        background: #f8fafc;
        color: #5d6b82;
        font-size: 14px;
      }

      @media (max-width: 780px) {
        header,
        section,
        footer {
          padding: 22px 20px;
        }

        .grid {
          grid-template-columns: 1fr;
        }
      }
    </style>
  </head>
  <body>
    <main>
      <header>
        <h1>Docker + Ansible + CI/CD Deploy Demo</h1>
        <p>Flask uygulamasi Docker ile paketlenir, GitHub Actions ile Docker Hub'a gonderilir ve Ansible ile local Ubuntu VM'e deploy edilebilir.</p>
      </header>

      <section>
        <h2>Gorev / Deploy Akisi</h2>
        <ol>
          {% for item in deploy_flow %}
          <li>{{ item }}</li>
          {% endfor %}
        </ol>
      </section>

      <section>
        <h2>Public IP vs Private IP</h2>
        <div class="grid">
          {% for item in ip_cards %}
          <article class="card">
            <h3>{{ item.title }}</h3>
            <p>{{ item.text }}</p>
          </article>
          {% endfor %}
        </div>
        <p class="note">GitHub Actions bulutta calistigi icin 127.0.0.1 adresi kullanicinin VirtualBox VM'i degil, GitHub runner'in kendisidir.</p>
      </section>

      <section>
        <h2>Data Warehouse vs Data Lake vs Data Mesh</h2>
        <div class="grid">
          {% for item in data_cards %}
          <article class="card">
            <h3>{{ item.title }}</h3>
            <p>{{ item.text }}</p>
          </article>
          {% endfor %}
        </div>
      </section>

      <footer>/health endpoint'i deploy kontrolu icin hazir.</footer>
    </main>
  </body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(
        PAGE_TEMPLATE,
        deploy_flow=DEPLOY_FLOW,
        ip_cards=IP_CARDS,
        data_cards=DATA_CARDS,
    )


@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "myapp"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
