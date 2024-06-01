import pytest
from backend.models import session, UserProgress

def test_create_user_progress():
    # Arrange
    new_progress = UserProgress(user_id=1, progress="50%")
    
    # Act
    session.add(new_progress)
    session.commit()
    
    # Assert
    saved_progress = session.query(UserProgress).filter_by(user_id=1).first()
    assert saved_progress.progress == "50%"
    session.delete(saved_progress)
    session.commit()
