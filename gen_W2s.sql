-- Generate W2 forms
CREATE OR REPLACE VIEW W2s AS
    SELECT
        e_ssn,
        annual_pay,
        CAST(state_tax_rate * annual_pay AS DECIMAL(10,2)) AS state_tax_deduction,
        CAST((base_tax_owed + (annual_pay - lower_bound) * federal_tax_rate) AS DECIMAL(10,2)) AS federal_tax_deduction,
        ss_deduction,
        medicare_deduction,
        CAST(contribution_401k * annual_pay AS DECIMAL(10,2)) AS deduction_401k,
        CAST(employee_contribution AS DECIMAL(10,2)) AS insurance_deduction,
        bonus,
        CAST(annual_pay - state_tax_rate * annual_pay - base_tax_owed - (annual_pay - lower_bound) * federal_tax_rate - ss_deduction - medicare_deduction - contribution_401k * annual_pay - employee_contribution + bonus AS DECIMAL(10,2)) AS net_income
    From Employee NATURAL JOIN StateTax NATURAL JOIN FederalTax NATURAL JOIN BenefitsPlan
;
SELECT * FROM W2s;
