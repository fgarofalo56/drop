# Databricks notebook source
# DBTITLE 1,Mount For XML files
#mount data lake for xml
#Only needs to be run once on a cluster, recomend to move to its own notebooks
configs = {"fs.azure.account.auth.type": "OAuth",
       "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
       "fs.azure.account.oauth2.client.id": "<application-id>",
       "fs.azure.account.oauth2.client.secret": dbutils.secrets.get(scope="<scope-name>",key="<service-credential-key-name>"),
       "fs.azure.account.oauth2.client.endpoint": "https://login.microsoftonline.com/<directory-id>/oauth2/token",
       "fs.azure.createRemoteFileSystemDuringInitialization": "true"}

dbutils.fs.mount(
source = "abfss://xml@<storageAccount>.dfs.core.windows.net",
mount_point = "/mnt/xml",
extra_configs = configs)

# COMMAND ----------

# DBTITLE 1,Mount Data Lake
#mount data lake for PARQUET extract
#Only needs to be run once on a cluster, recomend to move to its own notebooks
configs = {"fs.azure.account.auth.type": "OAuth",
       "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
       "fs.azure.account.oauth2.client.id": "<application-id>",
       "fs.azure.account.oauth2.client.secret": dbutils.secrets.get(scope="<scope-name>",key="<service-credential-key-name>"),
       "fs.azure.account.oauth2.client.endpoint": "https://login.microsoftonline.com/<directory-id>/oauth2/token",
       "fs.azure.createRemoteFileSystemDuringInitialization": "true"}

dbutils.fs.mount(
source = "abfss://datalake@<storageAccount>.dfs.core.windows.net",
mount_point = "/mnt/datalake",
extra_configs = configs)

# COMMAND ----------

# DBTITLE 1,Set Spark SQL for Case Sensitive
#this is needed as there is ambiguous columns in intercal data
# _VALUE and _Value from Reading object
#needs to run everytime the cluster starts up

spark.sql("set spark.sql.caseSensitive=true")

# COMMAND ----------

# DBTITLE 1,Read In XML data into a Data frame
#read in raw xml files
#Create temp view for XML Parseing

df = spark.read.format('xml') \
  .option("inferSchema", "true") \
  .option("rowTag","SSNExportDocument") \
  .load('/mnt/xml/*.xml')

#create view to query
df.createOrReplaceTempView("SSNExportDocument")
#df.show()

# COMMAND ----------

# DBTITLE 1,Print Schema of the data frame
df.printSchema()

# COMMAND ----------

# DBTITLE 1,Example using Python to Query data frame
##Read and use Python
from pyspark.sql import *
from pyspark.sql.functions import explode

#Select elmenets of DF
df.select(df._CreationTime.alias('CreationTime') \
          ,df._DocumentID.alias('DocumentID') \
          ,explode(df.MeterData).alias('eMeterData') \
         ).select('CreationTime', 'DocumentID', 'eMeterData._MacID', 'eMeterData._MeterName', \
                  explode('eMeterData.RegisterData.RegisterRead').alias('eRegisterRead')).show()


# COMMAND ----------

