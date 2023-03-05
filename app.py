from flask import Flask, render_template, Response, jsonify, request, redirect

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# prevent cached responses

if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response



@app.route('/', methods=["POST", "GET"])
def hello_world():
    if request.method == "POST":
        print(request.form['username'])
        print(request.form['password'])
        print(request.form['type'])
        auth_fail = 0
        if auth_fail:  
            return render_template('index.html', flag=1)  
        else:       
            global currentuserid
            currentuserid = request.form['username']
            if(request.form['type'] == 'Database Administrator'):
                return admin()
            elif(request.form['type'] == 'Front Desk Operator'):
                return render_template('frontdesk.html')
            elif(request.form['type'] == 'Data Entry Operator'):
                return render_template('data_operator.html')
            elif(request.form['type'] == 'Doctor'):
                return render_template('doctor.html')
    return render_template('index.html', flag=0)

@app.route('/admin', methods=["POST", "GET"])
def admin():
    # Query the database and get the list of usernames and types
    users = [('user1', 'type1'), ('user2', 'type2'), ('user3', 'type3')]
    return render_template('admin.html', users=users)

@app.route('/adduser', methods=["POST", "GET"])
def adduser():
    if request.method == "POST":
        print(request.form['username'])
        print(request.form['password'])
        print(request.form['type'])
        # Add the user to the database
    return admin()

if __name__ == '__main__':
    app.run(debug = True)