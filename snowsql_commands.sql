show stages;

list @UTIL_DB.PUBLIC.MY_INTERNAL_NAMED_STAGE;

select $1 from @UTIL_DB.PUBLIC.MY_INTERNAL_NAMED_STAGE/test_internal_stage_file1.txt;

use role pc_rivery_role;
use warehouse pc_rivery_wh;

create or replace TABLE PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST (
	FRUIT_NAME VARCHAR(25)
);

insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST
values ('banana')
, ('cherry')
, ('strawberry')
, ('pineapple')
, ('apple')
, ('mango')
, ('coconut')
, ('plum')
, ('avocado')
, ('starfruit');
