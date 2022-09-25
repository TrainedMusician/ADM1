COPY           5 RECORDS INTO region   FROM '/data/ADM/region.tbl'      USING DELIMITERS '|', '|\n';
COPY          25 RECORDS INTO nation   FROM '/data/ADM/nation.tbl'      USING DELIMITERS '|', '|\n';
COPY       10000 RECORDS INTO supplier FROM '/data/ADM/supplier.tbl'    USING DELIMITERS '|', '|\n';
COPY      150000 RECORDS INTO customer FROM '/data/ADM/customer.tbl'    USING DELIMITERS '|', '|\n';
COPY      200000 RECORDS INTO part     FROM '/data/ADM/part.tbl'        USING DELIMITERS '|', '|\n';
COPY      800000 RECORDS INTO partsupp FROM '/data/ADM/partsupp.tbl'    USING DELIMITERS '|', '|\n';
COPY     1500000 RECORDS INTO orders   FROM '/data/ADM/orders.tbl'      USING DELIMITERS '|', '|\n';
COPY     6001215 RECORDS INTO lineitem FROM '/data/ADM/lineitem.tbl'    USING DELIMITERS '|', '|\n';
