from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session, url_for  # pyright: ignore[reportMissingImports]

app = Flask(__name__)
app.secret_key = "nutrition_clinic_secret_key_2026"

ADMIN_USER = "admin"
ADMIN_PASS = "nutrition2026"

appointments = []

CLINIC_SCHEDULE = {
    "Saturday": {
        "name": "السبت",
        "time": "12:00 ظهراً - 4:00 عصراً",
        "location": "الحوامدية - أمام الإسعاف",
    },
    "Wednesday": {
        "name": "الأربعاء",
        "time": "12:00 ظهراً - 4:00 عصراً",
        "location": "الحوامدية - أمام الإسعاف",
    },
    "Sunday": {
        "name": "الأحد",
        "time": "4:00 عصراً - 10:00 مساءً",
        "location": "الحوامدية - أمام الإسعاف",
    },
    "Tuesday": {
        "name": "الثلاثاء",
        "time": "4:00 عصراً - 10:00 مساءً",
        "location": "الحوامدية - أمام الإسعاف",
    },
    "Thursday": {
        "name": "الخميس",
        "time": "4:00 عصراً - 10:00 مساءً",
        "location": "الحوامدية - أمام الإسعاف",
    },
    "Friday": {
        "name": "الجمعة",
        "time": "8:00 صباحاً - 8:00 مساءً",
        "location": "ميت رهينة - صيدلية د. أحمد (أمام الوحدة المحلية)",
    },
}


@app.route("/")
def index():
    return render_template("index.html", schedule=CLINIC_SCHEDULE)


@app.route("/book", methods=["POST"])
def book():
    name = request.form.get("name")
    phone = request.form.get("phone")
    day = request.form.get("day")
    notes = request.form.get("notes", "")

    if not name or not phone or not day:
        flash("الرجاء إدخال الاسم، رقم الهاتف، واختيار اليوم بشكل صحيح.", "danger")
        return redirect(url_for("index"))

    booking_id = len(appointments) + 1
    new_appointment = {
        "id": booking_id,
        "name": name,
        "phone": phone,
        "day": CLINIC_SCHEDULE.get(day, {}).get("name", day),
        "location": CLINIC_SCHEDULE.get(day, {}).get("location", ""),
        "time": CLINIC_SCHEDULE.get(day, {}).get("time", ""),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "notes": notes,
    }
    appointments.append(new_appointment)
    flash(
        "تم تسجيل حجزك بنجاح! سيتم مراجعة المواعيد وحضورك في الموعد المحدد.",
        "success",
    )
    return redirect(url_for("index"))


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == ADMIN_USER and password == ADMIN_PASS:
            session["admin_logged"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            flash("اسم المستخدم أو كلمة المرور غير صحيحة.", "danger")
    return render_template("admin_login.html")


@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin_logged"):
        return redirect(url_for("admin_login"))
    return render_template("admin_dashboard.html", appointments=appointments)


@app.route("/admin/done/<int:appointment_id>", methods=["POST"])
def complete_appointment(appointment_id):
    if not session.get("admin_logged"):
        return redirect(url_for("admin_login"))

    global appointments
    appointments = [app for app in appointments if app["id"] != appointment_id]
    flash("تم إتمام الكشف وحذف المريض من القائمة بنجاح.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged", None)
    return redirect(url_for("admin_login"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)