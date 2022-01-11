-- Generate bi-weekly paychecks
CREATE OR REPLACE VIEW Paychecks AS
    SELECT
        e_ssn,
        CAST(annual_pay / 26 AS DECIMAL(10,2)) AS total_pay,
        CAST(state_tax_rate * annual_pay / 26 AS DECIMAL(10,2)) AS state_tax_deduction,
        CAST((base_tax_owed + (annual_pay - lower_bound) * federal_tax_rate) / 26 AS DECIMAL(10,2)) AS federal_tax_deduction,
        CAST(ss_deduction / 26 AS DECIMAL(10,2)) AS ss_deduction,
        CAST(medicare_deduction / 26 AS DECIMAL(10,2)) AS medicare_deduction,
        CAST(contribution_401k * annual_pay / 26 AS DECIMAL(10,2)) AS deduction_401k,
        CAST(employee_contribution / 26 AS DECIMAL(10,2)) AS insurance_deduction,
        CAST((annual_pay - state_tax_rate * annual_pay - base_tax_owed - (annual_pay - lower_bound) * federal_tax_rate - ss_deduction - medicare_deduction - contribution_401k * annual_pay - employee_contribution) / 26 AS DECIMAL(10,2)) AS net_income
    FROM Employee NATURAL JOIN StateTax NATURAL JOIN FederalTax NATURAL JOIN BenefitsPlan
;
GRANT SELECT ON Paychecks TO manager;
GRANT SELECT ON Paychecks TO employee;
SELECT * FROM Paychecks;
