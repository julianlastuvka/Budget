This is the readme for my cs50 final proyect: Budget.

#### Video Demo: https://www.youtube.com/watch?v=PerFshL5L2w

#### Description: 
	Budget is a website that allows you to keep track of your expenses
	while making sure that you don't go over your budget.


#### Technologies used: 
	HTML, CSS and JS in the front-end. SQL and flask in the back-end.


#### Database: 
	I used a sql database with two tables to store the user information and history of expenses.
	The first table is called users and stores the user id, username, email, hash and annual budget.
	The second table is called history and stores the user id,
	name of expense, category, price anddate.


#### Functionalities:

## Register & Login: 
	This are self explanatory. If you don't fill all the fields
	or don't complete them correctly, an error message will pop up. 
	Once you register successfully, you'll be redirected to the login page.


## Budget (Presupuesto): 
	You can visualize your annualy and montly budget in the
	"see expenses" (Ver gastos) or "add expenses" (Agregar gastos) pages. If you
	want to change it, you can do so in the "account" (Cuenta) page. 


## Add expenses (Agregar gastos): 
	Here you can add your expenses one by one. To
	do so, fill the fields with the required information: expense name, year, month,
	day, category and price. If the information is not correct, an error message 
	detailing the error will appear. If it's correct, a success message will appear.


## See expenses (Ver gastos): 
	Here you can see and filter your expenses by day, month and year.
	To do so, decide if you want to visualize your expenses yearly, montly or daily and press the 	corresponding radio button. 
	Then choose the date that you want to check and press "search"(Buscar).
	If you don't have recorded expenses on that period of time, an error message will tell you and
	no expenses will be shown. 
	By default, this page will show you the expenses of the current month. 


## Account (Cuenta): Here you can modify your annual budget and password. Your password can be anything.


Thank you for reading! 

This was Budget.