import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, when, desc, to_date, row_number
from pyspark.sql.window import Window

def main():
    # Initialize Spark Session
    # Note: Ensure the PostgreSQL JDBC driver jar is available in the classpath or passed via --jars
    spark = SparkSession.builder \
        .appName("KabarakLostAndFoundAnalytics") \
        .getOrCreate()

    # Database connection properties
    # Update these with your actual database credentials
    jdbc_url = "jdbc:postgresql://localhost:5432/kabarak_lost_found"
    connection_properties = {
        "user": "postgres",
        "password": "password",
        "driver": "org.postgresql.Driver"
    }

    try:
        # 1. Read data from items table
        print("Reading data from PostgreSQL...")
        items_df = spark.read.jdbc(url=jdbc_url, table="items", properties=connection_properties)

        if items_df.count() == 0:
            print("No data found in items table.")
            return

        # 2. Perform Aggregations
        
        # Convert timestamp to date for daily stats
        items_with_date = items_df.withColumn("report_date", to_date(col("date_reported")))

        # A. Calculate totals per day (Found and Returned)
        daily_counts = items_with_date.groupBy("report_date").agg(
            count("*").alias("total_found"),
            count(when(col("status") == "Returned", 1)).alias("total_returned")
        )

        # Calculate Return Rate (for display/logging purposes as it's not in the target schema)
        daily_counts_with_rate = daily_counts.withColumn(
            "return_rate", 
            (col("total_returned") / col("total_found")) * 100
        )
        
        print("Daily Statistics calculated:")
        daily_counts_with_rate.show()

        # B. Find Top Location per day
        # Count items per location per day
        location_counts = items_with_date.groupBy("report_date", "location_found").count()
        
        # Window to rank locations by count desc per day
        window_spec = Window.partitionBy("report_date").orderBy(desc("count"))
        
        top_locations = location_counts.withColumn("rank", row_number().over(window_spec)) \
            .filter(col("rank") == 1) \
            .select(col("report_date"), col("location_found").alias("top_location"))

        # 3. Join stats with top location
        final_stats = daily_counts.join(top_locations, "report_date", "left") \
            .select("report_date", "total_found", "total_returned", "top_location")

        # 4. Write results to daily_stats table
        # Note: We use mode="append". Ensure daily_stats handles duplicates or is cleared before run if needed.
        # Since report_date is UNIQUE, simple append might fail if data exists. 
        # For this script, we assume we are populating fresh or handling errors.
        
        print("Writing results to daily_stats table...")
        final_stats.write.jdbc(
            url=jdbc_url, 
            table="daily_stats", 
            mode="append", 
            properties=connection_properties
        )
        print("Data written successfully.")

    except Exception as e:
        print(f"Error processing data: {e}")
        sys.exit(1)
    finally:
        spark.stop()

if __name__ == "__main__":
    main()
