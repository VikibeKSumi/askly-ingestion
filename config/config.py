import yaml
from pathlib import Path

class AsklyConfig():

    def __init__(self, file_path: Path):
        with open(file_path, "r", encoding="utf-8") as f:
            config_data = yaml.safe_load(f)

        self.BUCKET_NAME = config_data["cloud"]["bucket_name"]
        self.CLEAN_PREFIX = config_data["cloud"]["clean_prefix"]
        self.DENSE_MODEL_NAME = config_data["embedding"]["dense_model_name"]
        self.SPARSE_MODEL_NAME = config_data["embedding"]["sparse_model_name"]
        self.DIMENSION = config_data["embedding"]["dimension"]
        self.METRIC = config_data["embedding"]["metric"]
        self.NAMESPACE = config_data["vector_db"]["namespace"]
        self.INDEX_NAME = config_data["vector_db"]["index_name"]
        self.BATCH_SIZE = config_data["vector_db"]["batch_size"]
    
file_path = Path(__file__).parent / "config.yaml"
config = AsklyConfig(file_path=file_path)