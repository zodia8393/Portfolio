import asyncio
import logging
from config import load_config
from meeting_analyzer import MeetingAnalyzer
import json
import aiohttp

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_perplexity_api(api_key, api_url):
    sample_transcript = "Person1: Hello everyone. Today we are discussing the project overview."
    async with aiohttp.ClientSession() as session:
        async with session.post(
            api_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.1-sonar-huge-128k-online",
                "messages": [
                    {"role": "system", "content": "You are a helpful korean assistant that summarizes meeting transcripts."},
                    {"role": "user", "content": f"Please summarize the following meeting transcript in korean:\n\n{sample_transcript}"}
                ]
            }
        ) as response:
            result = await response.json()
            return result

async def main():
    logger.info("Starting the meeting analysis process")
    config = load_config()
    logger.info("Configuration loaded successfully")

    # Perplexity API 테스트
    logger.info("Testing Perplexity API")
    api_test_result = await test_perplexity_api(config.PERPLEXITY.api_key, config.PERPLEXITY.api_url)
    logger.info(f"Perplexity API test result: {api_test_result}")

    analyzer = MeetingAnalyzer(config)
    logger.info("MeetingAnalyzer initialized")

    if config.TEST.enabled:
        logger.info("Running in test mode")
        participants = {
            config.TEST.target_person: {
                "video": config.TEST.individual_video_path,
                "audio": config.TEST.individual_audio_path
            }
        }
        start_time = config.TEST.start_time
        end_time = config.TEST.end_time
    else:
        logger.info("Running in normal mode")
        participants = config.PARTICIPANTS
        start_time = 0
        end_time = None

    logger.info(f"Analyzing meeting for {len(participants)} participants")
    segments, summary = await analyzer.analyze_meeting(participants, start_time, end_time)

    logger.info("Saving analysis results")
    with open('C:/Users/BioBrain/Desktop/WS/WORK/final/result/meeting_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(segments, f, ensure_ascii=False, indent=2)
    
    with open('C:/Users/BioBrain/Desktop/WS/WORK/final/result/meeting_summary.txt', 'w', encoding='utf-8') as f:
        f.write(summary)

    logger.info("Meeting analysis complete. Results saved to meeting_analysis.json and meeting_summary.txt")

if __name__ == "__main__":
    asyncio.run(main())