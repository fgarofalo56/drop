#Reference Docs: https://docs.microsoft.com/en-us/sql/tools/sqlpackage/sqlpackage-extract?view=sql-server-ver15
$sourceSQLserver        = '<Enter Source SQL Server>'
$sourceDatabase         = '<Enter Source DB Name>'
$sourceUser             = "<Enter Source SQL Ser User Name"
$sourceUserPasssword    = '<Enter SQL Auth Password >' 
$workingPath            = 'C:\temp\sqlpackage'
#Make sure to use a tic mark ` befor any spaces in your package path
$sqlpackagePath         = 'C:\Program` Files\Microsoft` SQL` Server\150\DAC\bin'
#Set AllTables to true to extact all user tables, or set to false and pass list of tables
#if picking tables to extract set AllTables to false
$ExtractAllTableData    = $false

#To pick tables add them to tableNames.txt file otherwise extract all
#You can use T-SQL to build your list, for example:  select '['+TABLE_SCHEMA+'].['+TABLE_NAME+'], ' from INFORMATION_SCHEMA.TABLES where TABLE_TYPE = N'BASE TABLE'
#Copy and Paste the output into tableNames.txt
$tablesData             = Get-Content '.\DLM\AzureSQLDB\DatabaseProjects\Deployment\tableNames.txt'
# Set sqlpackage.exe dir: "C:\Program Files\Microsoft SQL Server\150\DAC\bin\sqlpackage.exe"
$sqlpackage = "$sqlpackagePath\sqlpackage.exe"

# Sets running params
$dacpac = "$workingPath\$sourceDatabase.dacpac"

If($ExtractAllTableData){
  $params = "/a:Extract /tf:$dacpac /ssn:$sourceSQLserver /sdn:$sourceDatabase /su:$sourceUser /sp:$sourceUserPasssword /p:IgnoreUserLoginMappings=true /p:ExtractAllTableData=true"
  Invoke-Expression -Command "$sqlpackage $params"
}Else{
$tables = ''
ForEach($_ in $tablesData){
    $tables +=  ("/p:TableData=$_ ") 
}
$params = "/a:Extract /tf:$dacpac /ssn:$sourceSQLserver /sdn:$sourceDatabase /su:$sourceUser /sp:$sourceUserPasssword /p:IgnoreUserLoginMappings=true $tables/p:ExtractAllTableData=false"
#run sqlpackage
Invoke-Expression -Command "$sqlpackage $params"
}

