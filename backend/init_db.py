#!/usr/bin/env python3
"""
Initialize database and create test users on first startup
"""
import os
import sys
import time
from sqlalchemy import inspect

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def wait_for_db():
    """Wait for database to be ready"""
    from app.database import engine
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # Try to connect
            inspector = inspect(engine)
            inspector.get_table_names()
            print("✅ Database connection established", flush=True)
            return True
        except Exception as e:
            retry_count += 1
            print(f"⏳ Waiting for database... ({retry_count}/{max_retries})", flush=True)
            time.sleep(2)
    
    print("❌ Could not connect to database", flush=True)
    return False

def init_database():
    """Initialize database tables"""
    try:
        from app.database import Base, engine
        print("📦 Creating database tables...", flush=True)
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created", flush=True)
        return True
    except Exception as e:
        print(f"❌ Error creating tables: {e}", flush=True)
        return False

def create_test_users():
    """Create 10 test users if they don't exist"""
    try:
        from sqlalchemy.orm import Session
        from app.database import SessionLocal
        from app.models import User, Profile, Interest, Skill
        from app.auth import get_password_hash
        
        db = SessionLocal()
        
        # Check if users already exist
        existing_users = db.query(User).count()
        if existing_users >= 10:
            print(f"✅ Database already has {existing_users} users. Skipping creation.", flush=True)
            db.close()
            return True
        
        print("🌱 Creating 10 test users...", flush=True)
        
        # Create interests
        interests_data = [
            "Programming", "Technology", "Gaming", "Hiking", "Artificial Intelligence", 
            "Web Development", "Photography", "Traveling", "Art", "Graphic Design", 
            "Cooking", "Movies", "Weightlifting", "Running", "Entrepreneurship", 
            "Marketing", "Swimming", "Data Science", "Research", "Reading", 
            "Music", "Video Editing", "Yoga", "Dancing", "Basketball",
            "Soccer", "Tennis", "Painting", "Writing", "Gardening"
        ]
        
        for interest_name in interests_data:
            existing = db.query(Interest).filter(Interest.name == interest_name).first()
            if not existing:
                interest = Interest(name=interest_name, category="General")
                db.add(interest)
        db.commit()
        
        # Create skills
        skills_data = [
            "Python", "JavaScript", "React", "Node.js", "Machine Learning", "Git", 
            "Docker", "Adobe Photoshop", "Adobe Illustrator", "Figma", "UI/UX Design", 
            "Content Creation", "Brand Design", "Leadership", "Project Management", 
            "Communication", "Public Speaking", "Teamwork", "Problem Solving", 
            "Data Analysis", "SQL", "Music Production", "Audio Engineering", "Sound Design",
            "Java", "C++", "PHP", "Ruby", "Swift", "Kotlin"
        ]
        
        for skill_name in skills_data:
            existing = db.query(Skill).filter(Skill.name == skill_name).first()
            if not existing:
                skill = Skill(name=skill_name, category="General")
                db.add(skill)
        db.commit()
        
        # Test accounts data
        test_accounts = [
            {
                "email": "john.doe@example.com", "password": "password123",
                "first_name": "John", "last_name": "Doe", "age": 28, "city": "San Francisco",
                "bio": "Passionate software developer with 5+ years of experience in full-stack development. Love working with Python and JavaScript. Currently exploring machine learning and AI. Always excited to collaborate on innovative tech projects and startups.",
                "search_goals": "Looking for work partners and friends with similar interests in technology and entrepreneurship.",
                "interests": ["Programming", "Technology", "Gaming", "Hiking", "Artificial Intelligence", "Web Development"],
                "skills": ["Python", "JavaScript", "React", "Node.js", "Machine Learning", "Git", "Docker"]
            },
            {
                "email": "jane.smith@example.com", "password": "password123",
                "first_name": "Jane", "last_name": "Smith", "age": 25, "city": "New York",
                "bio": "Creative UI/UX designer and digital artist with a passion for beautiful, functional design. I specialize in Adobe Creative Suite and Figma. Love exploring new places and capturing moments through photography.",
                "search_goals": "Seeking friends for travel adventures and creative collaborations.",
                "interests": ["Photography", "Traveling", "Art", "Graphic Design", "Cooking", "Movies"],
                "skills": ["Adobe Photoshop", "Adobe Illustrator", "Figma", "UI/UX Design", "Content Creation", "Brand Design"]
            },
            {
                "email": "mike.wilson@example.com", "password": "password123",
                "first_name": "Mike", "last_name": "Wilson", "age": 32, "city": "Los Angeles",
                "bio": "Fitness enthusiast, certified personal trainer, and entrepreneur. Founded two successful fitness startups in LA. Passionate about health, wellness, and helping others achieve their goals.",
                "search_goals": "Looking for workout partners and business collaborators.",
                "interests": ["Weightlifting", "Running", "Entrepreneurship", "Marketing", "Hiking", "Swimming"],
                "skills": ["Leadership", "Project Management", "Communication", "Public Speaking", "Teamwork", "Problem Solving"]
            },
            {
                "email": "sarah.johnson@example.com", "password": "password123",
                "first_name": "Sarah", "last_name": "Johnson", "age": 29, "city": "Chicago",
                "bio": "Data scientist and AI researcher with a PhD in Computer Science. Working at the intersection of machine learning and social impact. Passionate about using data to solve real-world problems.",
                "search_goals": "Interested in connecting with other data professionals and researchers.",
                "interests": ["Data Science", "Research", "Reading", "Artificial Intelligence", "Technology", "Programming"],
                "skills": ["Python", "Data Analysis", "Machine Learning", "SQL", "Problem Solving", "Communication"]
            },
            {
                "email": "alex.brown@example.com", "password": "password123",
                "first_name": "Alex", "last_name": "Brown", "age": 26, "city": "Seattle",
                "bio": "Professional musician, music producer, and audio engineer. Specialized in electronic music production and sound design. Love experimenting with new sounds and collaborating with other creatives.",
                "search_goals": "Looking for fellow musicians and music lovers to collaborate with.",
                "interests": ["Music", "Gaming", "Movies", "Video Editing", "Photography", "Art"],
                "skills": ["Music Production", "Audio Engineering", "Sound Design", "Content Creation", "Communication", "Teamwork"]
            },
            {
                "email": "emma.davis@example.com", "password": "password123",
                "first_name": "Emma", "last_name": "Davis", "age": 27, "city": "Boston",
                "bio": "Marketing specialist and content strategist with expertise in digital marketing and social media. Helped several startups grow their online presence.",
                "search_goals": "Seeking networking opportunities with marketing professionals and entrepreneurs.",
                "interests": ["Marketing", "Writing", "Yoga", "Reading", "Photography", "Traveling"],
                "skills": ["Project Management", "Communication", "Content Creation", "Leadership", "Brand Design", "Public Speaking"]
            },
            {
                "email": "david.martinez@example.com", "password": "password123",
                "first_name": "David", "last_name": "Martinez", "age": 31, "city": "Austin",
                "bio": "Full-stack developer and tech educator. Teaching coding bootcamps and creating online courses. Passionate about making technology accessible to everyone.",
                "search_goals": "Looking to connect with other developers, educators, and students.",
                "interests": ["Programming", "Technology", "Basketball", "Gaming", "Web Development", "Teaching"],
                "skills": ["JavaScript", "React", "Node.js", "Python", "Git", "Communication", "Leadership"]
            },
            {
                "email": "olivia.taylor@example.com", "password": "password123",
                "first_name": "Olivia", "last_name": "Taylor", "age": 24, "city": "Miami",
                "bio": "Aspiring entrepreneur and business student. Working on my first startup in the e-commerce space. Passionate about innovation, sustainability, and social entrepreneurship.",
                "search_goals": "Seeking mentors, co-founders, and fellow entrepreneurs.",
                "interests": ["Entrepreneurship", "Dancing", "Traveling", "Reading", "Art", "Cooking"],
                "skills": ["Leadership", "Project Management", "Problem Solving", "Communication", "Marketing", "Teamwork"]
            },
            {
                "email": "james.anderson@example.com", "password": "password123",
                "first_name": "James", "last_name": "Anderson", "age": 30, "city": "Denver",
                "bio": "Outdoor enthusiast and nature photographer. Work as a freelance photographer specializing in landscape and adventure photography. Love hiking and exploring the Rocky Mountains.",
                "search_goals": "Seeking outdoor adventure partners and photography collaborators.",
                "interests": ["Photography", "Hiking", "Traveling", "Art", "Gardening", "Movies"],
                "skills": ["Adobe Photoshop", "Content Creation", "Problem Solving", "Communication", "Teamwork", "UI/UX Design"]
            },
            {
                "email": "sophia.lee@example.com", "password": "password123",
                "first_name": "Sophia", "last_name": "Lee", "age": 26, "city": "Portland",
                "bio": "UX researcher and human-computer interaction specialist. Master's degree in HCI. Passionate about creating user-centered designs and improving digital experiences.",
                "search_goals": "Looking to network with UX professionals, designers, and researchers.",
                "interests": ["Technology", "Art", "Yoga", "Reading", "Painting", "Research"],
                "skills": ["UI/UX Design", "Figma", "Data Analysis", "Communication", "Problem Solving", "Leadership"]
            }
        ]
        
        created_count = 0
        for account_data in test_accounts:
            # Check if user exists
            existing_user = db.query(User).filter(User.email == account_data["email"]).first()
            if existing_user:
                continue
            
            # Create user
            user = User(
                email=account_data["email"],
                hashed_password=get_password_hash(account_data["password"]),
                is_active=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            
            # Create profile
            profile = Profile(
                user_id=user.id,
                first_name=account_data["first_name"],
                last_name=account_data["last_name"],
                age=account_data["age"],
                city=account_data["city"],
                bio=account_data["bio"],
                search_goals=account_data["search_goals"],
                is_profile_complete=True
            )
            db.add(profile)
            db.commit()
            
            # Add interests
            for interest_name in account_data["interests"]:
                interest = db.query(Interest).filter(Interest.name == interest_name).first()
                if interest:
                    user.interests.append(interest)
            
            # Add skills
            for skill_name in account_data["skills"]:
                skill = db.query(Skill).filter(Skill.name == skill_name).first()
                if skill:
                    user.skills.append(skill)
            
            db.commit()
            created_count += 1
            print(f"✅ Created: {account_data['first_name']} {account_data['last_name']} ({account_data['email']})", flush=True)
        
        db.close()
        print(f"🎉 Successfully created {created_count} test users!", flush=True)
        print("📧 All accounts use password: password123", flush=True)
        return True
        
    except Exception as e:
        print(f"❌ Error creating test users: {e}", flush=True)
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Initializing database...", flush=True)
    
    if not wait_for_db():
        sys.exit(1)
    
    if not init_database():
        sys.exit(1)
    
    if not create_test_users():
        sys.exit(1)
    
    print("✅ Database initialization complete!", flush=True)

