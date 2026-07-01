import io
import json
import pandas as pd
from datetime import date
from flask import (
    Flask, render_template, request, redirect, url_for,
    send_file, flash
)
from manajer_studio import StudioManager

app = Flask(__name__)
app.secret_key = "pixelops-secret-key-2026"

sm = StudioManager()


@app.template_filter("format_rp")
def format_rp(amount):
    """Format number as Indonesian Rupiah."""
    return f"Rp {amount:,.0f}".replace(",", ".")


@app.route("/")
def dashboard():
    total = sm.total_project()
    progress = sm.total_active_project()
    revisi = sm.total_revisi_project()
    selesai = sm.total_selesai_project()

    revenue = sm.total_revenue()
    piutang = sm.total_piutang()
    pay_stats = sm.payment_status_counts()

    all_projects = sm.tampil_project()

    recent = (all_projects or [])[:10]

    # Sort: Progres → Revisi → Selesai
    status_order = {"progres": 0, "revisi": 1, "selesai": 2}
    recent.sort(key=lambda p: status_order.get(p.get("status", "").lower(), 99))

    # Serialize for JS calendar (exclude finished projects)
    projects_json = json.dumps([
        {"id": p["id"], "nama": p["nama_project"],
         "deadline": p.get("deadline", ""),
         "status": p.get("status", "")}
        for p in all_projects if p.get("deadline") and p.get("status", "").lower() != "selesai"
    ])

    return render_template(
        "dashboard.html",
        total=total,
        progress=progress,
        revisi=revisi,
        selesai=selesai,
        revenue=revenue,
        piutang=piutang,
        total_tagihan=revenue + piutang,
        pay_stats=pay_stats,
        recent=recent,
        projects_json=projects_json,
    )


@app.route("/projects")
def project_list():
    projects = [p for p in sm.tampil_project() if p.get('status', '').lower() != 'selesai']
    return render_template("projects.html", projects=projects)


@app.route("/archived")
def archived_list():
    all_projects = sm.tampil_project()
    archived = [p for p in all_projects if p.get('status', '').lower() == 'selesai']
    return render_template("archived.html", archived=archived)


@app.route("/projects/<int:project_id>/edit", methods=["GET", "POST"])
def edit_project(project_id):
    project = sm.tampil_project_by_id(project_id)
    if not project:
        flash("Project tidak ditemukan!", "error")
        return redirect(url_for("project_list"))

    if request.method == "POST":
        nama = request.form.get("nama", "").strip()
        if not nama:
            flash("Nama Project wajib diisi!", "error")
            return redirect(url_for("edit_project", project_id=project_id))

        c_id = int(request.form.get("client_id", 0))
        d_id = int(request.form.get("designer_id", 0))
        jenis = request.form.get("jenis", "Logo Design")
        deadline = request.form.get("deadline", str(date.today()))
        budget = float(request.form.get("budget", 0))
        deskripsi = request.form.get("deskripsi", "")

        sm.update_project(project_id, nama, deskripsi, jenis, c_id, d_id, deadline, budget)
        flash(f"Project '{nama}' berhasil diperbarui! ✅", "success")
        return redirect(url_for("project_list"))

    clients = sm.tampil_client()
    designers = sm.tampil_designer()
    return render_template(
        "add_project.html", project=project, clients=clients,
        designers=designers, today=date.today()
    )


@app.route("/projects/add", methods=["GET", "POST"])
def add_project():
    clients = sm.tampil_client()
    designers = sm.tampil_designer()

    if request.method == "POST":
        nama = request.form.get("nama", "").strip()
        if not nama:
            flash("Nama Project wajib diisi!", "error")
            return redirect(url_for("add_project"))

        client_mode = request.form.get("client_mode", "existing")
        if client_mode == "new":
            c_nama = request.form.get("c_nama_baru", "").strip()
            if not c_nama:
                flash("Nama Klien Baru wajib diisi!", "error")
                return redirect(url_for("add_project"))
            c_perusahaan = request.form.get("c_perusahaan", "")
            c_email = request.form.get("c_email", "")
            c_telepon = request.form.get("c_telepon", "")
            c_id = sm.tambah_client(c_nama, c_perusahaan, c_email, c_telepon)
        else:
            c_id = int(request.form.get("client_id", 0))
            if c_id == 0:
                flash("Silakan pilih Klien!", "error")
                return redirect(url_for("add_project"))

        d_id = int(request.form.get("designer_id", 0))
        if d_id == 0:
            flash("Silakan pilih Desainer!", "error")
            return redirect(url_for("add_project"))

        jenis = request.form.get("jenis", "Logo Design")
        deadline = request.form.get("deadline", str(date.today()))
        budget = float(request.form.get("budget", 0))
        deskripsi = request.form.get("deskripsi", "")

        new_id = sm.tambah_project(
            nama, deskripsi, jenis, c_id, d_id, deadline, budget
        )
        flash(f"Project '{nama}' berhasil ditambahkan! 🚀", "success")
        return redirect(url_for("project_list"))

    return render_template(
        "add_project.html", clients=clients, designers=designers,
        today=date.today()
    )


