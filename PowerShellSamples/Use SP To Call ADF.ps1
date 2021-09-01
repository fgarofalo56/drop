#Get Auth Token
$clientid       = "Enter Your Client ID"
$clientSecret   = "Enter Your Client Secret"
$tenantID       = "Enter Your Tenant ID"
$authURI        = "https://login.microsoftonline.com/"+$tenantID+"/oauth2/token"
$resource       = "https://management.core.windows.net/"
$contentType    = "application/x-www-form-urlencoded"

#Get token if needed for managment APIs can be used for managment of Azure Services and other options like listing what API are aviable.
$body = @{
    grant_type = "client_credentials"
    client_id = $clientid
    client_secret = $clientSecret  
    resource = $resource      
}
$parms = @{
    ContentType = $contentType
    Headers     = @{'Content-Type' = $contentType}
    Method      = 'POST'
    Body        = $body
    URI         = $authURI
}
$token = Invoke-WebRequest @parms 
$authToken = ($token.Content | convertfrom-json | Select-object access_token).access_token



#Univerisal Params  (set to be used for all API Calls)
$subscriptionId = "Enter Your SubscriptionId"
$resourceGroupName = "Enter Your Resource Group Name"
$apiVersion     = "2018-06-01"
$baseURI        = "management.azure.com/subscriptions/"
$contentType    = "application/json"


#List ADF API Operations
$uri                = "https://management.azure.com/providers/Microsoft.DataFactory/operations?api-version=$($apiVersion)"
$parms = @{
    ContentType = $contentType
    Headers     = @{'Content-Type' = $contentType; 'Authorization' = 'Bearer '+ $authToken}
    Method      = 'GET'
    URI         = $uri
    Verbose    = $true}
$status = Invoke-RestMethod @parms 
$status.value


#ADF version 2: https://docs.microsoft.com/en-us/rest/api/datafactory/v2
#Get Factories
$api                = "factories"
$uri                = "https://$($baseURI)$($subscriptionId)/resourceGroups/$($resourceGroupName)/providers/Microsoft.DataFactory/$($api)?api-version=$($apiVersion)"
$parms = @{
    ContentType = $contentType
    Headers     = @{'Content-Type' = $contentType; 'Authorization' = 'Bearer '+ $authToken}
    Method      = 'GET'
    URI         = $uri
    Verbose    = $true}
$status = Invoke-RestMethod @parms 
$status.value


#Get Factory Detial
$factoryName    = "Enter Your ADF Factory Name"
$api            = "factories/$($factoryName)"
$uri            = "https://$($baseURI)$($subscriptionId)/resourceGroups/$($resourceGroupName)/providers/Microsoft.DataFactory/$($api)?api-version=$($apiVersion)"
$parms = @{
    ContentType = $contentType
    Headers     = @{'Content-Type' = $contentType; 'Authorization' = 'Bearer '+ $authToken}
    Method      = 'GET'
    URI         = $uri
    Verbose    = $true}
$status = Invoke-RestMethod @parms 
$status


#List Pipelines:
$factoryName    = "Enter Your ADF Factory Name"
$api            = "factories/$($factoryName)/pipelines"
$uri            = "https://$($baseURI)$($subscriptionId)/resourceGroups/$($resourceGroupName)/providers/Microsoft.DataFactory/$($api)?api-version=$($apiVersion)"
$parms = @{
    ContentType = $contentType
    Headers     = @{'Content-Type' = $contentType; 'Authorization' = 'Bearer '+ $authToken}
    Method      = 'GET'
    URI         = $uri
    Verbose    = $true}
$status = Invoke-RestMethod @parms 
$Status.value


#Get Pipeline 
$pipelineName   = "Enter Your Pipeline Name"
$factoryName    = "Enter Your ADF Factory Name"
$api            = "factories/$($factoryName)/pipelines/$($pipelineName)"
$uri            = "https://$($baseURI)$($subscriptionId)/resourceGroups/$($resourceGroupName)/providers/Microsoft.DataFactory/$($api)?api-version=$($apiVersion)"
$parms = @{
    ContentType = $contentType
    Headers     = @{'Content-Type' = $contentType; 'Authorization' = 'Bearer '+ $authToken}
    Method      = 'GET'
    URI         = $uri
    Verbose    = $true}
