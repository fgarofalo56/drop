#Reference Docs: https://docs.microsoft.com/en-us/sql/tools/sqlpackage/sqlpackage-publish?view=sql-server-ver15

$targetSQLServer        = '<Enter Target Server Address>'
$targetDatabase         = '<Enter Target DB Name>'
$overWriteFiles         = 'true'
$targetUser             = "<Enter Target SQL Auth User"
$targetUserPasssword    = '<Enter Target User Password' 
$workingPath            = 'C:\temp\sqlpackage'
$diagnostics            = 'false'
#Make sure to use a tic mark ` befor any spaces in your package path
$sqlpackagePath         = 'C:\Program` Files\Microsoft` SQL` Server\150\DAC\bin'


# Set sqlpackage.exe dir: "C:\Program Files\Microsoft SQL Server\150\DAC\bin\sqlpackage.exe"
$sqlpackage = "$sqlpackagePath\sqlpackage.exe"

# Sets running params
$dacpac = "$workingPath\$sourceDatabase.dacpac"

$params = "/a:Publish /sf:$dacpac /tsn:$targetSQLServer /tdn:$targetDatabase /tu:$targetUser /tp:$targetUserPasssword /Diagnostics:$diagnostics /OverwriteFiles:$overWriteFiles /SourceTrustServerCertificate:true"
Invoke-Expression -Command "$sqlpackage $params"
