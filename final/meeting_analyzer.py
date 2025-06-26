import asyncio
import logging
from typing import Dict, List
from face_recognition_module import FaceRecognizer
from audio_processing import AudioProcessor
from lip_sync_analysis import LipSyncAnalyzer
import aiohttp
import numpy as np
import cv2
import librosa

logger = logging.getLogger(__name__)

class MeetingAnalyzer:
    def __init__(self, config):
        self.config = config
        self.face_recognizer = FaceRecognizer()
        self.audio_processor = AudioProcessor()
        self.lip_sync_analyzer = LipSyncAnalyzer(config.LIPSYNC.landmark_predictor_path)
        logger.info("MeetingAnalyzer components initialized")

    async def analyze_meeting(self, participants: Dict[str, Dict[str, str]], start_time: float = 0, end_time: float = None):
        logger.info(f"Starting meeting analysis for {len(participants)} participants")
        tasks = []
        for person_name, paths in participants.items():
            tasks.append(self.process_person_data(person_name, paths, start_time, end_time))
        results = await asyncio.gather(*tasks)
        
        logger.info("Combining results from all participants")
        all_segments = [segment for result in results for segment in result]
        all_segments.sort(key=lambda x: x['start'])
        
        logger.info("Generating meeting summary")
        summary = await self.generate_summary(all_segments)
        return all_segments, summary

    async def process_person_data(self, person_name: str, paths: Dict[str, str], start_time: float, end_time: float):
        logger.info(f"Processing data for {person_name}")
        logger.info(f"Performing face recognition for {person_name}")
        await self.face_recognizer.process_individual_video(paths['video'], person_name)
        
        logger.info(f"Processing audio for {person_name}")
        audio_segments = await self.audio_processor.process_audio(paths['audio'], person_name)
        
        logger.info(f"Extracting video frames for {person_name}")
        video_frames = self.extract_video_frames(paths['video'], start_time, end_time)
        
        logger.info(f"Loading audio data for {person_name}")
        audio_data, sr = librosa.load(paths['audio'], sr=16000, offset=start_time, duration=end_time-start_time if end_time else None)
        
        logger.info(f"Performing lip sync analysis for {person_name}")
        lip_sync_result = await self.lip_sync_analyzer.analyze_lip_sync(video_frames, audio_data, sr)
        
        for segment in audio_segments:
            segment['lip_sync_score'] = lip_sync_result['correlation_score']
            segment['lip_sync_confidence'] = lip_sync_result['confidence']
        
        logger.info(f'Completed processing data for {person_name}')
        return audio_segments

    def extract_video_frames(self, video_path: str, start_time: float, end_time: float) -> List[np.ndarray]:
        logger.info(f"Extracting video frames from {video_path}")
        frames = []
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        cap.set(cv2.CAP_PROP_POS_MSEC, start_time * 1000)
        while True:
            ret, frame = cap.read()
            if not ret or (end_time and cap.get(cv2.CAP_PROP_POS_MSEC) / 1000 > end_time):
                break
            frames.append(frame)
        cap.release()
        logger.info(f"Extracted {len(frames)} frames")
        return frames

    async def generate_summary(self, segments: List[Dict]) -> str:
        logger.info("Generating meeting summary using Perplexity API")
        try:
            transcript = " ".join([f"{seg['speaker']}: {seg['text']}" for seg in segments])
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.config.PERPLEXITY.api_url,
                    headers={
                        "Authorization": f"Bearer {self.config.PERPLEXITY.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "llama-3.1-sonar-huge-128k-online",  # 유효한 모델로 변경
                        "messages": [
                            {"role": "system", "content": "You are a helpful korean assistant that summarizes meeting transcripts."},
                            {"role": "user", "content": f"Please summarize the following meeting transcript in korean:\n\n{transcript}"}
                        ]
                    }
                ) as response:
                    result = await response.json()
                    if 'choices' in result:
                        summary = result['choices'][0]['message']['content']
                        logger.info("Meeting summary generated successfully")
                        return summary
                    else:
                        error_message = result.get('error', {}).get('message', 'Unknown error occurred')
                        logger.error(f'Error in Perplexity API response: {error_message}')
                        return f'Failed to generate summary: {error_message}'
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return "Failed to generate summary"