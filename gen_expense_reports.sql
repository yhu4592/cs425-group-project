-- Generate expense reports
CREATE OR REPLACE VIEW ExpenseReports AS
    SELECT
        company_name,
        CAST(sum(annual_pay) AS DECIMAL(10,2)) AS total_wage_expenses,
        CAST(sum(bonus) AS DECIMAL(10,2)) AS total_bonus_expenses,
        CAST(sum(CASE
                WHEN contribution_401k >= 0.07
                THEN annual_pay * 0.07
                ELSE annual_pay * contribution_401k
                END
        ) AS DECIMAL(10,2)) AS total_401k_expenses,
        CAST(sum(CASE
                WHEN (salary_type='W2')
                THEN ss_deduction
                ELSE 0
                END
        ) AS DECIMAL(10,2)) AS total_ss_expenses,
        CAST(sum(employer_contribution) AS DECIMAL(10,2)) AS total_insurance_expenses
    FROM Employee NATURAL JOIN BenefitsPlan
    GROUP BY company_name
;
SELECT * FROM ExpenseReports;
