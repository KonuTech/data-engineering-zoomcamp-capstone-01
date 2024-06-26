from typing import Any
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, from_json, from_unixtime, to_timestamp
from pyspark.sql.types import (ArrayType, DoubleType, IntegerType, LongType,
                               StringType, StructField, StructType)

from src.constants import POSTGRES_PROPERTIES, POSTGRES_URL


def create_spark_session() -> SparkSession:
    """
    Creates a SparkSession for interacting with Spark.
    """
    spark: SparkSession = (
        SparkSession.builder.appName(
            "PostgreSQL Connection with PySpark for Earthquakes Data"
        )
        .config(
            "spark.jars.packages",
            "org.postgresql:postgresql:42.5.4,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0",
        )
        .getOrCreate()
    )
    return spark


def create_initial_dataframe(spark_session: SparkSession) -> DataFrame:
    """
    Reads the streaming data and creates the initial dataframe accordingly.
    """
    df: DataFrame = (
        spark_session.readStream.format("kafka")
        .option("kafka.bootstrap.servers", "kafka:9092")
        .option("subscribe", "earthquakes")
        .option("startingOffsets", "earliest")
        .load()
    )

    return df


def create_final_dataframe(df: DataFrame) -> DataFrame:
    """
    Modifies the initial dataframe, and creates the final dataframe.
    """
    schema: StructType = StructType(
        [
            StructField("generated", LongType(), True),
            StructField("metadata_url", StringType(), True),
            StructField("metadata_title", StringType(), True),
            StructField("metadata_status", IntegerType(), True),
            StructField("api", StringType(), True),
            StructField("count", IntegerType(), True),
            StructField("mag", DoubleType(), True),
            StructField("place", StringType(), True),
            StructField("time", LongType(), True),
            StructField("updated", LongType(), True),
            StructField("tz", StringType(), True),
            StructField("url", StringType(), True),
            StructField("detail", StringType(), True),
            StructField("felt", IntegerType(), True),
            StructField("cdi", DoubleType(), True),
            StructField("mmi", DoubleType(), True),
            StructField("alert", StringType(), True),
            StructField("status", StringType(), True),
            StructField("tsunami", IntegerType(), True),
            StructField("sig", IntegerType(), True),
            StructField("net", StringType(), True),
            StructField("code", StringType(), True),
            StructField("ids", StringType(), True),
            StructField("sources", StringType(), True),
            StructField("types", StringType(), True),
            StructField("nst", IntegerType(), True),
            StructField("dmin", DoubleType(), True),
            StructField("rms", DoubleType(), True),
            StructField("gap", IntegerType(), True),
            StructField("magtype", StringType(), True),
            StructField("type", StringType(), True),
            StructField("title", StringType(), True),
            StructField("geometry_coordinates", ArrayType(DoubleType(), True), True),
            StructField("longitude", DoubleType(), True),
            StructField("latitude", DoubleType(), True),
            StructField("radius", DoubleType(), True),
            StructField("id", StringType(), True),
        ]
    )

    df_out: DataFrame = (
        df.selectExpr("CAST(value AS STRING)")
        .select(from_json(col("value"), schema).alias("data"))
        .select(
            to_timestamp(from_unixtime(col("data.generated") / 1000)).alias(
                "generated"
            ),
            col("data.metadata_url"),
            col("data.metadata_title"),
            col("data.metadata_status"),
            col("data.api"),
            col("data.count"),
            col("data.mag"),
            col("data.place"),
            to_timestamp(from_unixtime(col("data.time") / 1000)).alias("time"),
            to_timestamp(from_unixtime(col("data.updated") / 1000)).alias("updated"),
            col("data.tz"),
            col("data.url"),
            col("data.detail"),
            col("data.felt"),
            col("data.cdi"),
            col("data.mmi"),
            col("data.alert"),
            col("data.status"),
            col("data.tsunami"),
            col("data.sig"),
            col("data.net"),
            col("data.code"),
            col("data.ids"),
            col("data.sources"),
            col("data.types"),
            col("data.nst"),
            col("data.dmin"),
            col("data.rms"),
            col("data.gap"),
            col("data.magType"),
            col("data.type"),
            col("data.title"),
            col("data.geometry_coordinates"),
            col("data.longitude"),
            col("data.latitude"),
            col("data.radius"),
            col("data.id"),
        )
    )

    return df_out


def start_streaming(df_parsed: DataFrame, spark: SparkSession) -> Any:
    """
    Starts the streaming to table spark_streaming.rappel_conso in PostgreSQL.
    """

    # Load existing ids
    df_existing_ids: DataFrame = spark.read.jdbc(
        POSTGRES_URL, "earthquakes", properties=POSTGRES_PROPERTIES
    ).select("id")

    query: Any = (
        df_parsed.writeStream.foreachBatch(
            lambda batch_df, _: (
                # Subtract existing ids from the batch
                batch_df.alias("new")
                .join(
                    df_existing_ids.alias("old"),
                    batch_df["id"] == df_existing_ids["id"],
                    "leftanti",
                )
                .limit(5)
                .show(),  # Print the first 5 rows of the new batch
                batch_df.alias("new")
                .join(
                    df_existing_ids.alias("old"),
                    batch_df["id"] == df_existing_ids["id"],
                    "leftanti",
                )
                .write.jdbc(
                    POSTGRES_URL,
                    "earthquakes",
                    "append",
                    properties=POSTGRES_PROPERTIES,
                ),
            )
        )
        .trigger(once=True)
        .start()
    )

    return query.awaitTermination()


def write_to_postgres() -> None:
    """
    Main function to write streaming data to PostgreSQL.
    """
    spark: SparkSession = create_spark_session()
    df: DataFrame = create_initial_dataframe(spark)
    df_parsed: DataFrame = create_final_dataframe(df)
    start_streaming(df_parsed, spark=spark)


if __name__ == "__main__":
    write_to_postgres()
