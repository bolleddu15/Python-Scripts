from pyspark.sql import SparkSession
from pyspark.sql.functions import split, col

# Initialize SparkSession
spark = SparkSession.builder.appName("SplitColumnExample").getOrCreate()

# Sample data
data = ['1,Manoj,\t24|Hyderabad']

# Create DataFrame
df = spark.createDataFrame(data, 'string').toDF('value')

# Split the 'value' column into multiple columns
split_col = split(df['value'], ',|\t|\|')

# Add new columns to DataFrame based on the split values
df = df.withColumn('id', split_col.getItem(0)) \
       .withColumn('name', split_col.getItem(1)) \
       .withColumn('age', split_col.getItem(2)) \
       .withColumn('city', split_col.getItem(3))

# Select and display the resulting columns
df.select('id', 'name', 'age', 'city').show()

