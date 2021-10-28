This is the readme for my cs50 final proyect: Budget.

#### Video Demo:
	https://www.youtube.com/watch?v=PerFshL5L2w

## Description:
	Budget is a website that allows you to keep track of your expenses
	while making sure that you don't go over your budget.


####Technologies used:
		HTML, CSS and JS in the front-end. SQL and flask in the back-end.

#### Responsiveness:
	The website is fully responsive. You can use in a phone, tablet or desktop.

#### Database:
	I used a sql database with two tables to store the user information and history of expenses.
	The first table is called users and stores the user id, username, email, hash and annual budget.
	The second table is called history and stores the user id,
	name of expense, category, price anddate.


### Functionalities:

#### Register [/Register]
	The first thing that the user needs to do is Register. If you don't fill all the fields
	or don't complete them correctly, an error message will pop up.
	Provide a username, email and password. There are no restrictions for this fields. The email that you put here won't be
	actually used for anything. But I asked it because it could be useful for future functionalities.
	You can provide your annual budget now or do it later.
	Once you successfully register, you'll be redirected to the login page.


#### Login [/Login]
		To login fill the fields with your username and password. Then click on "Iniciar sesion" (Login).
		If the information does not match or you left a field blank, an error message will appear.

#### Budget (Presupuesto):
	You can visualize your annualy and montly budget in the
	"see expenses" (Ver gastos) or "add expenses" (Agregar gastos) pages. If you
	want to change it, you can do so in the "account" (Cuenta) page.


#### Add expenses (Agregar gastos):
	Here you can add your expenses one by one. To
	do so, fill the fields with the required information: expense name, year, month,
	day, category and price. If the information is not correct, an error message
	detailing the error will appear. If it's correct, a success message will appear.


#### See expenses (Ver gastos):
	Here you can see and filter your expenses by day, month and year.
	To do so, decide if you want to visualize your expenses yearly, montly or daily and press the corresponding radio button.
	Then choose the date that you want to check and press "search"(Buscar).
	If you don't have recorded expenses on that period of time, an error message will tell you and
	no expenses will be shown.
	By default, this page will show you the expenses of the current month.
	The annual expenses will be shown in a table that displays month by month how much you spent. At the bottom of the table
	you can see the total expense for the year.
	The monthly expenses will be shown in a table that looks like a calendar. It shows you how much you spent in each day of the month
	that you choose. At the bottom you can see the total expense for the month.
	The daily expenses will also be shown in a table that is very similat to the annual expenses one. In this table you can see
	each individual expense with its respective name, category and price. At the bottom of the table the total expense of the day will
	be displayed.


#### Account (Cuenta):
	Here you can modify your annual budget and password. Your password can be anything. If you don't fill the field before submiting,
	an error message will appear. If change your budget or password successfully, a success message will appear.


#### App.py:
	This file manages the backend of the website as well as the functions that process the expenses and return how much the user spent
	in total in a day, month, or year.


Thank you for reading!

This was Budget.
