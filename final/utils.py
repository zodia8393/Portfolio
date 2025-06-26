import tempfile
import subprocess
import os
import cv2
import numpy as np
import librosa
from typing import List, Tuple, Optional
import logging
import face_recognition_module
import asyncio
from concurrent.futures import ThreadPoolExecutor
import json
import torch


logger = logging.getLogger(__name__)

def check_cuda_availability():
    return torch.cuda.is_available()

async def load_audio(audio_path: str) -> Tuple[np.ndarray, int]:
    """Loads audio from a file."""
    try:
        loop = asyncio.get_running_loop()
        with ThreadPoolExecutor() as pool:
            audio, sr = await loop.run_in_executor(pool, librosa.load, audio_path)
        return audio, sr
    except Exception as e:
        logger.error(f"Error loading audio: {e}")
        return np.array([]), 0

async def process_participant_video(analyzer, video_path: str, audio_path: str, participant_name: str) -> None:
    """Processes a participant's video to extract face embeddings and lip sync scores."""
    cap = cv2.VideoCapture(video_path)
    audio_data, sr = await load_audio(audio_path)
    if len(audio_data) == 0:
        logger.error(f"Failed to load audio for participant {participant_name}")
        return

    face_embedding = None
    lip_sync_results = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if face_embedding is None:
            face_embedding = await analyzer.face_recognizer.recognize_face(frame)
            await analyzer.face_recognizer.add_face(participant_name, frame, face_embedding)

        lip_sync_result = await analyzer.lip_sync_analyzer.analyze_lip_sync([frame], audio_data)
        if lip_sync_result:
            lip_sync_results.append(lip_sync_result)

    cap.release()

    avg_lip_sync_score = np.mean([result['correlation_score'] for result in lip_sync_results])
    await analyzer.db_manager.add_participant(participant_name, json.dumps(face_embedding.tolist()), avg_lip_sync_score)

async def process_side_videos(analyzer, video_path: str) -> None:
    """Processes side videos with two participants each for additional context and recognition accuracy."""
    cap = cv2.VideoCapture(video_path)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition_module.face_locations(rgb_frame)
        face_encodings = face_recognition_module.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            recognized_name = await analyzer.face_recognizer.recognize_face(frame[top:bottom, left:right])
            logger.info(f"Recognized {recognized_name} in side video.")
            analyzer.speaker_tracker.track_speaker((top, right, bottom, left), recognized_name)

    cap.release()

async def process_combined_video(analyzer, video_path: str, audio_path: str, speaker_labels: np.ndarray) -> List[Tuple[List[str], float, str, np.ndarray, int, str]]:
    cap = cv2.VideoCapture(video_path)
    audio_data, sr = await load_audio(audio_path)
    frame_results = []
    frame_index = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if len(speaker_labels) > 0:
            speaker_label = speaker_labels[min(frame_index, len(speaker_labels) - 1)]
            name = f"Speaker {speaker_label}"
        else:
            name = "Unknown"

        recognized_names = []
        faces = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml').detectMultiScale(frame)
        
        for (x, y, w, h) in faces:
            face_image = frame[y:y+h, x:x+w]
            recognized_name = await analyzer.face_recognizer.recognize_face(face_image)
            recognized_names.append(recognized_name)

        start_time = frame_index / sr
        end_time = start_time + 1 / sr
        audio_segment = audio_data[int(start_time*sr):int(end_time*sr)]
        
        pitch = await analyzer.audio_processor.extract_pitch(audio_segment)
        transcription = await analyzer.audio_processor.transcribe_audio(audio_segment)

        frame_results.append((recognized_names, pitch, transcription, frame, frame_index, name))
        
        frame_index += 1

    cap.release()
    return frame_results