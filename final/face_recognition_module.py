import numpy as np
import torch
from deepface import DeepFace
from typing import List, Dict, Union, Optional
import logging
import cv2
from deepface.modules import verification

logger = logging.getLogger(__name__)

class FaceRecognizer:
    def __init__(self, model_name: str = "Facenet512", distance_metric: str = "cosine", threshold: float = 0.6):
        logger.info(f"Initializing FaceRecognizer with model: {model_name}")
        self.model = DeepFace.build_model(model_name)
        self.distance_metric = distance_metric
        self.threshold = threshold
        self.face_embeddings: Dict[str, List[np.ndarray]] = {}
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {self.device}")
        if isinstance(self.model, torch.nn.Module):
            self.model.to(self.device)

    async def process_individual_video(self, video_path: str, person_name: str):
        logger.info(f"Processing video for {person_name}: {video_path}")
        cap = cv2.VideoCapture(video_path)
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = self.face_locations(frame)
            for face in face_locations:
                embedding = self.get_embedding(face)
                if embedding is not None:
                    self.add_face(person_name, embedding)
            frame_count += 1
            if frame_count % 100 == 0:
                logger.info(f"Processed {frame_count} frames for {person_name}")
        cap.release()
        logger.info(f"Completed processing video for {person_name}, total frames: {frame_count}")

    def add_face(self, name: str, embedding: np.ndarray):
        if name not in self.face_embeddings:
            self.face_embeddings[name] = []
        self.face_embeddings[name].append(embedding)

    def get_embedding(self, face_image: np.ndarray) -> Optional[np.ndarray]:
        try:
            if isinstance(self.model, torch.nn.Module):
                face_tensor = torch.from_numpy(face_image).float().unsqueeze(0).to(self.device)
                with torch.no_grad():
                    embedding = self.model(face_tensor).cpu().numpy()
            else:
                embedding = DeepFace.represent(face_image, model_name="Facenet512", enforce_detection=False)
            return embedding[0] if isinstance(embedding, list) else embedding
        except Exception as e:
            logger.error(f"Error getting face embedding: {e}")
            return None

    def face_locations(self, image: np.ndarray) -> List[np.ndarray]:
        faces = DeepFace.extract_faces(image, enforce_detection=False, align=False)
        return [face['face'] for face in faces]

    def calculate_distance(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        if self.distance_metric == "cosine":
            return verification.find_cosine_distance(embedding1, embedding2)
        return verification.find_euclidean_distance(embedding1, embedding2)

    async def recognize_face(self, face_image: np.ndarray) -> str:
        logger.info("Recognizing face")
        embedding = self.get_embedding(face_image)
        if embedding is None:
            logger.warning("Failed to get embedding for face")
            return "Unknown"
        
        min_distance = float('inf')
        recognized_name = "Unknown"
        for name, stored_embeddings in self.face_embeddings.items():
            for stored_embedding in stored_embeddings:
                distance = self.calculate_distance(embedding, stored_embedding)
                if distance < min_distance:
                    min_distance = distance
                    recognized_name = name
        
        result = recognized_name if min_distance < self.threshold else "Unknown"
        logger.info(f"Face recognized as: {result}")
        return result