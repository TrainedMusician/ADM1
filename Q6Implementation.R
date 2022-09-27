library(data.table)
library(microbenchmark)

setwd('gitRepos/adm1/')

oldFile <- 'data/lineitem.tbl'
newFile <- 'data/jobbert.tbl'

system(paste('bash addColumns.sh', oldFile, newFile))

# # Q1
# columnsWithClasses <- list(
# 	character=c('l_returnflag', 'l_linestatus'),
# 	numeric = c('l_extendedprice', 'l_discount', 'l_tax'),
# 	integer = c('l_quantity', 'l_shipdate'),
# 	NULL = c('l_orderkey', 'l_partkey', 'l_suppkey', 'l_linenumber',
# 			 'l_commitdate', 'l_receiptdate', 'l_shipinstruct', 'l_shipmode',
# 			 'l_comment', 'V17')
# )

# Q6
columnsWithClasses <- list(
	numeric = c('l_extendedprice', 'l_discount'),
	integer = c('l_quantity', 'l_shipdate'),
	NULL = c('l_orderkey', 'l_partkey', 'l_suppkey', 'l_linenumber',
			 'l_commitdate', 'l_receiptdate', 'l_shipinstruct', 'l_shipmode',
			 'l_comment', 'V17', 'l_returnflag', 'l_linestatus', 'l_tax')
)

dt <- fread(newFile, sep = '|', colClasses = columnsWithClasses, header = TRUE)
microbenchmark(sum(dt[l_shipdate %between% c('1994-01-01', '1994-12-12') & l_discount %between% c(.05, .07) & l_quantity < 24, l_quantity * l_extendedprice]), unit = 's')
