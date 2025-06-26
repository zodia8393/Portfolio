import numpy as np
import librosa
import whisper
from typing import List, Dict
import logging
import torch

logger = logging.getLogger(__name__)

class AudioProcessor:
    def __init__(self, whisper_model: str = 'large'):
        logger.info(f"Initializing AudioProcessor with Whisper model: {whisper_model}")
        self.whisper_model = whisper.load_model(whisper_model)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {self.device}")
        self.whisper_model.to(self.device)

    async def process_audio(self, audio_path: str, speaker_name: str) -> List[Dict]:
        logger.info(f"Processing audio for {speaker_name}: {audio_path}")
        try:
            audio, sr = librosa.load(audio_path, sr=16000)
            logger.info(f"Audio loaded, duration: {len(audio)/sr:.2f} seconds")
            
            audio_tensor = torch.from_numpy(audio).float().to(self.device)
            logger.info("Extracting MFCC features")
            mfcc = self.extract_mfcc(audio_tensor, sr)
            
            logger.info("Transcribing audio")
            transcription = self.transcribe_audio(audio_tensor)
            
            logger.info("Extracting segments")
            segments = self.extract_segments(transcription, speaker_name, mfcc)
            
            logger.info(f'Processed audio for {speaker_name}: {len(segments)} segments')
            return segments
        except Exception as e:
            logger.error(f'Error processing audio: {e}')
            return []

    def extract_mfcc(self, audio: torch.Tensor, sr: int) -> np.ndarray:
        mfcc = librosa.feature.mfcc(y=audio.cpu().numpy(), sr=sr, n_mfcc=13)
        return np.array(mfcc)

    def transcribe_audio(self, audio: torch.Tensor) -> Dict:
        return self.whisper_model.transcribe(audio.cpu().numpy())

    def extract_segments(self, transcription: Dict, speaker_name: str, mfcc: np.ndarray) -> List[Dict]:
        segments = []
        for segment in transcription['segments']:
            start_frame = int(segment['start'] * 100)
            end_frame = int(segment['end'] * 100)
            segments.append({
                'start': segment['start'],
                'end': segment['end'],
                'speaker': speaker_name,
                'text': segment['text'],
                'mfcc': mfcc[:, start_frame:end_frame].tolist()
            })
        return segments