-----------------------------------------------------------------------
-- Remove everything from previous sessions
-----------------------------------------------------------------------

-- Drop views
DROP VIEW IF EXISTS Paychecks;
DROP VIEW IF EXISTS W2s;
DROP VIEW IF EXISTS ExpenseReports;
-- Drop tables
DROP TABLE IF EXISTS Dependent;
DROP TABLE IF EXISTS Employee;
DROP TABLE IF EXISTS StateTax;
DROP TABLE IF EXISTS FederalTax;
DROP TABLE IF EXISTS Company;
DROP TABLE IF EXISTS BenefitsPlan;
-- Drop types
DROP TYPE IF EXISTS salary_type;
DROP TYPE IF EXISTS performance;


-----------------------------------------------------------------------
-- Custom types
-----------------------------------------------------------------------
CREATE TYPE salary_type AS ENUM ('hourly', 'W2');
CREATE TYPE performance AS ENUM ('super', 'good', 'ok', 'bad');


-----------------------------------------------------------------------
-- Table definitions
-----------------------------------------------------------------------

-- Benefits Plan Table
CREATE TABLE BenefitsPlan(
	benefits_plan_ID                NUMERIC(10,0) PRIMARY KEY,
	contribution_401k               NUMERIC(3,3) NOT NULL,
	attorney_plan                   VARCHAR(64),
	life_insurance_plan             VARCHAR(64),
	dental_plan                     VARCHAR(64),
	vision_plan                     VARCHAR(64),
	individual_premium_cost         NUMERIC(10,2),
	family_premium_cost             NUMERIC(10,2),
	employee_contribution           NUMERIC(10,2) NOT NULL,
	employer_contribution           NUMERIC(10,2) NOT NULL
);

-- Company Table
CREATE TABLE Company(
	company_name    VARCHAR(64) PRIMARY KEY,
	revenue         NUMERIC(20,2) NOT NULL
);

-- Federal Tax Table
CREATE TABLE FederalTax(
    tax_year				    NUMERIC(4,0),
    bracket 				    VARCHAR(64),
    base_tax_owed  			    NUMERIC(10,2) NOT NULL,
    federal_tax_rate 		    NUMERIC(10,2) NOT NULL,
    upper_bound 			    NUMERIC(10,2) NOT NULL,
    lower_bound			        NUMERIC(10,2) NOT NULL,
    PRIMARY KEY(tax_year, bracket)
);

-- State Tax Table
CREATE TABLE StateTax(
	state_name                      VARCHAR(64) PRIMARY KEY,
	state_tax_rate                  NUMERIC(4,4) NOT NULL
);

-- Employee Table
CREATE TABLE Employee(
    e_ssn                   NUMERIC(10,0) PRIMARY KEY,
    first_name              VARCHAR(64) NOT NULL,
    last_name               VARCHAR(64) NOT NULL,
    address                 VARCHAR(64) NOT NULL,
    job_title               VARCHAR(64) NOT NULL,
    salary_type             salary_type NOT NULL,
    annual_pay              NUMERIC(10,2) NOT NULL,
    bonus_percent           NUMERIC(4,3) NOT NULL,
    performance             performance NOT NULL,
    bonus                   NUMERIC(10,2) GENERATED ALWAYS AS (CASE
        WHEN salary_type='hourly' OR performance='bad'
            THEN 0
        WHEN performance='super'
            THEN (1.5 * bonus_percent * annual_pay)
 	 	WHEN performance='good'
            THEN (bonus_percent * annual_pay)
  	    WHEN performance='ok'
            THEN (0.5 * bonus_percent * annual_pay)
    	END ) STORED,
    ss_deduction           NUMERIC(10,2) GENERATED ALWAYS AS (CASE
        WHEN salary_type='hourly'
            THEN (0.15 * annual_pay)
        WHEN salary_type='W2'
            THEN (0.075 * annual_pay)
	    END ) STORED,
    medicare_deduction     NUMERIC(10,2) GENERATED ALWAYS AS (
        0.025 * annual_pay ) STORED,
    company_name            VARCHAR(64),
        CONSTRAINT fk_company_name FOREIGN KEY (company_name)
        REFERENCES Company(company_name) ON DELETE CASCADE,
    tax_year                NUMERIC(4,0),
    bracket                 VARCHAR(64),
        CONSTRAINT fk_federal_tax FOREIGN KEY(tax_year, bracket)
        REFERENCES FederalTax(tax_year, bracket) ON DELETE SET NULL,
    state_name              VARCHAR(64),
        CONSTRAINT fk_state_name FOREIGN KEY(state_name)
        REFERENCES StateTax(state_name) ON DELETE SET NULL,
    benefits_plan_ID        NUMERIC(10,0),
        CONSTRAINT fk_benefits_plan_ID FOREIGN KEY(benefits_plan_ID)
        REFERENCES BenefitsPlan(benefits_plan_ID) ON DELETE SET NULL
);

