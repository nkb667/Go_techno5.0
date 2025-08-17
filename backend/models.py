from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
import uuid

class UserRole(str, Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"

class QuestionType(str, Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    CODE_COMPLETION = "code_completion"
    FREE_TEXT = "free_text"

class DifficultyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

# User Models - Simplified for code-based authentication
class UserBase(BaseModel):
    full_name: str
    role: UserRole = UserRole.STUDENT
    is_active: bool = True

class User(UserBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    profile_image: Optional[str] = None
    points: int = 0
    level: int = 1
    streak_days: int = 0
    last_activity: Optional[datetime] = None

# Class Models
class ClassBase(BaseModel):
    name: str
    description: Optional[str] = None
    grade_level: Optional[str] = None

class ClassCreate(ClassBase):
    pass

class Class(ClassBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    teacher_id: str
    students: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True
    class_code: str = Field(default_factory=lambda: str(uuid.uuid4())[:8].upper())

# Lesson Models
class LessonBase(BaseModel):
    title: str
    content: str
    description: Optional[str] = None
    difficulty: DifficultyLevel = DifficultyLevel.BEGINNER
    estimated_time: int = 30  # minutes
    go_code_examples: List[str] = []
    key_concepts: List[str] = []

class LessonCreate(LessonBase):
    pass

class Lesson(LessonBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_by: str  # teacher/admin id
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_published: bool = False
    order_index: int = 0
    points_reward: int = 10

# Quiz Models
class QuizQuestion(BaseModel):
    question: str
    question_type: QuestionType
    options: Optional[List[str]] = None  # for multiple choice
    correct_answer: str
    explanation: Optional[str] = None
    points: int = 1

class QuizBase(BaseModel):
    title: str
    description: Optional[str] = None
    lesson_id: str
    questions: List[QuizQuestion] = []
    time_limit: Optional[int] = None  # minutes
    passing_score: int = 70  # percentage

class QuizCreate(QuizBase):
    pass

class Quiz(QuizBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_by: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True
    max_points: int = 0

# Progress Models
class LessonProgress(BaseModel):
    user_id: str
    lesson_id: str
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    is_completed: bool = False
    time_spent: int = 0  # minutes
    notes: Optional[str] = None

class QuizAttempt(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    quiz_id: str
    answers: Dict[str, Any] = {}
    score: float = 0.0
    max_score: float = 0.0
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    is_completed: bool = False
    time_taken: int = 0  # seconds

# Achievement Models
class Achievement(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    icon: str
    points_reward: int
    badge_color: str = "blue"
    criteria: Dict[str, Any]  # flexible criteria for different achievements
    is_active: bool = True

class UserAchievement(BaseModel):
    user_id: str
    achievement_id: str
    earned_at: datetime = Field(default_factory=datetime.utcnow)
    progress: float = 0.0  # for progressive achievements

# Notification Models
class Notification(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    title: str
    message: str
    type: str = "info"  # success, error, warning, info
    is_read: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    action_url: Optional[str] = None

# Analytics Models
class UserStats(BaseModel):
    user_id: str
    lessons_completed: int = 0
    quizzes_completed: int = 0
    total_points: int = 0
    current_streak: int = 0
    longest_streak: int = 0
    time_spent_learning: int = 0  # minutes
    average_quiz_score: float = 0.0
    achievements_earned: int = 0
    last_updated: datetime = Field(default_factory=datetime.utcnow)

# API Response Models
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: User

class APIResponse(BaseModel):
    success: bool = True
    message: str = ""
    data: Optional[Any] = None