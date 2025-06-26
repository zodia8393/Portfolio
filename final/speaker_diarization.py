import numpy as np
import librosa
from spectralcluster import SpectralClusterer
import cv2
from typing import Tuple, List
import logging
from face_recognition_module import FaceRecognizer

logger = logging.getLogger(__name__)

class SpeakerDiarization:
    def __init__(self, min_clusters=2, max_clusters=10):
        self.spectral_clusterer = SpectralClusterer(
            min_clusters=min_clusters,
            max_clusters=max_clusters
        )
        self.face_recognizer = FaceRecognizer()

    async def get_speaker_embeddings(self, audio_path: str) -> np.ndarray:
        try:
            y, sr = librosa.load(audio_path, sr=16000)
            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
            return mfcc.T
        except Exception as e:
            logger.error(f"Error in get_speaker_embeddings: {e}")
            return np.array([])

    async def cluster_speakers(self, embeddings: np.ndarray) -> np.ndarray:
        try:
            return self.spectral_clusterer.predict(embeddings)
        except Exception as e:
            logger.error(f"Error in cluster_speakers: {e}")
            return np.array([])

    async def diarize(self, video_path: str, audio_path: str) -> Tuple[np.ndarray, List[Tuple[int, np.ndarray]]]:
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                raise ValueError(f"Unable to open video file: {video_path}")
            
            frame_rate = cap.get(cv2.CAP_PROP_FPS)
            
            audio_embeddings = await self.get_speaker_embeddings(audio_path)
            if audio_embeddings.size == 0:
                raise ValueError("Failed to extract audio embeddings")
            
            speaker_labels = await self.cluster_speakers(audio_embeddings)
            if speaker_labels.size == 0:
                raise ValueError("Failed to cluster speakers")
            
            face_locations = []
            face_encodings = []
            speaker_faces = []
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_locs = await self.face_recognizer.face_locations(rgb_frame)
                face_encs = await self.face_recognizer.face_encodings(rgb_frame, face_locs)
                
                face_locations.append(face_locs)
                face_encodings.append(face_encs)
            
            cap.release()
            
            for i, label in enumerate(speaker_labels):
                frame_index = int(i * frame_rate / len(speaker_labels))
                if frame_index < len(face_locations) and len(face_locations[frame_index]) > 0:
                    speaker_faces.extend([(label, face_enc) for face_enc in face_encodings[frame_index]])
            
            return speaker_labels, speaker_faces
        except Exception as e:
            logger.error(f"Error in speaker diarization: {e}")
            logger.error(f"Error details: {type(e).__name__}, {str(e)}")
            return np.array([]), []

    def __str__(self):
        return f"SpeakerDiarization(min_clusters={self.spectral_clusterer.min_clusters}, max_clusters={self.spectral_clusterer.max_clusters})"

    def __repr__(self):
        return self.__str__()