# DBTITLE 1,Create Temp View for RegisterReads
# MAGIC %sql
# MAGIC --MeterData_RegisterData_RegisterRead_Tier_Register XML Parse to tmp View
# MAGIC CREATE
# MAGIC OR REPLACE TEMPORARY VIEW tmpDocReg As
# MAGIC Select
# MAGIC   a.Document_CreationTime,
# MAGIC   a.Document_DocumentID,
# MAGIC   a.Document_EndTime,
# MAGIC   a.Document_ExportID,
# MAGIC   a.Document_JobID,
# MAGIC   a.Document_RunID,
# MAGIC   a.Document_StartTime,
# MAGIC   a.Document_Version,
# MAGIC   a.Document_xmlns,
# MAGIC   a.MeterData_MacID,
# MAGIC   a.MeterData_MeterName,
# MAGIC   a.MeterData_UtilDeviceID,
# MAGIC   a.MeterData_UtilServicePointID,
# MAGIC   a.MeterData_XMLNS,
# MAGIC   a.RegisterData_EndTime,
# MAGIC   a.RegisterData_NumberReads,
# MAGIC   a.RegisterData_StartTime,
# MAGIC   a.eRegisterRead.`_GatewayCollectedTime` as RegisterRead_GatewayCollectedTime,
# MAGIC   a.eRegisterRead.`_ReadTime` as RegisterRead_ReadTime,
# MAGIC   a.eRegisterRead.`_RegisterReadSource` as RegisterRead_Source,
# MAGIC   a.eRegisterRead.`Tier`.`_Number` as RegisterRead_TierNumber --,a.eRegisterRead.`Tier`.`Register`
# MAGIC ,
# MAGIC   a.eRegisterRead.`Tier`.`Register`.`_Number` as RegisterRead_Number,
# MAGIC   a.eRegisterRead.`Tier`.`Register`.`_Summation` as RegisterRead_Summation,
# MAGIC   a.eRegisterRead.`Tier`.`Register`.`_SummationRawValue` as RegisterRead_SummationRawValue,
# MAGIC   a.eRegisterRead.`Tier`.`Register`.`_SummationUOM` as RegisterRead_SummationUOM,
# MAGIC   a.eRegisterRead.`Tier`.`Register`.`_VALUE` as RegisterRead_VALUE
# MAGIC From
# MAGIC   (
# MAGIC     Select
# MAGIC       regdata.Document_CreationTime,
# MAGIC       regdata.Document_DocumentID,
# MAGIC       regdata.Document_EndTime,
# MAGIC       regdata.Document_ExportID,
# MAGIC       regdata.Document_JobID,
# MAGIC       regdata.Document_RunID,
# MAGIC       regdata.Document_StartTime,
# MAGIC       regdata.Document_Version,
# MAGIC       regdata.Document_xmlns,
# MAGIC       regdata.eMeterData.`_MacID` as MeterData_MacID,
# MAGIC       regdata.eMeterData.`_MeterName` as MeterData_MeterName,
# MAGIC       regdata.eMeterData.`_UtilDeviceID` as MeterData_UtilDeviceID,
# MAGIC       regdata.eMeterData.`_UtilServicePointID` as MeterData_UtilServicePointID,
# MAGIC       regdata.eMeterData.`_xmlns` as MeterData_XMLNS,
# MAGIC       regdata.eMeterData.`RegisterData`.`_EndTime` as RegisterData_EndTime,
# MAGIC       regdata.eMeterData.`RegisterData`.`_NumberReads` as RegisterData_NumberReads,
# MAGIC       regdata.eMeterData.`RegisterData`.`_StartTime` as RegisterData_StartTime,
# MAGIC       explode(eMeterData.`RegisterData`.`RegisterRead`) as eRegisterRead --  ,explode(eMeterData.`RegisterData`) as (eRegisterRead_ReadNumber)
# MAGIC     From
# MAGIC       (
# MAGIC         Select
# MAGIC           `_CreationTime` as Document_CreationTime,
# MAGIC           `_DocumentID` as Document_DocumentID,
# MAGIC           `_EndTime` as Document_EndTime,
# MAGIC           `_ExportID` as Document_ExportID,
# MAGIC           `_JobID` as Document_JobID,
# MAGIC           `_RunID` as Document_RunID,
# MAGIC           `_StartTime` as Document_StartTime,
# MAGIC           `_Version` as Document_Version,
# MAGIC           `_xmlns` as Document_xmlns,
# MAGIC           explode(`MeterData`) as eMeterData
# MAGIC         From
# MAGIC           SSNExportDocument
# MAGIC       ) regdata
# MAGIC   ) a

# COMMAND ----------

# DBTITLE 1,Write Out Parquet File for Register Reads Data
#Create PARQUET output
from datetime import date

now = date.today()
today = now.strftime("%Y%d%m")
filename = today + '_SSNExportDocument_MeterData_RegisterData_RegisterRead_Tier_Register'
dlPath = '/mnt/datalake/meterData/' + filename

df = sqlContext.sql("SELECT * FROM tmpDocReg")

df.write.mode("append").parquet(dlPath)
print("Done")



# COMMAND ----------

