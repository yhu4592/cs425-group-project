import psycopg2

# Establish an ODBC connection to the PostgreSQL server and return the connection and cursor
def makeConnection(username, password):
  try:
    conn = psycopg2.connect(
      host="localhost",
      port="5432",
      database="postgres",
      user=username, # postgres
      password=password) # admin
    cur = conn.cursor()
    return (conn, cur)
  except Exception as e:
    print("Failed to connect to database with exception:")
    print(e)
    quit()

# Reads sql file as string and execute it
init_code = ""
def initDatabase():
  conn, cur = makeConnection("postgres", "admin")
  init_file = open("code.sql", mode="r")
  init_code = init_file.read()
  init_file.close()
  cur.execute(init_code)
  conn.commit()
  if conn is not None:
    conn.close()

# Generate W2 function; executes gen_W2s.sql file
def generateW2s():
  try:
    w2_file = open("gen_W2s.sql", mode="r")
    w2_code = w2_file.read()
    w2_file.close()
    cur.execute(w2_code)
    conn.commit()
    row = cur.fetchone()
    print("e_ssn, annual_pay, state_tax_deduction, federal_tax_deduction, ss_deduction, medicare_deduction, deduction_401k, insurance_deduction, bonus, net_income")
    while row:
      for col in row:
        print(col, sep=" ", end=", ")
      print()
      row = cur.fetchone()
  except Exception as e:
    print("Failed to generate W2s with exception:")
    print(e)

# Generate Expense Reports function; executes gen_expense_reports.sql file
def generateExpenseReports():
  try:
    expense_file = open("gen_expense_reports.sql", mode="r")
    expense_code = expense_file.read()
    expense_file.close()
    cur.execute(expense_code)
    conn.commit()
    row = cur.fetchone()
    print("total_wage_expenses, total_bonus,expenses, total_401k_expenses, total_ss_expenses, total_insurance_expenses")
    while row:
      for col in row:
        print(col, sep=" ", end=", ")
      print()
      row = cur.fetchone()
  except Exception as e:
    print("Failed to generate expense reports with exception:")
    print(e)

# Generate Paychecks function; executes gen_paychecks.sql file
def generatePaychecks():
  try:
    paycheck_file = open("gen_paychecks.sql", mode="r")
    paycheck_code = paycheck_file.read()
    paycheck_file.close()
    cur.execute(paycheck_code)
    conn.commit()
    row = cur.fetchone()
    print("e_ssn, total_pay, state_tax_deduction, federal_tax_deduction, ss_deduction, medicare_deduction, deduction_401k, insurance_deduction, net_income")
    while row:
      for col in row:
        print(col, sep=" ", end=", ")
      print()
      row = cur.fetchone()
  except Exception as e:
    print("Failed to generate paychecks with exception:")
    print(e)

# Add an employee to the employee table
def addEmployee(employee_code):
  try:
    cur.execute(employee_code)
    conn.commit()
    print("Employee info added")
  except Exception as e:
    print("Failed to add employee with exception:")
    print(e)

# Update an employee's information
def updateEmployeeInformation(e_ssn, attribute_name, attribute_value):
  try:
    update_employee_file = open("update_employee_attribute.sql", mode="r")
    update_employee_code = update_employee_file.read()
    update_employee_file.close()
    update_employee_code = update_employee_code.replace("__ATTRIBUTE__", attribute_name)
    update_employee_code = update_employee_code.replace("__SSN__", e_ssn)
    attribute_name = attribute_name.lower()
    if not (attribute_name == 'annual_pay' or attribute_name == 'bonus_percent' or attribute_name == 'tax_year' or attribute_name == 'benefits_plan_id'):
      attribute_value = "'" + attribute_value + "'"
    update_employee_code = update_employee_code.replace("__VALUE__", attribute_value)
    cur.execute(update_employee_code)
    conn.commit()
    print("Employee info updated")
  except Exception as e:
    print("Failed to update employee info with exception:")
    print(e)

# Read the information from a table
def readTable(table_name):
  try:
    read_table_file = open("read_table.sql", mode="r")
    read_table_code = read_table_file.read()
    read_table_file.close()
    read_table_code = read_table_code.replace("__TABLE_NAME__", table_name)
    cur.execute(read_table_code)
    row = cur.fetchone()
    while row:
      for col in row:
        print(col, sep=" ", end=", ")
      print()
      row = cur.fetchone()
  except Exception as e:
    print("Table not found with exception:")
    print(e)

# Show most recently generated paycheck report (manager rights)
def showPaychecks():
  try:
    print("e_ssn, total_pay, state_tax_deduction, federal_tax_deduction, ss_deduction, medicare_deduction, deduction_401k, insurance_deduction, net_income")
    readTable("paychecks")
    row = cur.fetchone()
    while row:
      for col in row:
        print(col, sep=" ", end=", ")
      print()
      row = cur.fetchone()
  except Exception as e:
    print("No paychecks have been generated with exception:")
    print(e)

