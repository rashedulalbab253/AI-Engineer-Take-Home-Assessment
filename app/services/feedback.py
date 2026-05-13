from app.db.database import SessionLocal
from app.db.models import FeedbackRecord

def process_feedback(draft_id: str, context: str, replace_dict: dict):
    db = SessionLocal()
    learned_count = 0
    try:
        for old_text, new_text in replace_dict.items():
            record = FeedbackRecord(
                draft_id=draft_id,
                context=context,
                replace_from=old_text,
                replace_to=new_text
            )
            db.add(record)
            learned_count += 1
        db.commit()
        return learned_count
    finally:
        db.close()

def get_learned_preferences():
    db = SessionLocal()
    try:
        records = db.query(FeedbackRecord).all()
        preferences = {}
        for r in records:
            preferences[r.replace_from] = r.replace_to
        return preferences
    finally:
        db.close()