# DBTITLE 1,Example query XML Data using SQL 
# MAGIC %sql
# MAGIC 
# MAGIC Select *
# MAGIC ,a.eMeterData.`_MacID`
# MAGIC ,a.eMeterData.`_MeterName`
# MAGIC ,a.eMeterData.`_UtilDeviceID`
# MAGIC ,a.eMeterData.`_UtilServicePointID`
# MAGIC ,a.eMeterData.`_xmlns`
# MAGIC ,a.eMeterData.`RegisterData`
# MAGIC ,a.eMeterData.`RegisterData`.`_EndTime`
# MAGIC ,a.eMeterData.`RegisterData`.`_NumberReads`
# MAGIC ,a.eMeterData.`RegisterData`.`_StartTime`
# MAGIC From (
# MAGIC Select 
# MAGIC       `_CreationTime` as Document_CreationTime
# MAGIC       ,`_DocumentID` as Document_DocumentID
# MAGIC       ,`_EndTime` as Document_EndTime
# MAGIC       ,`_ExportID` as Document_ExportID
# MAGIC       ,`_JobID` as Document_JobID
# MAGIC       ,`_RunID` as Document_RunID
# MAGIC       ,`_StartTime` as Document_StartTime
# MAGIC       ,`_Version` as Document_Version
# MAGIC       ,`_xmlns` as Document_xmlns
# MAGIC    -- ,explode(`MeterData`.`RegisterData`.`RegisterRead`) as eRegisterData
# MAGIC    -- ,explode(`MeterData`).`_MacId`
# MAGIC    -- ,explode(`MeterData`).`_MeterName`
# MAGIC    -- ,explode(`MeterData`).`_UtilDeviceID`
# MAGIC    -- ,explode(`MeterData`).`_UtilServicePointID`
# MAGIC    -- ,explode(`MeterData`).`_xmlns`
# MAGIC       ,explode(`MeterData`) as eMeterData
# MAGIC     From SSNExportDocument
# MAGIC     limit 1000 ) a

# COMMAND ----------