-- Dependent Table
Create table Dependent(
	d_ssn                           NUMERIC(10,0) PRIMARY KEY,
	d_name                          VARCHAR(64) NOT NULL,
    relation_to_employee            VARCHAR(64) NOT NULL,
    e_ssn                           NUMERIC(10,0),
        CONSTRAINT fk_ssn FOREIGN KEY(e_ssn)
        REFERENCES Employee(e_ssn) ON DELETE SET NULL,
    benefits_plan_ID                NUMERIC(10,0),
        CONSTRAINT fk_benefits_plan_ID FOREIGN KEY(benefits_plan_ID)
        REFERENCES BenefitsPlan(benefits_plan_ID) ON DELETE SET NULL
);


-----------------------------------------------------------------------
-- Create table indices for faster queries
-----------------------------------------------------------------------

CREATE INDEX employee_index_company_name ON Employee (company_name);
CREATE INDEX employee_index_federal_tax ON Employee (tax_year, bracket);
CREATE INDEX employee_index_state_name ON Employee (state_name);
CREATE INDEX employee_index_benefits_plan_id ON Employee (benefits_plan_ID);
CREATE INDEX employee_index_salary_type ON Employee (salary_type);
CREATE INDEX dependent_index_e_ssn ON Dependent (e_ssn);


-----------------------------------------------------------------------
-- Insert sample data into tables
-----------------------------------------------------------------------

-- BenefitsPlan sample data
INSERT INTO BenefitsPlan(benefits_plan_ID, contribution_401k, attorney_plan, life_insurance_plan, dental_plan, vision_plan,
                         individual_premium_cost, family_premium_cost, employee_contribution, employer_contribution) VALUES
    (1012345678, 0.06, 'MetLife', 'Northwestern Mutual', 'Bits, Nibbles, and Bytes', 'EyeMed', 1111, 1111, 1111, 1111),
    (3141592653, 0.08, 'LegalShield', 'Berkshire Farm', 'Bone Zone', '2020 Vision', 2222, 2222, 2222, 2222),
    (8675309, 0.04, 'NonProgressive', 'OrangeMed', 'DentalSalon', 'Eagle Eye', 3333, 3333, 3333, 3333)
;

-- Company sample data
INSERT INTO Company (company_name, revenue) VALUES
    ('Unemployed', 0),
    ('Johnson Inc.', 100000000),
    ('Trudy Center', 999999999),
    ('Wacker Street  Bank', 800000),
    ('Petes Pizza Clinic', 800000),
    ('Barington Mortuary', 3000000)
;

-- FederalTax sample data
INSERT INTO FederalTax (tax_year, bracket, base_tax_owed, federal_tax_rate, upper_bound, lower_bound) VALUES
    (2020, '$0 - $9,875', 0, 0.10, 9875, 0),
    (2020, '$9,876 - $40,125', 987.50, 0.12, 40125, 9876),
    (2020, '$40,126 - $85,525', 4617.50, 0.22, 85525, 40126),
    (2020, '$85,526 - $163,300', 14605.50, 0.24, 163300, 85526),
    (2020, '$163,301 - $207,350', 33271.50 , 0.32, 207350, 163301)
;

-- StateTax sample data
INSERT INTO StateTax(state_name, state_tax_rate) VALUES
    ('IL', 0.0625),
    ('NY', 0.04),
    ('CA', 0.0725)
;

-- Employee sample data
INSERT INTO Employee (e_ssn, first_name, last_name, address, job_title, salary_type, annual_pay, bonus_percent,
                      performance, company_name, tax_year, bracket, state_name, benefits_plan_ID) VALUES
    (111111111, 'Alice', 'Smith', '123 Fake Street', 'Accountant', 'W2', 85000, 0.125, 'super', 'Johnson Inc.', 2020, '$40,126 - $85,525', 'IL', 1012345678),
    (222222222, 'Bob', 'Johnson', '234 Fake Street', 'Administrator', 'W2', 120000, 0.45, 'ok', 'Johnson Inc.', 2020, '$85,526 - $163,300', 'NY', 1012345678),
    (333333333, 'Charles', 'Williams', '345 Fake Street', 'Janitor', 'hourly', 60000, 0.10, 'good', 'Johnson Inc.', 2020, '$40,126 - $85,525', 'CA', 8675309),
    (444444444, 'Daniel', 'Brown', '456 Fake Street', 'Customer support', 'W2', 20000, 0.15, 'bad', 'Trudy Center', 2020, '$9,876 - $40,125', 'IL', 8675309),
    (555555555, 'Ethan', 'Jones', '567 Fake Street', 'Tech support', 'hourly', 96000, 0.15, 'good', 'Trudy Center', 2020, '$85,526 - $163,300', 'NY', 3141592653)
;

