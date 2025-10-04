from flask import Blueprint,redirect,render_template,url_for,request,flash,session

auth_bp = Blueprint('auth', __name__)

USER_CREDENTIALS = {
    'username' : 'admin',
    'password' : '1234'
}
@auth_bp.route("/login", methods = ["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        if username == USER_CREDENTIALS['username'] and password == USER_CREDENTIALS['password']:
            session['user'] = username  #use hoga badme, session is used to remeber who is logged in
            flash("Login Successful","success")
            return redirect(url_for('tasks.view_tasks')) 
        else:
            flash("Invalid Username of Password","danger")

    return render_template("login.html") #if login is not successful

@auth_bp.route("/logout")
def logout():
    session.pop('user',None) #use ho gaya
    flash("Logged out", "info")
    return redirect(url_for('auth.login'))