$status = Invoke-RestMethod @parms 
$Status


#Get Pipeline Activity Runs
$factoryName    = "Enter Your ADF Factory Name"
$api            = "factories/$($factoryName)/queryPipelineRuns"
$uri            = "https://$($baseURI)$($subscriptionId)/resourceGroups/$($resourceGroupName)/providers/Microsoft.DataFactory/$($api)?api-version=$($apiVersion)"
$parms = @{
    ContentType = $contentType
    Headers     = @{'Content-Type' = $contentType; 'Authorization' = 'Bearer '+ $authToken}
    Method      = 'GET'
    URI         = $uri
    Verbose    = $true}
$status = Invoke-RestMethod @parms 
$Status



#Run Pipeline: https://docs.microsoft.com/en-us/rest/api/datafactory/pipelines/createrun
$pipelineName   = "Enter Your Pipeline Name"
$factoryName    = "Enter Your ADF Factory Name"
$api            = "factories/$($factoryName)/pipelines/$($pipelineName)/createRun"
$uri            = "https://$($baseURI)$($subscriptionId)/resourceGroups/$($resourceGroupName)/providers/Microsoft.DataFactory/$($api)?api-version=$($apiVersion)"
$parms = @{
    ContentType = $contentType
    Headers     = @{'Content-Type' = $contentType; 'Authorization' = 'Bearer '+ $authToken}
    Method      = 'POST'
    URI         = $uri
    Verbose    = $true}
$status = Invoke-RestMethod @parms 
$status

#Get Pipeline by Run ID
$runId          = "Enter Your Run Id"
$factoryName    = "Enter Your ADF Factory Name"
$api            = "factories/$($factoryName)/pipelineruns/$($runId)"
$uri            = "https://$($baseURI)$($subscriptionId)/resourceGroups/$($resourceGroupName)/providers/Microsoft.DataFactory/$($api)?api-version=$($apiVersion)"
$parms = @{
    ContentType = $contentType
    Headers     = @{'Content-Type' = $contentType; 'Authorization' = 'Bearer '+ $authToken}
    Method      = 'Get'
    URI         = $uri
    Verbose    = $true}
$status = Invoke-RestMethod @parms 
$status

#Get Pipeline Runs
$factoryName    = "Enter Your ADF Factory Name"
$api            = "factories/$($factoryName)/pipelineruns"
$uri            = "https://$($baseURI)$($subscriptionId)/resourceGroups/$($resourceGroupName)/providers/Microsoft.DataFactory/$($api)?api-version=$($apiVersion)"
$parms = @{
    ContentType = $contentType
    Headers     = @{'Content-Type' = $contentType; 'Authorization' = 'Bearer '+ $authToken}
    Method      = 'Get'
    URI         = $uri
    Verbose    = $true}
$status = Invoke-RestMethod @parms 
$status



#Get Pipeline Runs by Factory (https://docs.microsoft.com/en-us/rest/api/datafactory/pipelineruns/querybyfactory)
$runId          = "Enter Your Run Id"
$factoryName    = "Enter Your ADF Factory Name"
$api            = "factories/$($factoryName)/queryPipelineRuns"
$uri            = "https://$($baseURI)$($subscriptionId)/resourceGroups/$($resourceGroupName)/providers/Microsoft.DataFactory/$($api)?api-version=$($apiVersion)"
$body = @{
    lastUpdatedAfter = "2018-06-16T00:36:44.3345758Z"
}

$parms = @{
    ContentType = $contentType
    Headers     = @{'Content-Type' = $contentType; 'Authorization' = 'Bearer '+ $authToken}
    Method      = 'POST'
    URI         = $uri
    Body        = $body
    Verbose    = $true}
$status = Invoke-RestMethod @parms 
$status.value
