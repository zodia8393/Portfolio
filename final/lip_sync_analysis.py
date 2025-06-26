import numpy as np
import torch
import cv2
import dlib
from typing import List, Dict, Optional
import logging
import librosa

logger = logging.getLogger(__name__)

class LipSyncAnalyzer:
    def __init__(self, landmark_predictor_path: str):
        logger.info("Initializing LipSyncAnalyzer")
        self.face_detector = dlib.get_frontal_face_detector()
        self.landmark_predictor = dlib.shape_predictor(landmark_predictor_path)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {self.device}")

    def extract_lip_landmarks(self, frame: np.ndarray) -> Optional[np.ndarray]:
        try:
            if frame.ndim == 2:
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            elif frame.shape[2] == 4:
                frame = frame[:, :, :3]
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_detector(gray)
            if len(faces) == 0:
                return None
            
            landmarks = self.landmark_predictor(gray, faces[0])
            lip_landmarks = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(48, 68)], dtype=np.float32)
            return lip_landmarks.flatten()
        except Exception as e:
            logger.error(f"Error extracting lip landmarks: {e}")
            return None

    def compute_lip_movement(self, landmarks: np.ndarray) -> float:
        landmarks = landmarks.reshape(-1, 2)
        centroid = np.mean(landmarks, axis=0)
        distances = np.linalg.norm(landmarks - centroid, axis=1)
        return np.mean(distances)

    def extract_audio_features(self, audio: np.ndarray, sr: int) -> np.ndarray:
        logger.info("Extracting audio features")
        mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
        delta = librosa.feature.delta(mfcc)
        delta2 = librosa.feature.delta(mfcc, order=2)
        return np.concatenate([mfcc, delta, delta2])

    def compute_dtw(self, lip_movements: np.ndarray, audio_features: np.ndarray) -> float:
        logger.info("Computing DTW")
        n, m = len(lip_movements), len(audio_features)
        dtw_matrix = np.zeros((n+1, m+1))
        dtw_matrix[0, 1:] = np.inf
        dtw_matrix[1:, 0] = np.inf
        
        for i in range(1, n+1):
            for j in range(1, m+1):
                cost = abs(lip_movements[i-1] - audio_features[j-1])
                dtw_matrix[i, j] = cost + min(dtw_matrix[i-1, j], dtw_matrix[i, j-1], dtw_matrix[i-1, j-1])
        
        return dtw_matrix[n, m]

    async def analyze_lip_sync(self, video_frames: List[np.ndarray], audio_data: np.ndarray, sr: int) -> Dict[str, float]:
        try:
            logger.info("Starting lip sync analysis")
            lip_movements = []
            for i, frame in enumerate(video_frames):
                landmarks = self.extract_lip_landmarks(frame)
                if landmarks is not None:
                    movement = self.compute_lip_movement(landmarks)
                    lip_movements.append(movement)
                if i % 100 == 0:
                    logger.info(f"Processed {i} frames for lip movements")

            if not lip_movements:
                logger.warning("No lip movements detected in the provided frames.")
                return {"correlation_score": 0.0, "dtw_score": float('inf'), "confidence": 0.0}

            lip_movements = np.array(lip_movements)
            audio_features = self.extract_audio_features(audio_data, sr)

            logger.info("Aligning lip movements and audio features")
            min_len = min(len(lip_movements), audio_features.shape[1])
            lip_movements = lip_movements[:min_len]
            audio_features = audio_features[:, :min_len]

            logger.info("Computing correlation")
            if torch.cuda.is_available():
                lip_movements_tensor = torch.from_numpy(lip_movements).float().to(self.device)
                audio_features_tensor = torch.from_numpy(audio_features).float().to(self.device)
                correlation = torch.nn.functional.cosine_similarity(
                    lip_movements_tensor.unsqueeze(0),
                    audio_features_tensor.mean(dim=0).unsqueeze(0)
                ).item()
            else:
                correlation = np.corrcoef(lip_movements, audio_features.mean(axis=0))[0, 1]

            dtw_score = self.compute_dtw(lip_movements, audio_features.mean(axis=0))

            logger.info("Computing confidence")
            confidence = np.mean(lip_movements) / np.max(lip_movements)

            result = {
                "correlation_score": float(correlation),
                "dtw_score": float(dtw_score),
                "confidence": float(confidence)
            }

            logger.info("Lip sync analysis completed successfully.")
            return result

        except Exception as e:
            logger.error(f"Error analyzing lip sync: {e}")
            logger.error(f"Error details: {type(e).__name__}, {str(e)}")
            return {"correlation_score": 0.0, "dtw_score": float('inf'), "confidence": 0.0}