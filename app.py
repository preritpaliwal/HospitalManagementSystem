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
                return redirect('/admin/0')
            elif(request.form['type'] == 'Front Desk Operator'):
                return redirect('/frontdesk/main/0')
            elif(request.form['type'] == 'Data Entry Operator'):
                return redirect('/dataentryoperator/0')
            elif(request.form['type'] == 'Doctor'):
                return redirect('/doctor')
    return render_template('index.html', flag=0)

@app.route('/admin/<flag>', methods=["POST", "GET"])
def admin(flag):
    # Query the database and get the list of usernames and types
    return render_template('admin.html', users=users , flag=int(flag))

@app.route('/adduser', methods=["POST", "GET"])
def adduser():
    if request.method == "POST":
        print(request.form['username'])
        print(request.form['password'])
        print(request.form['type'])
        error = 1
        if error:
            return redirect('/admin/1')
        # Add the user to the database
        users.append((request.form['username'], request.form['type']))
    return redirect('/admin/0')

@app.route('/deleteuser', methods=["POST", "GET"])
def deleteuser():
    if request.method == "POST":
        print(request.form['username_to_delete'])
        # Delete the user from the database
        for user in users:
            if user[0] == request.form['username_to_delete']:
                users.remove(user)
    return redirect('/admin/0')

@app.route('/frontdesk/<function>/<flag>', methods=["POST", "GET"])
def frontdesk(function, flag):
    display = 0
    if function == 'registerpatient':
        display = 1
    elif function == 'admitpatient':
        display = 2
    elif function == 'dischargepatient':
        display = 3
    elif function == 'makeappointment':
        display = 4
    elif function == 'scheduletesttreatment':
        display = 5
    print(display)
    return render_template('front_desk_op.html', display=int(display), flag=int(flag))

@app.route('/registerpatientbutton', methods=["POST", "GET"])
def registerpatientbutton():
    return redirect('/frontdesk/registerpatient/0')

@app.route('/registerpatient', methods=["POST", "GET"])
def registerpatient():
    if request.method == "POST":
        print(request.form['patient-name'])
        print(request.form['patient-age'])
        print(request.form['patient-phone'])
        print(request.form['patient-email'])
        print(request.form['patient-address'])
        print(request.form['patient-ins'])
        error = 0
        if error:
            return redirect('/frontdesk/registerpatient/1')
        # Register the patient in the database
    return redirect('/frontdesk/registerpatient/0')

@app.route('/admitpatientbutton', methods=["POST", "GET"])
def admitpatientbutton():
    return redirect('/frontdesk/admitpatient/0')

@app.route('/dischargepatientbutton', methods=["POST", "GET"])
def dischargepatientbutton():
    return redirect('/frontdesk/dischargepatient/0')

@app.route('/makeappointmentbutton', methods=["POST", "GET"])
def makeappointmentbutton():
    return redirect('/frontdesk/makeappointment/0')

@app.route('/scheduletesttreatmentbutton', methods=["POST", "GET"])
def scheduletesttreatmentbutton():
    return redirect('/frontdesk/scheduletesttreatment/0')

@app.route('/dataentryoperator/<flag>', methods=["POST", "GET"])
def dataoperator(flag):
    return render_template('data_operator.html', flag=int(flag))

@app.route('/updateresults', methods=["POST", "GET"])
def updateresults():
    if request.method == "POST":
        print(request.form['test-id'])
        print(request.form['results'])
        # Update the results in the database
        test_not_found = 1
        if test_not_found:
            return redirect('/dataentryoperator/1')
    return redirect('/dataentryoperator/0')

@app.route('/doctor', methods=["POST", "GET"])
def doctor():
    # Query the database and get the list of patients
    patients = [('1', 'patient1', '20', '293298329', 'pat1@gmail.com', 'Surat, India', '1234567890'), ('2', 'patient2', '20', '945453345', 'pat2@gmail.com', 'Surat, India', '1234567890'), ('3', 'patient3', '20', '293298329', 'pat3@gmail.com', 'Surat, India', '1234567890')]
    return render_template('doctor.html', patients=patients)

@app.route('/gotorecordmedication/<flag>', methods=["POST", "GET"])
def gotorecordmedication(flag):
    return render_template('record_medication.html', flag=int(flag))

@app.route('/gotorecordtesttreatment/<flag>', methods=["POST", "GET"])
def gotorecordtesttreatment(flag):
    return render_template('record_test_treatment.html', flag=int(flag))

@app.route('/recordmedication', methods=["POST", "GET"])
def recordmedication():
    if request.method == "POST":
        print(request.form['patient_id'])
        print(request.form['medication_id'])
        print(request.form['dosage'])
        print(request.form['date'])
        error = 0
        if error:
            return redirect('/gotorecordmedication/1')
        # Record the medication in the database
    return redirect('/gotorecordmedication/0')

@app.route('/recordtesttreatment', methods=["POST", "GET"])
def recordtesttreatment():
    if request.method == "POST":
        print(request.form['patient_id'])
        print(request.form['test_treatment_id'])
        print(request.form['doctor_id'])
        error = 0
        if error:
            return redirect('/gotorecordtesttreatment/1')
        # Record the test in the database
    return redirect('/gotorecordtesttreatment/0')

if __name__ == '__main__':
    app.run(debug = True)