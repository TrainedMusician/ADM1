COPY           5 RECORDS INTO region   FROM '/data/ADM/SF-1/region.tbl'      USING DELIMITERS '|', '|\n';
COPY          25 RECORDS INTO nation   FROM '/data/ADM/SF-1/nation.tbl'      USING DELIMITERS '|', '|\n';
COPY       10000 RECORDS INTO supplier FROM '/data/ADM/SF-1/supplier.tbl'    USING DELIMITERS '|', '|\n';
COPY      150000 RECORDS INTO customer FROM '/data/ADM/SF-1/customer.tbl'    USING DELIMITERS '|', '|\n';
COPY      200000 RECORDS INTO part     FROM '/data/ADM/SF-1/part.tbl'        USING DELIMITERS '|', '|\n';
COPY      800000 RECORDS INTO partsupp FROM '/data/ADM/SF-1/partsupp.tbl'    USING DELIMITERS '|', '|\n';
COPY     1500000 RECORDS INTO orders   FROM '/data/ADM/SF-1/orders.tbl'      USING DELIMITERS '|', '|\n';
COPY     6001215 RECORDS INTO lineitem FROM '/data/ADM/SF-1/lineitem.tbl'    USING DELIMITERS '|', '|\n';
