from flask import Flask, render_template, request, redirect, session, url_for
from auth import signup, login, get_totp_secret, verify_totp, get_totp_uri
from file_manager import create_file, access_file, share_file, view_metadata, get_user_files

app = Flask(__name__)
app.secret_key = "secure_fs_super_secret_key"

# HOME → LOGIN PAGE
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        if login(u, p):
            session["pre_auth_user"] = u
            return redirect(url_for("two_factor"))
        else:
            return render_template("login.html", error="Invalid Credentials")


    return render_template("login.html")

# 2FA PAGE
@app.route("/2fa", methods=["GET"])
def two_factor():
    if "pre_auth_user" not in session:
        return redirect("/")
    
    u = session["pre_auth_user"]
    secret = get_totp_secret(u)
    uri = get_totp_uri(u)
    return render_template("2fa.html", secret=secret, uri=uri)

# VERIFY 2FA
@app.route("/verify-2fa", methods=["POST"])
def verify_2fa():
    if "pre_auth_user" not in session:
        return redirect("/")
    
    u = session["pre_auth_user"]
    code = request.form["otp"]

    if verify_totp(u, code):
        session["user"] = u
        session.pop("pre_auth_user", None)
        return redirect("/dashboard")
    else:
        secret = get_totp_secret(u)
        uri = get_totp_uri(u)
        return render_template("2fa.html", secret=secret, uri=uri, error="Invalid Security Code")

# SIGNUP
@app.route("/signup", methods=["POST"])
def signup_user():
    u = request.form["username"]
    p = request.form["password"]
    if signup(u, p):
        session["pre_auth_user"] = u
        return redirect(url_for("two_factor"))
    else:
        return render_template("login.html", error="Username already exists.")



# DASHBOARD
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect("/")

    user = session["user"]
    message = ""
    file_content = ""
    file_metadata = None

    if request.method == "POST":
        action = request.form.get("action")

        if action == "create":
            fname = request.form["filename"]
            content = request.form["content"]
            res = create_file(user, fname, content)
            if res == "Success":
                message = "File created successfully!"
            else:
                message = res # Security violation message

        elif action == "read":
            fname = request.form["filename"]
            file_content = access_file(user, fname)
            if file_content == "Access Denied!":
                message = "Access Denied!"
                file_content = ""

        elif action == "share":
            fname = request.form["filename"]
            target = request.form["target"]
            message = share_file(user, fname, target)

        elif action == "metadata":
            fname = request.form["filename"]
            file_metadata = view_metadata(fname)
            if not file_metadata:
                message = "No metadata found."

    user_files = get_user_files(user)
    return render_template("dashboard.html", 
                         user=user, 
                         message=message, 
                         files=user_files, 
                         file_content=file_content, 
                         file_metadata=file_metadata)


# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)