import flask
from . import db
from .models import User, Form
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user,login_required, logout_user, current_user
from datetime import datetime, date
from sqlalchemy import *
import xlwt
from io import BytesIO
# import flask_excel as excel

routes = flask.Blueprint('routes', __name__)

# The path to fill in the form
@routes.route('/', methods=['GET', 'POST'])
def form():
    args = flask.request.form
    if(flask.request.method == 'POST'):
        # initialize a new form based on the POST request
        new_form = Form(year=args["year"],receivedDate = datetime.strptime(args["receivedDate"], '%Y-%m-%d') ,topic = args["topic"], \
            profession = args["profession"], detailedProfessionCategory = args["detailedProfessionCategory"] ,tenderingList= args["tenderingList"], \
            winner = args["winner"], scopeOfWork = args["scopeOfWork"], majorTerms= args["majorTerms"], totalPrice= args["totalPrice"], \
            unitPrice = args["unitPrice"], currency = args["currency"], exchangeRate = args["exchangeRate"], moblizationTime = args["moblizationTime"],\
            moblizationCost = args["moblizationCost"], tax = args["tax"], localContent = args["localContent"], handleDate = args["handleDate"], \
            personInCharge= args["personInCharge"], internalApprovedDate = args["internalApprovedDate"], \
            headOfficeApprovedDate = args["headOfficeApprovedDate"], responseDateToOperator = args["responseDateToOperator"],\
            remarks = args["remarks"])


        # insert the new form into database
        db.session.add(new_form)
        db.session.commit()

    # default GET request
    return flask.render_template("form.html", user=current_user)

# The path to download the records
@routes.route('/chart', methods=['GET', 'POST'])
@login_required
def chart():
    args = flask.request.form
    forms = None
    if flask.request.method == 'POST':
        #if not all dates are selected
        if args["startDate"] == '' or args["endDate"] == '':
            # query all records
            forms = Form.query.all()
            
        else:
            # query records based on start and end dates
            forms = Form.query.filter(and_(Form.receivedDate <= args["endDate"], Form.receivedDate >= args["startDate"]))

        # if there are results based on condition
        if forms != None:
            #initialize io and excel file
            output = BytesIO()
            workbook = xlwt.Workbook()
            sh = workbook.add_sheet('form')
            sh.write(0,0,"年份Year")
            sh.write(0,1,"收到日期 Received date")
            sh.write(0,2,"主题Topic")
            sh.write(0,3,"所属专业Profession")
            sh.write(0,4,"具体分类Detailed Profession Categary")
            sh.write(0,5,"投标商名单Tendering List")
            sh.write(0,6,"中标公司Winner")
            sh.write(0,7,"工作范围Scope of Work")
            sh.write(0,8,"主要合同条款Major Terms")
            sh.write(0,9,"总价Total Price")
            sh.write(0,10,"单价Unit Price")
            sh.write(0,11,"币种Currency")
            sh.write(0,12,"汇率Exchange Rate")
            sh.write(0,13,"动员时间Mobilization Time")
            sh.write(0,14,"动员费用Mobilization Cost")
            sh.write(0,15,"税费Tax")
            sh.write(0,16,"本地化率Local Content")
            sh.write(0,17,"分发开始处理日期Handle date")
            sh.write(0,18,"处理负责人Person in Charge")
            sh.write(0,19,"内部批复日期Internal Approved Date")
            sh.write(0,20,"总部批复时间")
            sh.write(0,21,"递交作业者日期Reponse Date to Operator")
            sh.write(0,22,"备注Remarks")
            sh.write(0,23,"文件序号File Number")

            idx = 0
            for row in forms:
                sh.write(idx + 1,0,row.year)
                sh.write(idx + 1, 1, row.receivedDate.strftime('%Y/%m/%d'))
                sh.write(idx + 1, 2, row.topic)
                sh.write(idx + 1, 3, row.profession)
                sh.write(idx + 1, 4, row.detailedProfessionCategory)
                sh.write(idx + 1, 5, row.tenderingList)
                sh.write(idx + 1, 6, row.winner)
                sh.write(idx + 1, 7, row.scopeOfWork)
                sh.write(idx + 1, 8, row.majorTerms)
                sh.write(idx + 1, 9, row.totalPrice)
                sh.write(idx + 1, 10 ,row.unitPrice)
                sh.write(idx + 1, 11 ,row.currency)
                sh.write(idx + 1, 12 ,row.exchangeRate)
                sh.write(idx + 1, 13 ,row.moblizationTime)
                sh.write(idx + 1, 14 ,row.moblizationCost)
                sh.write(idx + 1, 15 ,row.tax)
                sh.write(idx + 1, 16 ,row.localContent)
                sh.write(idx + 1, 17 ,row.handleDate)
                sh.write(idx + 1, 18 ,row.personInCharge)
                sh.write(idx + 1, 19 ,row.internalApprovedDate)
                sh.write(idx + 1, 20 ,row.headOfficeApprovedDate)
                sh.write(idx + 1, 21 ,row.responseDateToOperator)
                sh.write(idx + 1, 22 ,row.remarks)
                sh.write(idx + 1, 23 ,row.id)
                idx += 1
            workbook.save(output)
            output.seek(0)
            return flask.Response(output, mimetype="application/ms-excel", \
                headers={"Content-Disposition":"attachment;filename=test.xls"})
        else:
            flask.flash("Form doesn't exist",category='error')

    # default GET request
    return flask.render_template("chart.html", user=current_user)


# path for login
@routes.route('/login', methods=['GET','POST'])
def login():
    args = flask.request.form
    if flask.request.method == 'POST':
        # Acquire username and password from html form
        username = args.get('username')
        password = args.get('password')

        #search for the username
        user = User.query.filter_by(username=username).first()

        #if the username exists
        if user:
            #check if the hash of entered password equals passwords from database
            if check_password_hash(user.password,password):
                flask.flash('successs', category='success')
                login_user(user,remember=True)
                flask.redirect(flask.url_for('routes.chart'))
            else:
                flask.flash('Incorrect Password',category='error')
        else:
            flask.flash('not exist', category='error')
    return flask.render_template("login.html", user=current_user)

# path for logout
@routes.route('/logout',methods=['GET'])
def logout():
    logout_user()
    return flask.redirect(flask.url_for('routes.chart'))


# path for new account
@routes.route('/signup', methods=['GET','POST'])
def signup():
    args = flask.request.form
    # This authentication key ensures not everyone can interact with the database       
    authKey = 'tianyi'
    if flask.request.method == 'POST':
        # Acquire username and password from html form
        username = args.get('username')
        password = args.get('password')
        auth=args.get('authKey')

        # Query to check whether the user exists
        user = User.query.filter_by(username=username).first()
        if authKey != auth:
            flask.flash("Invalid Authentication Key", category="error")
        elif user:
            flask.flash("already exist", category="error")
        else:
            #save the username and hash of password to database
            new_user = User(username=username,password=generate_password_hash(password,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            return flask.redirect(flask.url_for('routes.chart'))


    
    return flask.render_template("signup.html", user=current_user)