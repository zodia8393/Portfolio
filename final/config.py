from decouple import config, Csv
from dataclasses import dataclass
from typing import Dict, Tuple, List
import os
import logging

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class PerplexityConfig:
    api_key: str
    api_url: str

@dataclass
class TestConfig:
    enabled: bool
    start_time: float
    end_time: float
    target_person: str
    individual_video_path: str
    individual_audio_path: str
    side_video_path: str
    full_video_path: str
    full_audio_path: str

@dataclass(frozen=True)
class FaceRecognitionConfig:
    model: str
    distance_metric: str

@dataclass(frozen=True)
class AudioConfig:
    whisper_model: str

@dataclass(frozen=True)
class LipSyncConfig:
    landmark_predictor_path: str

@dataclass(frozen=True)
class OutputConfig:
    path: str

@dataclass(frozen=True)
class DiarizationConfig:
    min_clusters: int
    max_clusters: int

@dataclass(frozen=True)
class ProcessingConfig:
    num_workers: int

@dataclass(frozen=True)
class DatabaseConfig:
    host: str
    user: str
    password: str
    name: str
    pool_size: int
    port: int 

@dataclass(frozen=True)
class VideoConfig:
    path: str
    audio_path: str
    fps: float

@dataclass(frozen=True)
class APIConfig:
    key: str

@dataclass(frozen=True)
class Config:
    FACE_RECOGNITION: FaceRecognitionConfig
    AUDIO: AudioConfig
    LIPSYNC: LipSyncConfig
    DIARIZATION: DiarizationConfig
    PROCESSING: ProcessingConfig
    DATABASE: DatabaseConfig
    VIDEO: VideoConfig
    OUTPUT: OutputConfig
    PARTICIPANTS: Dict[str, Tuple[str, str]]
    SIDE_VIDEOS: Dict[str, str]
    API: APIConfig
    TEST: TestConfig
    PERPLEXITY: PerplexityConfig

def parse_csv_to_dict(raw_data: List[str], tuple_size: int) -> Dict[str, Tuple[str, ...]]:
    result = {}
    for i in range(0, len(raw_data), tuple_size):
        if i + tuple_size <= len(raw_data):
            key = raw_data[i]
            values = tuple(raw_data[i+1:i+tuple_size])
            result[key] = values
    return result

def validate_paths(*paths):
    for path in paths:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Path does not exist: {path}")

def load_config() -> Config:
    try:
        participants_raw = config('PARTICIPANTS', cast=Csv())
        side_videos_raw = config('SIDE_VIDEOS', cast=Csv())

        participants = parse_csv_to_dict(participants_raw, 3)
        side_videos = parse_csv_to_dict(side_videos_raw, 2)

        landmark_predictor_path = config('LANDMARK_PREDICTOR_PATH')
        video_path = config('VIDEO_PATH')
        video_audio_path = config('VIDEO_AUDIO_PATH')
        output_path = config('OUTPUT_PATH')

        validate_paths(landmark_predictor_path, video_path, video_audio_path)

        return Config(
            FACE_RECOGNITION=FaceRecognitionConfig(
                model=config('FACE_RECOGNITION_MODEL'),
                distance_metric=config('FACE_RECOGNITION_DISTANCE_METRIC')
            ),
            AUDIO=AudioConfig(
                whisper_model=config('WHISPER_MODEL')
            ),
            LIPSYNC=LipSyncConfig(
                landmark_predictor_path=landmark_predictor_path
            ),
            DIARIZATION=DiarizationConfig(
                min_clusters=config('MIN_CLUSTERS', cast=int),
                max_clusters=config('MAX_CLUSTERS', cast=int),
            ),
            PROCESSING=ProcessingConfig(
                num_workers=config('NUM_WORKERS', cast=int)
            ),
            DATABASE=DatabaseConfig(
                host=config('DB_HOST'),
                user=config('DB_USER'),
                password=config('DB_PASSWORD'),
                name=config('DB_NAME'),
                pool_size=config('DB_POOL_SIZE', cast=int),
                port=config('DB_PORT', cast=int)  
            ),
            VIDEO=VideoConfig(
                path=video_path,
                audio_path=video_audio_path,
                fps=config('VIDEO_FPS', cast=float)
            ),
            OUTPUT=OutputConfig(
                path=output_path
            ),
            PARTICIPANTS=participants,
            SIDE_VIDEOS=side_videos,
            API=APIConfig(
                key=config('API_KEY')
            ),
            TEST=TestConfig(
                enabled=config('TEST_MODE_ENABLED', cast=bool, default=False),
                start_time=config('TEST_START_TIME', cast=float, default=0.0),
                end_time=config('TEST_END_TIME', cast=float, default=60.0),
                target_person=config('TEST_TARGET_PERSON', default=''),
                individual_video_path=config('TEST_INDIVIDUAL_VIDEO_PATH', default=''),
                individual_audio_path=config('TEST_INDIVIDUAL_AUDIO_PATH', default=''),
                side_video_path=config('TEST_SIDE_VIDEO_PATH', default=''),
                full_video_path=config('TEST_FULL_VIDEO_PATH', default=''),
                full_audio_path=config('TEST_FULL_AUDIO_PATH', default='')
            ),
            PERPLEXITY=PerplexityConfig(
                api_key=config('PERPLEXITY_API_KEY'),
                api_url=config('PERPLEXITY_API_URL', default="https://api.perplexity.ai/chat/completions")
            ),
        )
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        config = load_config()
        logger.info("Configuration loaded successfully")
        logger.info(f"Number of participants: {len(config.PARTICIPANTS)}")
        logger.info(f"Number of side videos: {len(config.SIDE_VIDEOS)}")
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")