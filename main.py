from flask.views import MethodView
from wtforms import Form, StringField, SubmitField
from flask import Flask, render_template, request
from roommates_bill import room

app = Flask(__name__)
class HomePage(MethodView):

    def get(self):
        return render_template('index.html')


class BillFormPage(MethodView):

    def get(self):
        bill_form = BillForm()
        return render_template('bill_form_page.html', billform=bill_form)

    def post(self):
        billform = BillForm(request.form)
        amount = billform.amount.data
        period = billform.period.data

        name1 = billform.name1.data
        name2 = billform.name2.data
        days_in_house1 = billform.days_in_house1.data
        days_in_house2 = billform.days_in_house2.data

        the_bill = room.Bill(float(amount), period)
        roommate1 = room.Roommate(name1, float(days_in_house1))
        roommate2 = room.Roommate(name2, float(days_in_house2))

        return render_template('bill_form_page.html',
                               result=True,
                               billform=billform,
                               name1=roommate1.name,
                               amount1=roommate1.pays(the_bill, roommate2),
                               name2=roommate2.name,
                               amount2=roommate2.pays(the_bill, roommate1))


class BillForm(Form):
    amount = StringField("Bill Amount: ", default="100")
    period = StringField("Bill Period: ", default="December 2023")

    name1 = StringField("Name: ", default="John")
    days_in_house1 = StringField("Days in the house: ", default=30)

    name2 = StringField("Name: ", default="Aaron")
    days_in_house2 = StringField("Days in the house: ", default=30)

    button = SubmitField("Calculate")


app.add_url_rule('/', 
                 view_func=HomePage.as_view('home_page'))
app.add_url_rule('/bill_form_page', 
                 view_func=BillFormPage.as_view('bill_form_page'))


app.run()
