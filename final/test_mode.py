import logging
import cv2
import numpy as np
from typing import List, Tuple
import librosa
from meeting_analyzer import MeetingAnalyzer

logger = logging.getLogger(__name__)

async def process_video(analyzer: MeetingAnalyzer, video_path: str, audio_path: str, start_time: float, end_time: float, video_type: str) -> List[Tuple[float, float, str]]:
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    audio_data, sr = librosa.load(audio_path, sr=16000)
    
    speaker_segments = []
    current_time = start_time

    while current_time < end_time:
        cap.set(cv2.CAP_PROP_POS_MSEC, current_time * 1000)
        ret, frame = cap.read()
        if not ret:
            break

        face_locations = await analyzer.face_recognizer.face_locations(frame)
        if face_locations:
            face_encodings = await analyzer.face_recognizer.face_encodings(frame, face_locations)
            if face_encodings:
                recognized_name = await analyzer.face_recognizer.recognize_face(face_locations[0], video_type)
                
                lip_sync_result = await analyzer.lip_sync_analyzer.analyze_lip_sync([frame], audio_data, current_time)
                if lip_sync_result:
                    logger.info(f"Lip sync analysis result: {lip_sync_result}")
                    speaker_segments.append((current_time, current_time + 1/fps, recognized_name))
        
        current_time += 1/fps

    cap.release()
    return speaker_segments

async def run_test_mode(config, analyzer):
    # Set target person
    analyzer.face_recognizer.set_target_person(config.TEST.target_person)

    # Process individual video to collect target person's embeddings
    await analyzer.face_recognizer.process_individual_video(
        config.TEST.individual_video_path,
        config.TEST.individual_audio_path,
        config.TEST.start_time,
        config.TEST.end_time
    )

    # Process individual video
    individual_results = await process_video(analyzer, config.TEST.individual_video_path, config.TEST.individual_audio_path, config.TEST.start_time, config.TEST.end_time, "individual")

    # Process side video
    side_results = await process_video(analyzer, config.TEST.side_video_path, config.TEST.full_audio_path, config.TEST.start_time, config.TEST.end_time, "side")

    # Process main video
    main_results = await process_video(analyzer, config.TEST.full_video_path, config.TEST.full_audio_path, config.TEST.start_time, config.TEST.end_time, "full")

    # Analyze results
    target_person = config.TEST.target_person
    individual_speaking_times = [r[0] for r in individual_results if r[2] == target_person]
    side_detections = [r for r in side_results if r[2] == target_person]
    main_detections = [r for r in main_results if r[2] == target_person]

    # Calculate accuracy
    side_accuracy = len([r for r in side_detections if r[0] in individual_speaking_times]) / len(individual_speaking_times) if individual_speaking_times else 0
    main_accuracy = len([r for r in main_detections if r[0] in individual_speaking_times]) / len(individual_speaking_times) if individual_speaking_times else 0

    logger.info(f"Test results for {target_person}:")
    logger.info(f"Side video detection accuracy: {side_accuracy:.2f}")
    logger.info(f"Main video detection accuracy: {main_accuracy:.2f}")

    # Save results
    with open('C:/Users/BioBrain/Desktop/WS/WORK/final/test_results.txt', 'w',encoding='utf-8') as f:
        f.write(f"Test results for {target_person}:\n")
        f.write(f"Side video detection accuracy: {side_accuracy:.2f}\n")
        f.write(f"Main video detection accuracy: {main_accuracy:.2f}\n")
        f.write("\nDetailed results:\n")
        f.write("Individual video speaking times:\n")
        for time in individual_speaking_times:
            f.write(f"{time:.2f}\n")
        f.write("\nSide video detections:\n")
        for r in side_detections:
            f.write(f"Time: {r[0]:.2f}, Lip sync score: {r[2]:.2f}\n")
        f.write("\nMain video detections:\n")
        for r in main_detections:
            f.write(f"Time: {r[0]:.2f}, Lip sync score: {r[2]:.2f}\n")

    logger.info("Test results saved to test_results.txt")