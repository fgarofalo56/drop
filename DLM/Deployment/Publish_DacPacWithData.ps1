#Reference Docs: https://docs.microsoft.com/en-us/sql/tools/sqlpackage/sqlpackage-publish?view=sql-server-ver15

$targetSQLServer        = 'demo-mdw-sqlsrv.database.windows.net'
$targetDatabase         = 'AdventureWorksDW2017'
$overWriteFiles         = 'true'
$targetUser             = Get-AzKeyVaultSecret -VaultName '<Enter KeyVault Name>' -Name '<Enter Secret Name for your UserName>' -AsPlainText
$targetUserPasssword    = Get-AzKeyVaultSecret -VaultName '<Enter KeyVault Name>' -Name '<Enter Secret Name for SQL Auth Password>' -AsPlainText
$workingPath            = 'C:\temp\sqlpackage'
$diagnostics            = 'false'
$blockDataLoss          = 'false'

#Make sure to use a tic mark ` befor any spaces in your package path
$sqlpackagePath         = 'C:\Program` Files\Microsoft` SQL` Server\150\DAC\bin'


# Set sqlpackage.exe dir: "C:\Program Files\Microsoft SQL Server\150\DAC\bin\sqlpackage.exe"
$sqlpackage = "$sqlpackagePath\sqlpackage.exe"

# Sets running params
$dacpac = "$workingPath\$targetDatabase.dacpac"

$params = "/a:Publish /sf:$dacpac /tsn:$targetSQLServer /tdn:$targetDatabase /tu:$targetUser /tp:$targetUserPasssword /Diagnostics:$diagnostics /OverwriteFiles:$overWriteFiles /SourceTrustServerCertificate:true /p:AllowIncompatiblePlatform=true /p:BlockOnPossibleDataLoss=$blockDataLoss"


Invoke-Expression -Command "$sqlpackage $params"