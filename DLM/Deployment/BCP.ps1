#Refrance Links:
# https://docs.microsoft.com/en-us/sql/relational-databases/import-export/import-and-export-bulk-data-by-using-the-bcp-utility-sql-server?view=sql-server-ver15
# https://docs.microsoft.com/en-us/sql/tools/bcp-utility?view=sql-server-ver15

$bpcPath    = 'C:\Program` Files\Microsoft` SQL` Server\110\Tools\Binn'
$bpc        = "$bpcPath\bcp.exe"


$targetSQLServer        = '<Enter Target Server>'
$targetDatabase         = '<Enter Target Database>'

$targetUser             = '<Enter SQL Auth username>'
$targetUserPasssword    = '<Enter SQL Auth Password>'
$workingPath            = '<Enter Path of work Dir where Data bcp files are located>'

ForEach($dir in (dir $workingPath))
{
 ForEach($file in $dir.GetFiles()){
     $tableName = $dir.Name
     $fileName  = $file.Name
     $filePath  = $file.FullName
     $parms     = "`"$tableName`" IN `"$filePath`" -S `"$targetSQLServer`" -d `"$targetDatabase`" -U `"$targetUser`" -P `"$targetUserPasssword`" -n"
    Invoke-Expression -Command "$bpc $parms"
 }
}