-- Dependent sample data
INSERT INTO Dependent(d_ssn, d_name, relation_to_employee, e_ssn, benefits_plan_ID) VALUES
    (192837645, 'Xander', 'husband', 333333333, 8675309),
    (987654321, 'Ysabel', 'step sister in law', 222222222, 3141592653),
    (123456789, 'Zeke', 'son', 111111111, 1012345678)
;

-----------------------------------------------------------------------
-- Run queries to generate reports / views (MOVED TO SEPARATE FILES)
-----------------------------------------------------------------------

-- Generate bi-weekly paychecks
-- CREATE OR REPLACE VIEW Paychecks AS
--     SELECT
--         e_ssn,
--         CAST(annual_pay / 26 AS DECIMAL(10,2)) AS total_pay,
--         CAST(state_tax_rate * annual_pay / 26 AS DECIMAL(10,2)) AS state_tax_deduction,
--         CAST((base_tax_owed + (annual_pay - lower_bound) * federal_tax_rate) / 26 AS DECIMAL(10,2)) AS federal_tax_deduction,
--         CAST(ss_deduction / 26 AS DECIMAL(10,2)) AS ss_deduction,
--         CAST(medicare_deduction / 26 AS DECIMAL(10,2)) AS medicare_deduction,
--         CAST(contribution_401k * annual_pay / 26 AS DECIMAL(10,2)) AS deduction_401k,
--         CAST(employee_contribution / 26 AS DECIMAL(10,2)) AS insurance_deduction,
--         CAST((annual_pay - state_tax_rate * annual_pay - base_tax_owed - (annual_pay - lower_bound) * federal_tax_rate - ss_deduction - medicare_deduction - contribution_401k * annual_pay - employee_contribution) / 26 AS DECIMAL(10,2)) AS net_income
--     FROM Employee NATURAL JOIN StateTax NATURAL JOIN FederalTax NATURAL JOIN BenefitsPlan
-- ;

-- -- Generate W2 forms
-- CREATE OR REPLACE VIEW W2s AS
--     SELECT
--         e_ssn,
--         annual_pay,
--         CAST(state_tax_rate * annual_pay AS DECIMAL(10,2)) AS state_tax_deduction,
--         CAST((base_tax_owed + (annual_pay - lower_bound) * federal_tax_rate) AS DECIMAL(10,2)) AS federal_tax_deduction,
--         ss_deduction,
--         medicare_deduction,
--         CAST(contribution_401k * annual_pay AS DECIMAL(10,2)) AS deduction_401k,
--         CAST(employee_contribution AS DECIMAL(10,2)) AS insurance_deduction,
--         bonus,
--         CAST(annual_pay - state_tax_rate * annual_pay - base_tax_owed - (annual_pay - lower_bound) * federal_tax_rate - ss_deduction - medicare_deduction - contribution_401k * annual_pay - employee_contribution + bonus AS DECIMAL(10,2)) AS net_income
--     From Employee NATURAL JOIN StateTax NATURAL JOIN FederalTax NATURAL JOIN BenefitsPlan
-- ;

-- -- Generate expense reports
-- CREATE OR REPLACE VIEW ExpenseReports AS
--     SELECT
--         company_name,
--         CAST(sum(annual_pay) AS DECIMAL(10,2)) AS total_wage_expenses,
--         CAST(sum(bonus) AS DECIMAL(10,2)) AS total_bonus_expenses,
--         CAST(sum(CASE
--                 WHEN contribution_401k >= 0.07
--                 THEN annual_pay * 0.07
--                 ELSE annual_pay * contribution_401k
--                 END
--         ) AS DECIMAL(10,2)) AS total_401k_expenses,
--         CAST(sum(CASE
--                 WHEN (salary_type='W2')
--                 THEN ss_deduction
--                 ELSE 0
--                 END
--         ) AS DECIMAL(10,2)) AS total_ss_expenses,
--         CAST(sum(employer_contribution) AS DECIMAL(10,2)) AS total_insurance_expenses
--     FROM Employee NATURAL JOIN BenefitsPlan
--     GROUP BY company_name
-- ;

-----------------------------------------------------------------------
-- Create role for users which are allowed to generate reports
-----------------------------------------------------------------------
DROP OWNED BY administrator;
DROP USER IF EXISTS administrator;
DROP USER IF EXISTS manager;
DROP USER IF EXISTS employee;

CREATE USER administrator WITH PASSWORD '11111';
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO administrator;
GRANT CREATE ON DATABASE postgres TO administrator;

CREATE USER manager WITH PASSWORD '22222';
GRANT SELECT, UPDATE, DELETE ON Employee TO manager;

CREATE USER employee WITH PASSWORD '33333';
GRANT SELECT, INSERT ON Employee TO employee;
GRANT UPDATE (first_name, last_name, benefits_plan_ID, address) ON Employee TO employee;
GRANT SELECT, INSERT, DELETE ON Dependent TO employee;
