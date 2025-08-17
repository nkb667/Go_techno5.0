from motor.motor_asyncio import AsyncIOMotorClient
from models import Achievement
import os

class Database:
    client: AsyncIOMotorClient = None
    database = None

database = Database()

async def get_database():
    return database.database

async def connect_to_mongo():
    """Create database connection"""
    database.client = AsyncIOMotorClient(os.environ["MONGO_URL"])
    database.database = database.client[os.environ["DB_NAME"]]
    
    # Create indexes for better performance
    await create_indexes()
    
    # Initialize default achievements
    await init_default_achievements()

async def close_mongo_connection():
    """Close database connection"""
    database.client.close()

async def create_indexes():
    """Create database indexes"""
    db = database.database
    
    # User indexes - removed email index since we don't use email anymore
    await db.users.create_index("id", unique=True)
    
    # Class indexes
    await db.classes.create_index("teacher_id")
    await db.classes.create_index("class_code", unique=True)
    
    # Lesson indexes
    await db.lessons.create_index("created_by")
    await db.lessons.create_index("difficulty")
    await db.lessons.create_index("order_index")
    
    # Quiz indexes
    await db.quizzes.create_index("lesson_id")
    await db.quizzes.create_index("created_by")
    
    # Progress indexes
    await db.lesson_progress.create_index([("user_id", 1), ("lesson_id", 1)], unique=True)
    await db.quiz_attempts.create_index("user_id")
    await db.quiz_attempts.create_index("quiz_id")
    
    # Achievement indexes
    await db.user_achievements.create_index([("user_id", 1), ("achievement_id", 1)], unique=True)
    
    # Notification indexes
    await db.notifications.create_index("user_id")
    await db.notifications.create_index("created_at")

async def init_default_achievements():
    """Initialize default achievements"""
    db = database.database
    
    default_achievements = [
        {
            "id": "first_lesson",
            "title": "First Steps",
            "description": "Complete your first lesson",
            "icon": "🎯",
            "points_reward": 50,
            "badge_color": "green",
            "criteria": {"lessons_completed": 1},
            "is_active": True
        },
        {
            "id": "quiz_master",
            "title": "Quiz Master",
            "description": "Score 100% on your first quiz",
            "icon": "🏆",
            "points_reward": 100,
            "badge_color": "gold",
            "criteria": {"perfect_quiz_score": 1},
            "is_active": True
        },
        {
            "id": "week_streak",
            "title": "Weekly Warrior",
            "description": "Maintain a 7-day learning streak",
            "icon": "🔥",
            "points_reward": 200,
            "badge_color": "orange",
            "criteria": {"streak_days": 7},
            "is_active": True
        },
        {
            "id": "go_beginner",
            "title": "GO Beginner",
            "description": "Complete 5 beginner lessons",
            "icon": "📚",
            "points_reward": 150,
            "badge_color": "blue",
            "criteria": {"beginner_lessons": 5},
            "is_active": True
        },
        {
            "id": "code_explorer",
            "title": "Code Explorer",
            "description": "Complete lessons from 3 different difficulty levels",
            "icon": "🗺️",
            "points_reward": 300,
            "badge_color": "purple",
            "criteria": {"difficulty_variety": 3},
            "is_active": True
        }
    ]
    
    for achievement in default_achievements:
        existing = await db.achievements.find_one({"id": achievement["id"]})
        if not existing:
            await db.achievements.insert_one(achievement)