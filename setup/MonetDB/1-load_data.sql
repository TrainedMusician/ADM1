COPY INTO region   FROM '/data/ADM/region.tbl'      USING DELIMITERS '|', '|\n';
COPY INTO nation   FROM '/data/ADM/nation.tbl'      USING DELIMITERS '|', '|\n';
COPY INTO supplier FROM '/data/ADM/supplier.tbl'    USING DELIMITERS '|', '|\n';
COPY INTO customer FROM '/data/ADM/customer.tbl'    USING DELIMITERS '|', '|\n';
COPY INTO part     FROM '/data/ADM/part.tbl'        USING DELIMITERS '|', '|\n';
COPY INTO partsupp FROM '/data/ADM/partsupp.tbl'    USING DELIMITERS '|', '|\n';
COPY INTO orders   FROM '/data/ADM/orders.tbl'      USING DELIMITERS '|', '|\n';
COPY INTO lineitem FROM '/data/ADM/lineitem.tbl'    USING DELIMITERS '|', '|\n';