# DBTITLE 1,Create Temp View for Interval Read Data
# MAGIC %sql 
# MAGIC 
# MAGIC CREATE OR REPLACE TEMPORARY VIEW tmpIntervalData As
# MAGIC 
# MAGIC --Cast Data type to set data type for view and export out
# MAGIC 
# MAGIC Select
# MAGIC   cast(d.Document_CreationTime as DATE) as Document_CreationTime,
# MAGIC   d.Document_DocumentID,
# MAGIC   cast(d.Document_EndTime as DATE) as Document_EndTime,
# MAGIC   d.Document_ExportID,
# MAGIC   d.Document_JobID,
# MAGIC   d.Document_RunID,
# MAGIC   d.Document_StartTime,
# MAGIC   d.Document_Version,
# MAGIC   d.Document_xmlns,
# MAGIC   d.MacID,
# MAGIC   d.MeterName,
# MAGIC   d.UtilDeviceId,
# MAGIC   d.UtilServicePointID,
# MAGIC   d.MeterDate_xmlns,
# MAGIC   d.IntervalReadData_EndTime,
# MAGIC   d.IntervalReadData_IntervalLength,
# MAGIC   d.IntervalReadData_NumberIntervals,
# MAGIC   d.IntervalReadData_StartTime,
# MAGIC   d.Interval_BlockSequenceNumber,
# MAGIC   d.Interval_EndTime,
# MAGIC   d.Interval_GatewayCollectedTime,
# MAGIC   d.Interval_IntervalSequenceNumber,
# MAGIC   d.eReading.`_BlockEndValue` as Reading_BlockEndValue,
# MAGIC   d.eReading.`_Channel` as Reading_Channel,
# MAGIC   d.eReading.`_RawValue` as Reading_RawValue,
# MAGIC   d.eReading.`_UOM` as Reading_UOM,
# MAGIC   d.eReading.`_Value` as Reading_Value
# MAGIC From
# MAGIC   (
# MAGIC     Select
# MAGIC       c.Document_CreationTime,
# MAGIC       c.Document_DocumentID,
# MAGIC       c.Document_EndTime,
# MAGIC       c.Document_ExportID,
# MAGIC       c.Document_JobID,
# MAGIC       c.Document_RunID,
# MAGIC       c.Document_StartTime,
# MAGIC       c.Document_Version,
# MAGIC       c.Document_xmlns,
# MAGIC       c.MacID,
# MAGIC       c.MeterName,
# MAGIC       c.UtilDeviceId,
# MAGIC       c.UtilServicePointID,
# MAGIC       c.MeterDate_xmlns,
# MAGIC       c.IntervalReadData_EndTime,
# MAGIC       c.IntervalReadData_IntervalLength,
# MAGIC       c.IntervalReadData_NumberIntervals,
# MAGIC       c.IntervalReadData_StartTime,
# MAGIC       c.eeIntervalData.`_BlockSequenceNumber` as Interval_BlockSequenceNumber,
# MAGIC       c.eeIntervalData.`_EndTime` as Interval_EndTime,
# MAGIC       c.eeIntervalData.`_GatewayCollectedTime` as Interval_GatewayCollectedTime,
# MAGIC       c.eeIntervalData.`_IntervalSequenceNumber` as Interval_IntervalSequenceNumber,
# MAGIC       explode(c.eeIntervalData.`Reading`) as eReading
# MAGIC     From
# MAGIC       (
# MAGIC         Select
# MAGIC           b.Document_CreationTime,
# MAGIC           b.Document_DocumentID,
# MAGIC           b.Document_EndTime,
# MAGIC           b.Document_ExportID,
# MAGIC           b.Document_JobID,
# MAGIC           b.Document_RunID,
# MAGIC           b.Document_StartTime,
# MAGIC           b.Document_Version,
# MAGIC           b.Document_xmlns,
# MAGIC           b.MacID,
# MAGIC           b.MeterName,
# MAGIC           b.UtilDeviceId,
# MAGIC           b.UtilServicePointID,
# MAGIC           b.MeterDate_xmlns,
# MAGIC           b.eIntervalData.`_EndTime` as IntervalReadData_EndTime,
# MAGIC           b.eIntervalData.`_IntervalLength` as IntervalReadData_IntervalLength,
# MAGIC           b.eIntervalData.`_NumberIntervals` as IntervalReadData_NumberIntervals,
# MAGIC           b.eIntervalData.`_StartTime` as IntervalReadData_StartTime,
# MAGIC           explode(b.eIntervalData.`Interval`) as eeIntervalData
# MAGIC         From
# MAGIC           (
# MAGIC             Select
# MAGIC               a.Document_CreationTime,
# MAGIC               a.Document_DocumentID,
# MAGIC               a.Document_EndTime,
# MAGIC               a.Document_ExportID,
# MAGIC               a.Document_JobID,
# MAGIC               a.Document_RunID,
# MAGIC               a.Document_StartTime,
# MAGIC               a.Document_Version,
# MAGIC               a.Document_xmlns,
# MAGIC               a.eMeterData.`_MacID` as MacID,
# MAGIC               a.eMeterData.`_MeterName` as MeterName,
# MAGIC               a.eMeterData.`_UtilDeviceID` as UtilDeviceId,
# MAGIC               a.eMeterData.`_UtilServicePointID` as UtilServicePointID,
# MAGIC               a.eMeterData.`_xmlns` as MeterDate_xmlns,
# MAGIC               explode(a.eMeterData.`IntervalReadData`) as eIntervalData
# MAGIC             From
# MAGIC               (
# MAGIC                 Select
# MAGIC                   `_CreationTime` as Document_CreationTime,
# MAGIC                   `_DocumentID` as Document_DocumentID,
# MAGIC                   `_EndTime` as Document_EndTime,
# MAGIC                   `_ExportID` as Document_ExportID,
# MAGIC                   `_JobID` as Document_JobID,
# MAGIC                   `_RunID` as Document_RunID,
# MAGIC                   `_StartTime` as Document_StartTime,
# MAGIC                   `_Version` as Document_Version,
# MAGIC                   `_xmlns` as Document_xmlns,
# MAGIC                   explode(`MeterData`) as eMeterData
# MAGIC                 From
# MAGIC                   SSNExportDocument
# MAGIC                -- limit 10
# MAGIC               ) a
# MAGIC           ) b
# MAGIC       ) c
# MAGIC   ) d

# COMMAND ----------

# DBTITLE 1,Example check data types of each col in the Interval View used for outputting to Parquet
# MAGIC %sql
# MAGIC 
# MAGIC desc tmpIntervalData

# COMMAND ----------

# DBTITLE 1,Write Out Parquet File for Interval Read Data
#Create PARQUET output
from datetime import date

now = date.today()
today = now.strftime("%Y%d%m")
filename = today + '_SSNExportDocument_MeterData_IntervalReadData_Intervals'
dlPath = '/mnt/datalake/meterData/' + filename

df = sqlContext.sql("SELECT * FROM tmpIntervalData")

df.write.mode("append").parquet(dlPath)
print("Done")

# COMMAND ----------

# DBTITLE 1,Example query from Datalake of the parquet files
datalakeDF = spark.read.format('parquet') \
  .option("inferSchema", "true") \
  .load('/mnt/datalake/meterData/*IntervalReadData_Intervals/*.parquet')
display(datalakeDF)
#create view to query
#df.createOrReplaceTempView("SSNExportDocument")
#df.show()

datalakeDF.createOrReplaceTempView("datalakeDFtable")

# COMMAND ----------

# DBTITLE 1,Example to see what tables have been created
# MAGIC %sql
# MAGIC show tables
