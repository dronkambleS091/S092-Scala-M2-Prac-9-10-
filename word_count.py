import os
import sys

# Tell Spark to use the current Python interpreter
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

from pyspark.sql import SparkSession

# Create Spark session
spark = SparkSession.builder \
    .appName("WordCount") \
    .master("local[*]") \
    .getOrCreate()

# Set log level to reduce unnecessary messages
spark.sparkContext.setLogLevel("ERROR")

# Read the input text file
text_file = spark.sparkContext.textFile("input.txt")

# Count frequency of each word
word_counts = (
    text_file
    .flatMap(lambda line: line.split())
    .map(lambda word: (word, 1))
    .reduceByKey(lambda a, b: a + b)
)

# Display word counts
print("\n--- Word Count ---")

for word, count in sorted(word_counts.collect()):
    print(word, ":", count)

# Stop Spark
spark.stop()