# Show the specific employee's paycheck
def showEmployeePaycheck():
  try:
    read_table_file = open("read_table.sql", mode="r")
    read_table_code = read_table_file.read()
    read_table_file.close()
    read_table_code = read_table_code.replace("__TABLE_NAME__", "Paychecks")
    read_table_code += "WHERE e_ssn = " + e_ssn
    cur.execute(read_table_code)
    row = cur.fetchone()
    print("e_ssn, total_pay, state_tax_deduction, federal_tax_deduction, ss_deduction, medicare_deduction, deduction_401k, insurance_deduction, net_income")
    print(str(row).replace("Decimal", "").replace("('", "").replace("')", ""))
  except Exception as e:
    conn.commit()
    print("Failed to show employee paycheck with exception: ")
    print(e)

# Show employee info given SSN
def showEmployeeInfo():
  try:
    read_table_file = open("read_table.sql", mode="r")
    read_table_code = read_table_file.read()
    read_table_file.close()
    read_table_code = read_table_code.replace("__TABLE_NAME__", "employee")
    read_table_code += "WHERE e_ssn = " + e_ssn
    cur.execute(read_table_code)
    row = cur.fetchone()
    print("e_ssn, first_name, last_name, address, job_title, salary_type, annual_pay, bonus_percent, performance, company_name, tax_year, bracket, state_name, benefits_plan_ID")
    print(str(row).replace("Decimal", "").replace("('", "").replace("')", ""))
  except Exception as e:
    print("Employee SSN not found with exception:")
    print(e)

# Show an employee's dependents
def showEmployeeDependents():
  show_dependents_file = open("show_dependents.sql", mode="r")
  show_dependents_code = show_dependents_file.read()
  show_dependents_file.close()
  show_dependents_code = show_dependents_code.replace("__E_SSN__", e_ssn)
  cur.execute(show_dependents_code)
  row = cur.fetchone()
  if row:
    print("d_ssn, d_name, relation_to_employee, e_ssn, benefits_plan_ID")
  while row:
    for col in row:
      print(col, sep=" ", end=", ")
    print()
    row = cur.fetchone()

# Get credentials from the user
username = input("Enter username: ")
if (username.lower() == "init"):
  initDatabase()

password = input("Enter password: ")

e_ssn = ""
if username == "employee":
  e_ssn = input("Enter your employee SSN: ")

conn, cur = makeConnection(username, password)

# CHECK USER ROLE TO PICK MENU

