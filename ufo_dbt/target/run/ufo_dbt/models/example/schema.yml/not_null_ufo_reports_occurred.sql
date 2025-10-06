
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select occurred
from UFO.UFO.ufo_reports
where occurred is null



  
  
      
    ) dbt_internal_test