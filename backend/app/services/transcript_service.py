from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled

class TranscriptService:
    def fetch(self, video_id: str):
        try:
            return YouTubeTranscriptApi().fetch(video_id)
        except TranscriptsDisabled as exc:
            raise RuntimeError("This YouTube video has no available captions.") from exc
        except Exception as exc:
            raise RuntimeError(f"Unable to fetch transcript: {exc}") from exc