# Administrator Menu
if username == "administrator":
  while True:
    print()
    print("[1] Add Employee")
    print("[2] Update Information")
    print("[3] Generate report")
    print("[4] View table")
    print("[Q] Exit")
    mainMenuButton = input("Enter your choice: ")

    # Admin Main Menu [1] - Add Employee
    if (mainMenuButton == "1"):

      # Enter Employee Information
      e_ssn = input("Enter employee ssn: ")
      first_name = input("Enter employee first name: ")
      last_name = input("Enter employee last name: ")
      address = input("Enter employee address: ")
      job_title = input("Enter employee job title: ")
      salary_type = input("Enter employee salary type ('W2' or 'hourly'): ")
      annual_pay = input("Enter employee annual pay: ")
      bonus_percent = input("Enter employee bonus percent: ")
      performance = input("Enter employee performance ('bad', 'ok', 'good', or 'super'): ")
      company_name = input("Enter employee company name (foreign keys must exist): ")
      tax_year = input("Enter employee tax year (foreign keys must exist): ")
      bracket = input("Enter employee tax bracket (foreign keys must exist): ")
      state_name = input("Enter employee state name (foreign keys must exist): ")
      benefits_plan_ID = input("Enter employee benefits plan ID (foreign keys must exist): ")

      # Read Insert SQL statement
      employee_file = open("add_employee.sql", mode="r")
      employee_code = employee_file.read()
      employee_file.close()

      # Replace query placeholders with user input
      employee_code = employee_code.replace("__E_SSN__", e_ssn)
      employee_code = employee_code.replace("__FIRST_NAME__", first_name)
      employee_code = employee_code.replace("__LAST_NAME__", last_name)
      employee_code = employee_code.replace("__ADDRESS__", address)
      employee_code = employee_code.replace("__JOB_TITLE__", job_title)
      employee_code = employee_code.replace("__SALARY_TYPE__", salary_type)
      employee_code = employee_code.replace("__ANNUAL_PAY__", annual_pay)
      employee_code = employee_code.replace("__BONUS_PERCENT__", bonus_percent)
      employee_code = employee_code.replace("__PERFORMANCE__", performance)
      employee_code = employee_code.replace("__COMPANY_NAME__", company_name)
      employee_code = employee_code.replace("__TAX_YEAR__", tax_year)
      employee_code = employee_code.replace("__BRACKET__", bracket)
      employee_code = employee_code.replace("__STATE_NAME__", state_name)
      employee_code = employee_code.replace("__BENEFITS_PLAN_ID__", benefits_plan_ID)

      # Add Employee to Table
      addEmployee(employee_code)
      print("Employee added.")

    # Admin Main Menu [2] - Update Information
    elif (mainMenuButton == "2"):
      print("[1] Raise")
      print("[2] Worker Address")
      print("[3] Performance Evaluation")
      print("[4] Bonus")
      updateButton = input("Choose a update option: ")

      # Give a raise
      if (updateButton == "1"):
        employee_ssn = input("Enter employee's SSN: ")
        attr_value = input("Enter new salary: ")
        updateEmployeeInformation(employee_ssn, 'annual_pay', attr_value)

      # Update an address
      elif (updateButton == "2"):
        employee_ssn = input("Enter employee's SSN: ")
        attr_value = input("Enter new address: ")
        updateEmployeeInformation(employee_ssn, 'address', attr_value)

      # Fill out performance evaluation
      elif (updateButton == "3"):
        employee_ssn = input("Enter employee's SSN: ")
        attr_value = input("Enter new performance evaluation ('bad', 'ok', 'good', or 'super'): ")
        updateEmployeeInformation(employee_ssn, 'performance', attr_value)

      # Set bonus
      elif (updateButton == "4"):
        employee_ssn = input("Enter employee's SSN: ")
        attr_value = input("Enter new bonus percent: ")
        updateEmployeeInformation(employee_ssn, 'bonus_percent', attr_value)

    # Admin Main Menu [3] - Generate Reports
    elif (mainMenuButton == "3"):
      print("[1] W2 Report")
      print("[2] Expense Report")
      print("[3] BiWeekly Paycheck")

      # Choose Report to Generate
      reportButton = input("Press the report to generate: ")

      # Generates W2
      if (reportButton == "1"):
        generateW2s()

      # Generates Expense Reports
      elif (reportButton == "2"):
        generateExpenseReports()

      # Generates Paychecks
      elif (reportButton == "3"):
        generatePaychecks()

    # Admin Main Menu [4] - View Table
    elif (mainMenuButton == "4"):
      table_name = input("Enter a table name: ")
      readTable(table_name)

    elif (mainMenuButton.lower() == "q"):
      break

# Manager Menu
if username == "manager":
  while True:
    print()
    print("[1] Update Information")
    print("[2] View Employees")
    print("[3] Show Paychecks")
    print("[Q] Exit")
    mainMenuButton = input("Enter your choice: ")

    # Manager Main Menu [1] - Update Information
    if (mainMenuButton == "1"):
      print("[1] Raise")
      print("[2] Worker Address")
      print("[3] Performance Evaluation")
      updateButton = input("Choose a update option: ")
      # Give a raise
      if (updateButton == "1"):
        employee_ssn = input("Enter employee's SSN: ")
        attr_value = input("Enter new salary: ")
        updateEmployeeInformation(employee_ssn, 'annual_pay', attr_value)
      # Update an address
      elif (updateButton == "2"):
        employee_ssn = input("Enter employee's SSN: ")
        attr_value = input("Enter new address: ")
        updateEmployeeInformation(employee_ssn, 'address', attr_value)
      # Fill out performance evaluation
      elif (updateButton == "3"):
        employee_ssn = input("Enter employee's SSN: ")
        attr_value = input("Enter new performance evaluation ('bad', 'ok', 'good', or 'super'): ")
        updateEmployeeInformation(employee_ssn, 'performance', attr_value)

    # Manager Main Menu [2] - View Employees
    elif (mainMenuButton == "2"):
      readTable("employee")

    # Manager Main Menu [3] - Show Paychecks
    elif (mainMenuButton == "3"):
      showPaychecks()

    elif (mainMenuButton.lower() == "q"):
      break

