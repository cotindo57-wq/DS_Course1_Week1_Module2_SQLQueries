import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect("data.sqlite")

# Step 1
df_boston = pd.read_sql(
    """
    SELECT
        e.firstName,
        e.lastName
    FROM employees e
    INNER JOIN offices o
        ON e.officeCode = o.officeCode
    WHERE o.city = 'Boston'
    """,
    conn
)

# Step 2
df_zero_emp = pd.read_sql(
    """
    SELECT 
        o.officeCode,
        o.city
    FROM offices o
    LEFT JOIN employees e
        ON o.officeCode = e.officeCode
    WHERE e.employeeNumber IS NULL
    """,
    conn
)

# Step 3
df_employee = pd.read_sql(
    """
    SELECT 
        e.firstName,
        e.lastName,
        o.city,
        o.state
    FROM employees e
    LEFT JOIN offices o
        ON e.officeCode = o.officeCode
    ORDER BY e.firstName, e.lastName
    """,
    conn
)

# Step 4
df_contacts = pd.read_sql(
    """
    SELECT
        c.contactFirstName,
        c.contactLastName,
        c.phone,
        c.salesRepEmployeeNumber
    FROM customers c
    LEFT JOIN orders o
        ON c.customerNumber = o.customerNumber
    WHERE o.orderNumber IS NULL
    ORDER BY c.contactLastName ASC
    """,
    conn
)

# Step 5
df_payment = pd.read_sql(
    """
    SELECT
        c.contactFirstName,
        c.contactLastName,
        p.amount,
        p.paymentDate
    FROM customers c
    INNER JOIN payments p
        ON c.customerNumber = p.customerNumber
    ORDER BY CAST(p.amount AS REAL) DESC
    """,
    conn
)

# Step 6
df_credit = pd.read_sql(
    """
    SELECT
        e.employeeNumber,
        e.firstName,
        e.lastName,
        COUNT(c.customerNumber) AS number_customers
    FROM employees e
    INNER JOIN customers c
        ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY e.employeeNumber, e.firstName, e.lastName
    HAVING AVG(c.creditLimit) > 90000
    ORDER BY number_customers DESC
    LIMIT 4
    """,
    conn
)

# Step 7
df_product_sold = pd.read_sql(
    """
    SELECT
        p.productName,
        COUNT(od.orderNumber) AS numorders,
        SUM(od.quantityOrdered) AS totalunits
    FROM products p
    INNER JOIN orderdetails od
        ON p.productCode = od.productCode
    GROUP BY p.productName
    ORDER BY totalunits DESC
    """,
    conn
)

# Step 8
df_total_customers = pd.read_sql(
    """
    SELECT
        p.productName,
        p.productCode,
        COUNT(DISTINCT o.customerNumber) AS numpurchasers
    FROM products p
    INNER JOIN orderdetails od
        ON p.productCode = od.productCode
    INNER JOIN orders o
        ON od.orderNumber = o.orderNumber
    GROUP BY p.productName, p.productCode
    ORDER BY numpurchasers DESC
    """,
    conn
)

# Step 9
df_customers = pd.read_sql(
    """
    SELECT
        o.officeCode,
        o.city,
        COUNT(c.customerNumber) AS n_customers
    FROM offices o
    LEFT JOIN employees e
        ON o.officeCode = e.officeCode
    LEFT JOIN customers c
        ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY o.officeCode, o.city
    """,
    conn
)

# Step 10
df_under_20 = pd.read_sql(
    """
    SELECT DISTINCT
        e.employeeNumber,
        e.firstName,
        e.lastName,
        o.city,
        o.officeCode
    FROM employees e
    INNER JOIN customers c
        ON e.employeeNumber = c.salesRepEmployeeNumber
    INNER JOIN orders ord
        ON c.customerNumber = ord.customerNumber
    INNER JOIN orderdetails od
        ON ord.orderNumber = od.orderNumber
    INNER JOIN offices o
        ON e.officeCode = o.officeCode
    WHERE od.productCode IN (
        SELECT
            od2.productCode
        FROM orderdetails od2
        INNER JOIN orders ord2
            ON od2.orderNumber = ord2.orderNumber
        GROUP BY od2.productCode
        HAVING COUNT(DISTINCT ord2.customerNumber) < 20
    )
    ORDER BY e.lastName ASC
    """,
    conn
)