@app.route("/projects/<int:project_id>/complete", methods=["POST"])
def complete_project(project_id):
    sm.update_status_project(project_id, "Selesai")
    flash("Project selesai! 🎉", "success")
    return redirect(url_for("project_list"))


@app.route("/projects/<int:project_id>/delete", methods=["POST"])
def delete_project(project_id):
    sm.hapus_project(project_id)
    flash("Project berhasil dihapus.", "success")
    return redirect(url_for("project_list"))


@app.route("/projects/<int:project_id>/revision", methods=["POST"])
def add_revision(project_id):
    catatan = request.form.get("catatan", "")
    if catatan.strip():
        sm.tambah_revisi(project_id, catatan)
        flash("Revisi berhasil ditambahkan.", "success")
    else:
        flash("Catatan revisi tidak boleh kosong!", "error")
    return redirect(url_for("project_list"))


@app.route("/projects/<int:project_id>/payment", methods=["POST"])
def add_payment(project_id):
    total = float(request.form.get("total", 0))
    dp = float(request.form.get("dp", 0))
    sm.tambah_payment(project_id, total, dp)
    flash("Tagihan berhasil dibuat! 💳", "success")
    return redirect(url_for("project_list"))


@app.route("/revisions")
def revision_list():
    revisions = sm.tampil_revisi()
    return render_template("revisions.html", revisions=revisions)


@app.route("/clients-designers")
def clients_designers():
    clients = sm.tampil_client()
    designers = sm.tampil_designer()
    return render_template("clients_designers.html", clients=clients, designers=designers)


@app.route("/clients/add", methods=["POST"])
def add_client():
    nama = request.form.get("nama", "").strip()
    if not nama:
        flash("Nama Klien wajib diisi!", "error")
        return redirect(url_for("clients_designers"))
    perusahaan = request.form.get("perusahaan", "")
    email = request.form.get("email", "")
    telepon = request.form.get("telepon", "")
    sm.tambah_client(nama, perusahaan, email, telepon)
    flash("Klien berhasil ditambahkan! ✅", "success")
    return redirect(url_for("clients_designers"))


@app.route("/clients/<int:client_id>/delete", methods=["POST"])
def delete_client(client_id):
    sm.hapus_client(client_id)
    flash("Klien berhasil dihapus.", "success")
    return redirect(url_for("clients_designers"))


@app.route("/designers/add", methods=["POST"])
def add_designer():
    nama = request.form.get("nama", "").strip()
    if not nama:
        flash("Nama Desainer wajib diisi!", "error")
        return redirect(url_for("clients_designers"))
    spesialis = request.form.get("spesialis", "")
    email = request.form.get("email", "")
    sm.tambah_designer(nama, spesialis, email)
    flash("Desainer berhasil ditambahkan! ✅", "success")
    return redirect(url_for("clients_designers"))


@app.route("/designers/<int:designer_id>/delete", methods=["POST"])
def delete_designer(designer_id):
    sm.hapus_designer(designer_id)
    flash("Desainer berhasil dihapus.", "success")
    return redirect(url_for("clients_designers"))


@app.route("/payments")
def payment_list():
    payments = sm.tampil_payment()
    # Sort: Belum Bayar (sisa > 0, dp = 0) → DP (sisa > 0, dp > 0) → Lunas (sisa = 0)
    def sort_key(p):
        sisa = p.get('sisa', 0)
        dp = p.get('dp', 0)
        if sisa == 0: return 2  # Lunas
        if dp == 0: return 0    # Belum Bayar
        return 1                 # DP
    payments.sort(key=sort_key)
    return render_template("payments.html", payments=payments)


@app.route("/payments/<int:payment_id>/pay", methods=["POST"])
def pay_payment(payment_id):
    bayar = float(request.form.get("bayar", 0))
    if bayar <= 0:
        flash("Jumlah bayar harus lebih dari 0!", "error")
    else:
        sm.update_payment(payment_id, bayar)
        flash("Pembayaran berhasil! ✅", "success")
    return redirect(url_for("payment_list"))


@app.route("/export/excel")
def export_excel():
    # Project data
    df_projects = pd.DataFrame(sm.tampil_project())
    # Finance summary
    pay_stats = sm.payment_status_counts()
    finance_summary = {
        "Metric": [
            "Total Revenue",
            "Total Piutang",
            "Lunas",
            "DP (Dicicil)",
            "Belum Bayar",
        ],
        "Value": [
            sm.total_revenue(),
            sm.total_piutang(),
            pay_stats.get("Lunas", 0),
            pay_stats.get("DP", 0),
            pay_stats.get("Belum Bayar", 0),
        ],
    }
    df_finance = pd.DataFrame(finance_summary)

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df_projects.to_excel(writer, index=False, sheet_name="Projects")
        df_finance.to_excel(writer, index=False, sheet_name="Finance")

    buffer.seek(0)
    return send_file(
        buffer,
        mimetype=(
            "application/vnd.openxmlformats-officedocument"
            ".spreadsheetml.sheet"
        ),
        as_attachment=True,
        download_name="pixelops_data.xlsx",
    )


if __name__ == "__main__":
    app.run(debug=True)