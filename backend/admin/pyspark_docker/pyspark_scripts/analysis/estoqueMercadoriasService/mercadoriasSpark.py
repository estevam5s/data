from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType
from abc import ABC, abstractmethod


class SparkConfig(ABC):
    @abstractmethod
    def configure_spark(self, app_name):
        pass


class DefaultSparkConfig(SparkConfig):
    def configure_spark(self, app_name):
        spark = SparkSession.builder.appName(app_name).getOrCreate()
        spark.sparkContext.setLogLevel("OFF")
        return spark


class DataFrameReader(ABC):
    @abstractmethod
    def read_csv(self, spark_session, file_path, header, schema):
        pass


class CsvReader(DataFrameReader):
    def read_csv(self, spark_session, file_path, header, schema):
        return spark_session.read.csv(file_path, header=header, schema=schema)


class SparkCsvReader:
    def __init__(self, spark_config: SparkConfig, data_frame_reader: DataFrameReader):
        self.spark_config = spark_config
        self.data_frame_reader = data_frame_reader

    def read(self, app_name, file_path, header=True, schema=None):
        spark_session = self.spark_config.configure_spark(app_name)
        return self.data_frame_reader.read_csv(spark_session, file_path, header, schema)


class EstoqueMercadoriasCsvReader:
    SCHEMA = StructType([
        StructField("ID", IntegerType(), True),
        StructField("NOME", StringType(), True),
        StructField("QUANTIDADE", IntegerType(), True)
    ])

    @staticmethod
    def read_csv(file_path):
        spark_csv_reader = SparkCsvReader(DefaultSparkConfig(), CsvReader())
        df = spark_csv_reader.read("Estoque de Mercadorias CSV Reader", file_path, schema=EstoqueMercadoriasCsvReader.SCHEMA)
        return df


if __name__ == "__main__":
    df = EstoqueMercadoriasCsvReader.read_csv("../../../src/data/estoque_mercadorias.csv")
    df.show()