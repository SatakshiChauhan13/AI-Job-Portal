from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_connection

app = Flask(__name__)
app.secret_key = "jobportal123"

@app.route("/")
def home():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM jobs
        ORDER BY created_at DESC
        LIMIT 3
    """)

    jobs = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("index.html", jobs=jobs)

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user and check_password_hash(user["password"], password):

            session["user_id"] = user["id"]
            session["user_name"] = user["full_name"]

            flash("Login successful!", "success")

            return redirect("/dashboard")

        flash("Invalid email or password!", "error")

        return redirect("/login")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form["full_name"]
        email = request.form["email"]
        password = generate_password_hash(
            request.form["password"]
        )

        conn = get_connection()
        cursor = conn.cursor()

        # Check duplicate email
        cursor.execute(
            "SELECT id FROM users WHERE email=%s",
            (email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:

            cursor.close()
            conn.close()

            flash(
                "Email already registered. Please login.",
                "error"
            )

            return redirect("/register")

        query = """
        INSERT INTO users(full_name, email, password)
        VALUES(%s,%s,%s)
        """

        cursor.execute(
            query,
            (full_name, email, password)
        )

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            "Registration successful! Please login.",
            "success"
        )

        return redirect("/login")

    return render_template("register.html")

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:

        flash("Please login to continue.", "error")

        return redirect("/login")

    return render_template(
        "dashboard.html",
        name=session["user_name"]
    )

@app.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully!", "success")

    return redirect("/login")

@app.route("/post_job", methods=["GET", "POST"])
def post_job():

    if "user_id" not in session:
        flash("Please login first.", "error")
        return redirect("/login")

    if request.method == "POST":

        job_title = request.form["job_title"]
        company_name = request.form["company_name"]
        location = request.form["location"]
        salary = request.form["salary"]
        description = request.form["description"]

        conn = get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO jobs(job_title, company_name, location, salary, description)
        VALUES(%s,%s,%s,%s,%s)
        """

        cursor.execute(
            query,
            (
                job_title,
                company_name,
                location,
                salary,
                description
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        flash("Job posted successfully!", "success")

        return redirect("/jobs")

    return render_template("post_job.html")

@app.route("/jobs")
def jobs():

    search = request.args.get("search", "")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if search:

        value = "%" + search + "%"

        query = """
        SELECT *
        FROM jobs
        WHERE job_title LIKE %s
        OR company_name LIKE %s
        OR location LIKE %s
        ORDER BY created_at DESC
        """

        cursor.execute(query, (value, value, value))

    else:

        cursor.execute("""
            SELECT *
            FROM jobs
            ORDER BY created_at DESC
        """)

    jobs = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "jobs.html",
        jobs=jobs,
        search=search
    )

@app.route("/apply/<int:job_id>")
def apply(job_id):

    if "user_id" not in session:

        flash("Please login to apply for jobs.", "error")

        return redirect("/login")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM applications
        WHERE user_id=%s
        AND job_id=%s
        """,
        (session["user_id"], job_id)
    )

    if cursor.fetchone():

        cursor.close()
        conn.close()

        flash(
            "You have already applied for this job.",
            "error"
        )

        return redirect("/jobs")

    cursor.execute(
        """
        INSERT INTO applications(user_id, job_id)
        VALUES(%s,%s)
        """,
        (session["user_id"], job_id)
    )

    conn.commit()

    cursor.close()
    conn.close()

    flash(
        "Application submitted successfully!",
        "success"
    )

    return redirect("/my_applications")

@app.route("/my_applications")
def my_applications():

    if "user_id" not in session:

        flash("Please login to view your applications.", "error")

        return redirect("/login")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT
        jobs.job_title,
        jobs.company_name,
        jobs.location,
        jobs.salary,
        jobs.description,
        applications.applied_at
    FROM applications
    JOIN jobs
        ON applications.job_id = jobs.id
    WHERE applications.user_id = %s
    ORDER BY applications.applied_at DESC
    """

    cursor.execute(query, (session["user_id"],))

    applications = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "my_applications.html",
        applications=applications
    )

if __name__ == "__main__":
    app.run(debug=True)