# Employee Menu
if username == "employee":
  while True:
    print()
    print("[1] Sign Up")
    print("[2] View Your Information")
    print("[3] Update Your Information")
    print("[4] View Your Paycheck")
    print("[Q] Exit")
    mainMenuButton = input("Enter your choice: ")

    # Employee Main Menu [1] - Sign up
    if (mainMenuButton == "1"):
      # Confirm that the employee isn't already added
      cur.execute("SELECT COUNT(e_ssn) FROM Employee WHERE e_ssn = " + e_ssn)
      row = cur.fetchone()
      if row[0] != 0:
        print("Employee is already registered")
        continue

      # Employees are not allow to enter certain information (i.e. Managers / Administrators will fill these in later)
      first_name = input("Enter your first name: ")
      last_name = input("Enter your last name: ")
      address = input("Enter your address: ")
      job_title = "Unemployed"
      salary_type = "W2"
      annual_pay = "0"
      bonus_percent = "0"
      performance = "ok"
      company_name = "Unemployed"
      tax_year = "2020"
      bracket = "$0 - $9,875"
      state_name = input("Enter your state name (foreign keys must exist): ")
      benefits_plan_ID = input("Enter your benefits plan ID (foreign keys must exist): ")

      # Read Insert SQL statement
      employee_file = open("add_employee.sql", mode="r")
      employee_code = employee_file.read()
      employee_file.close()

      # Replace query placeholders with user input
      employee_code = employee_code.replace("__E_SSN__", e_ssn)
      employee_code = employee_code.replace("__FIRST_NAME__", first_name)
      employee_code = employee_code.replace("__LAST_NAME__", last_name)
      employee_code = employee_code.replace("__ADDRESS__", address)
      employee_code = employee_code.replace("__JOB_TITLE__", job_title)
      employee_code = employee_code.replace("__SALARY_TYPE__", salary_type)
      employee_code = employee_code.replace("__ANNUAL_PAY__", annual_pay)
      employee_code = employee_code.replace("__BONUS_PERCENT__", bonus_percent)
      employee_code = employee_code.replace("__PERFORMANCE__", performance)
      employee_code = employee_code.replace("__COMPANY_NAME__", company_name)
      employee_code = employee_code.replace("__TAX_YEAR__", tax_year)
      employee_code = employee_code.replace("__BRACKET__", bracket)
      employee_code = employee_code.replace("__STATE_NAME__", state_name)
      employee_code = employee_code.replace("__BENEFITS_PLAN_ID__", benefits_plan_ID)

      # Add Employee to Table
      addEmployee(employee_code)

    # Employee Main Menu [2] - View Employee Info
    if (mainMenuButton == "2"):
      showEmployeeInfo()
      print()
      showEmployeeDependents()

    # Employee Main Menu [3] - Update Information (name, benefit plan, address, dependent)
    elif (mainMenuButton == "3"):
      print("[1] Update First/Last Name")
      print("[2] Update Benefits Plan")
      print("[3] Update Address")
      print("[4] Add a dependent")
      print("[5] Remove a dependent")
      updateButton = input("Choose what information to update: ")

      # Update Name
      if (updateButton == "1"):
        newFirstName = input("Enter your new first name: ")
        newLastName = input("Enter your new last name: ")
        updateEmployeeInformation(e_ssn, 'first_name', newFirstName)
        updateEmployeeInformation(e_ssn, 'last_name', newLastName)

      # Update Benefits Plan
      elif (updateButton == "2"):
        newBenefitsPlanID = input("Enter a new benefits plan ID: ")
        updateEmployeeInformation(e_ssn, 'benefits_plan_ID', newBenefitsPlanID)

      # Update Address
      elif (updateButton == "3"):
        address = input("Enter new address: ")
        updateEmployeeInformation(e_ssn, 'address', address)

      # Add dependent
      elif (updateButton == "4"):
        d_ssn = input("Enter the SSN of the dependent to be added: ")
        d_name = input("Enter the name of the dependent to be added: ")
        d_relationship = input("Enter the relationship of the dependent to the employee: ")
        benefits_plan_ID = input("Enter the benefits plan ID of the dependent (must exist): ")
        try:
          cur.execute("INSERT INTO Dependent (d_ssn, d_name, relation_to_employee, e_ssn, benefits_plan_id) VALUES ('"
          + d_ssn + "', '" + d_name + "', '" + d_relationship + "', " + e_ssn + ", " + benefits_plan_ID + ");")
          conn.commit()
          print("Dependent added")
        except Exception as e:
          print("Failed to add dependent with exception:")
          print(e)

      # Remove a dependent
      elif (updateButton == "5"):
        try:
          d_ssn = input("Enter the SSN of the dependent to be removed: ")
          cur.execute("DELETE FROM Dependent WHERE d_ssn = " + d_ssn + " AND e_ssn = " + e_ssn)
          conn.commit()
          print("Dependent removed (if existed)")
        except Exception as e:
          print("Failed to remove dependent with exception:")
          print(e)

    # Employee Main Menu [4] - View Paycheck
    elif (mainMenuButton == "4"):
      showEmployeePaycheck()

    # Quit
    elif (mainMenuButton.lower() == "q"):
      break

# Close database connection
if conn is not None:
  conn.close()
