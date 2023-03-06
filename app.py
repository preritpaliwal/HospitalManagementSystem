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

# Routes    
users = [('user1', 'type1'), ('user2', 'type2'), ('user3', 'type3')]

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
                return redirect('/admin')
            elif(request.form['type'] == 'Front Desk Operator'):
                return render_template('frontdesk.html')
            elif(request.form['type'] == 'Data Entry Operator'):
                return redirect('/dataentryoperator')
            elif(request.form['type'] == 'Doctor'):
                return redirect('/doctor')
    return render_template('index.html', flag=0)

@app.route('/admin', methods=["POST", "GET"])
def admin():
    # Query the database and get the list of usernames and types
    return render_template('admin.html', users=users)

@app.route('/adduser', methods=["POST", "GET"])
def adduser():
    if request.method == "POST":
        print(request.form['username'])
        print(request.form['password'])
        print(request.form['type'])
        # Add the user to the database
        users.append((request.form['username'], request.form['type']))
    return redirect('/admin')

@app.route('/deleteuser', methods=["POST", "GET"])
def deleteuser():
    if request.method == "POST":
        print(request.form['username_to_delete'])
        # Delete the user from the database
        for user in users:
            if user[0] == request.form['username_to_delete']:
                users.remove(user)
    return redirect('/admin')

@app.route('/dataentryoperator', methods=["POST", "GET"])
def dataoperator():
    return render_template('data_operator.html')

@app.route('/updateresults', methods=["POST", "GET"])
def updateresults():
    if request.method == "POST":
        print(request.form['test-id'])
        print(request.form['results'])
        # Update the results in the database
    return redirect('/dataentryoperator')

@app.route('/doctor', methods=["POST", "GET"])
def doctor():
    # Query the database and get the list of patients
    patients = [('1', 'patient1', '20', '293298329', 'pat1@gmail.com', 'Surat, India', '1234567890'), ('2', 'patient2', '20', '945453345', 'pat2@gmail.com', 'Surat, India', '1234567890'), ('3', 'patient3', '20', '293298329', 'pat3@gmail.com', 'Surat, India', '1234567890')]
    return render_template('doctor.html', patients=patients)

@app.route('/gotorecordmedication', methods=["POST", "GET"])
def gotorecordmedication():
    return render_template('record_medication.html')

@app.route('/gotorecordtesttreatment', methods=["POST", "GET"])
def gotorecordtesttreatment():
    return render_template('record_test_treatment.html')

@app.route('/recordmedication', methods=["POST", "GET"])
def recordmedication():
    if request.method == "POST":
        print(request.form['patient_id'])
        print(request.form['medication_id'])
        print(request.form['dosage'])
        print(request.form['date'])
        # Record the medication in the database
    return redirect('/doctor')

@app.route('/recordtesttreatment', methods=["POST", "GET"])
def recordtesttreatment():
    if request.method == "POST":
        print(request.form['patient_id'])
        print(request.form['test_treatment_id'])
        print(request.form['doctor_id'])
        # Record the test in the database
    return redirect('/doctor')

if __name__ == '__main__':
    app.run(debug = True)