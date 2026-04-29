# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "61f828ab-fc19-4852-821a-f341feab3a9e",
# META       "default_lakehouse_name": "lh_medical_prescriptions",
# META       "default_lakehouse_workspace_id": "76d469df-375e-4be1-931e-72eb81797419",
# META       "known_lakehouses": [
# META         {
# META           "id": "61f828ab-fc19-4852-821a-f341feab3a9e"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

from pyspark.sql import functions as F

# 1. Caminho para os arquivos JSON
path = "Files/medical-prescriptions/*.json"

# 2. Ler os arquivos JSON
df_raw = spark.read.option("multiline", "true").json(path)

# 3. Transformação: Explodir o array 'medications' e selecionar os campos
# Usamos F.col("patient.full_name") para acessar subcampos do JSON
df_final = df_raw.select(
    F.col("prescription_id"),
    F.col("issue_date"),
    F.col("patient.full_name").alias("patient_name"),
    F.col("patient.patient_id").alias("patient_id"),
    F.explode(F.col("medications")).alias("medication")
).select(
    "*",
    F.col("medication.name").alias("medication_name"),
    F.col("medication.dosage").alias("medication_dosage"),
    F.col("medication.frequency").alias("medication_frequency")
).drop("medication") # Removemos a coluna temporária do objeto original

# 4. Salvar como uma Tabela Delta no Lakehouse (Tabelas)
df_final.write.format("delta").mode("overwrite").saveAsTable("medical_prescriptions")

# Mostrar o resultado
display(df_final)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
