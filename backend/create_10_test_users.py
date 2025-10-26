#!/usr/bin/env python3
"""
Script to create 10 test users with complete profiles, skills, and interests
"""

import sys
import os

# Set SQLite database URL
os.environ['DATABASE_URL'] = 'sqlite:///./people_search.db'

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import User, Profile, Interest, Skill
from app.auth import get_password_hash

def setup_database():
    """Create all database tables"""
    print("📦 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created\n")

def create_10_test_users():
    """Create 10 test users with complete profiles"""
    db = SessionLocal()
    
    try:
        print("🌱 Creating 10 Complete Test Users")
        print("=" * 60)
        
        # Create interests
        print("\n📝 Creating interests...")
        interests_data = [
            "Programming", "Technology", "Gaming", "Hiking", "Artificial Intelligence", 
            "Web Development", "Photography", "Traveling", "Art", "Graphic Design", 
            "Cooking", "Movies", "Weightlifting", "Running", "Entrepreneurship", 
            "Marketing", "Swimming", "Data Science", "Research", "Reading", 
            "Music", "Video Editing", "Yoga", "Dancing", "Basketball",
            "Soccer", "Tennis", "Painting", "Writing", "Gardening"
        ]
        
        created_interests = 0
        for interest_name in interests_data:
            existing = db.query(Interest).filter(Interest.name == interest_name).first()
            if not existing:
                interest = Interest(name=interest_name, category="General")
                db.add(interest)
                created_interests += 1
        db.commit()
        print(f"✅ Created {created_interests} new interests")
        
        # Create skills
        print("\n🛠️ Creating skills...")
        skills_data = [
            "Python", "JavaScript", "React", "Node.js", "Machine Learning", "Git", 
            "Docker", "Adobe Photoshop", "Adobe Illustrator", "Figma", "UI/UX Design", 
            "Content Creation", "Brand Design", "Leadership", "Project Management", 
            "Communication", "Public Speaking", "Teamwork", "Problem Solving", 
            "Data Analysis", "SQL", "Music Production", "Audio Engineering", "Sound Design",
            "Java", "C++", "PHP", "Ruby", "Swift", "Kotlin"
        ]
        
        created_skills = 0
        for skill_name in skills_data:
            existing = db.query(Skill).filter(Skill.name == skill_name).first()
            if not existing:
                skill = Skill(name=skill_name, category="General")
                db.add(skill)
                created_skills += 1
        db.commit()
        print(f"✅ Created {created_skills} new skills")
        
        # Test accounts data
        test_accounts = [
            {
                "email": "john.doe@example.com",
                "password": "password123",
                "first_name": "John",
                "last_name": "Doe",
                "age": 28,
                "city": "San Francisco",
                "bio": "Passionate software developer with 5+ years of experience in full-stack development. Love working with Python and JavaScript. Currently exploring machine learning and AI. Always excited to collaborate on innovative tech projects and startups. When I'm not coding, you'll find me gaming or hiking in the Bay Area.",
                "search_goals": "Looking for work partners and friends with similar interests in technology and entrepreneurship. Open to co-founding a startup!",
                "interests": ["Programming", "Technology", "Gaming", "Hiking", "Artificial Intelligence", "Web Development"],
                "skills": ["Python", "JavaScript", "React", "Node.js", "Machine Learning", "Git", "Docker"]
            },
            {
                "email": "jane.smith@example.com",
                "password": "password123",
                "first_name": "Jane",
                "last_name": "Smith",
                "age": 25,
                "city": "New York",
                "bio": "Creative UI/UX designer and digital artist with a passion for beautiful, functional design. I specialize in Adobe Creative Suite and Figma. Love exploring new places, trying different cuisines, and capturing moments through photography. Recently got into content creation and building my portfolio. Looking to collaborate on creative projects!",
                "search_goals": "Seeking friends for travel adventures and creative collaborations. Interested in finding design partners for freelance projects.",
                "interests": ["Photography", "Traveling", "Art", "Graphic Design", "Cooking", "Movies"],
                "skills": ["Adobe Photoshop", "Adobe Illustrator", "Figma", "UI/UX Design", "Content Creation", "Brand Design"]
            },
            {
                "email": "mike.wilson@example.com",
                "password": "password123",
                "first_name": "Mike",
                "last_name": "Wilson",
                "age": 32,
                "city": "Los Angeles",
                "bio": "Fitness enthusiast, certified personal trainer, and entrepreneur. Founded two successful fitness startups in LA. Passionate about health, wellness, and helping others achieve their goals. Strong believer in work-life balance. Love weightlifting, running marathons, and networking with like-minded professionals. Always up for a challenge!",
                "search_goals": "Looking for workout partners and business collaborators. Interested in connecting with other entrepreneurs and fitness professionals.",
                "interests": ["Weightlifting", "Running", "Entrepreneurship", "Marketing", "Hiking", "Swimming"],
                "skills": ["Leadership", "Project Management", "Communication", "Public Speaking", "Teamwork", "Problem Solving"]
            },
            {
                "email": "sarah.johnson@example.com",
                "password": "password123",
                "first_name": "Sarah",
                "last_name": "Johnson",
                "age": 29,
                "city": "Chicago",
                "bio": "Data scientist and AI researcher with a PhD in Computer Science. Working at the intersection of machine learning and social impact. Passionate about using data to solve real-world problems and make a positive difference. Published several papers on predictive analytics. Love reading, attending tech conferences, and mentoring aspiring data scientists.",
                "search_goals": "Interested in connecting with other data professionals, researchers, and anyone passionate about using technology for good. Open to collaboration on research projects.",
                "interests": ["Data Science", "Research", "Reading", "Artificial Intelligence", "Technology", "Programming"],
                "skills": ["Python", "Data Analysis", "Machine Learning", "SQL", "Problem Solving", "Communication"]
            },
            {
                "email": "alex.brown@example.com",
                "password": "password123",
                "first_name": "Alex",
                "last_name": "Brown",
                "age": 26,
                "city": "Seattle",
                "bio": "Professional musician, music producer, and audio engineer. Specialized in electronic music production and sound design. Have a home studio where I create beats and produce for local artists. Love experimenting with new sounds and collaborating with other creatives. Also into gaming, movies, and attending live concerts. Let's make some music together!",
                "search_goals": "Looking for fellow musicians and music lovers to collaborate and perform with. Interested in forming a band or working on music production projects.",
                "interests": ["Music", "Gaming", "Movies", "Video Editing", "Photography", "Art"],
                "skills": ["Music Production", "Audio Engineering", "Sound Design", "Content Creation", "Communication", "Teamwork"]
            },
            {
                "email": "emma.davis@example.com",
                "password": "password123",
                "first_name": "Emma",
                "last_name": "Davis",
                "age": 27,
                "city": "Boston",
                "bio": "Marketing specialist and content strategist with expertise in digital marketing and social media. Helped several startups grow their online presence. Passionate about storytelling, branding, and creating engaging content. Love yoga, reading mystery novels, and exploring new coffee shops. Always looking to learn and grow professionally.",
                "search_goals": "Seeking networking opportunities with marketing professionals and entrepreneurs. Interested in freelance collaborations and startup projects.",
                "interests": ["Marketing", "Writing", "Yoga", "Reading", "Photography", "Traveling"],
                "skills": ["Project Management", "Communication", "Content Creation", "Leadership", "Brand Design", "Public Speaking"]
            },
            {
                "email": "david.martinez@example.com",
                "password": "password123",
                "first_name": "David",
                "last_name": "Martinez",
                "age": 31,
                "city": "Austin",
                "bio": "Full-stack developer and tech educator. Teaching coding bootcamps and creating online courses. Passionate about making technology accessible to everyone. Expert in JavaScript, React, and Node.js. Love basketball, gaming, and attending tech meetups. Believe in continuous learning and giving back to the community.",
                "search_goals": "Looking to connect with other developers, educators, and students. Open to mentoring opportunities and collaborative projects.",
                "interests": ["Programming", "Technology", "Basketball", "Gaming", "Teaching", "Web Development"],
                "skills": ["JavaScript", "React", "Node.js", "Python", "Git", "Communication", "Leadership"]
            },
            {
                "email": "olivia.taylor@example.com",
                "password": "password123",
                "first_name": "Olivia",
                "last_name": "Taylor",
                "age": 24,
                "city": "Miami",
                "bio": "Aspiring entrepreneur and business student. Working on my first startup in the e-commerce space. Passionate about innovation, sustainability, and social entrepreneurship. Love dancing, traveling, and meeting inspiring people. Always eager to learn from experienced entrepreneurs and build meaningful connections.",
                "search_goals": "Seeking mentors, co-founders, and fellow entrepreneurs. Interested in networking events and startup communities.",
                "interests": ["Entrepreneurship", "Dancing", "Traveling", "Reading", "Art", "Cooking"],
                "skills": ["Leadership", "Project Management", "Problem Solving", "Communication", "Marketing", "Teamwork"]
            },
            {
                "email": "james.anderson@example.com",
                "password": "password123",
                "first_name": "James",
                "last_name": "Anderson",
                "age": 30,
                "city": "Denver",
                "bio": "Outdoor enthusiast and nature photographer. Work as a freelance photographer specializing in landscape and adventure photography. Love hiking, camping, and exploring the Rocky Mountains. Also passionate about environmental conservation. Looking to collaborate on outdoor projects and connect with fellow nature lovers.",
                "search_goals": "Seeking outdoor adventure partners and photography collaborators. Interested in environmental initiatives and conservation projects.",
                "interests": ["Photography", "Hiking", "Traveling", "Art", "Gardening", "Movies"],
                "skills": ["Adobe Photoshop", "Content Creation", "Problem Solving", "Communication", "Teamwork", "UI/UX Design"]
            },
            {
                "email": "sophia.lee@example.com",
                "password": "password123",
                "first_name": "Sophia",
                "last_name": "Lee",
                "age": 26,
                "city": "Portland",
                "bio": "UX researcher and human-computer interaction specialist. Master's degree in HCI. Passionate about creating user-centered designs and improving digital experiences. Love reading, painting, and practicing yoga. Interested in accessibility, inclusive design, and the future of technology. Always curious and eager to learn.",
                "search_goals": "Looking to network with UX professionals, designers, and researchers. Open to collaborative research projects and design sprints.",
                "interests": ["Technology", "Art", "Yoga", "Reading", "Painting", "Research"],
                "skills": ["UI/UX Design", "Figma", "Data Analysis", "Communication", "Problem Solving", "Leadership"]
            }
        ]
        
        print("\n👥 Creating test accounts...")
        print("=" * 60)
        
        for account_data in test_accounts:
            # Check if user exists
            existing_user = db.query(User).filter(User.email == account_data["email"]).first()
            if existing_user:
                print(f"⚠️  {account_data['first_name']} {account_data['last_name']} ({account_data['email']}) - Already exists")
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
            
            print(f"✅ {account_data['first_name']} {account_data['last_name']} ({account_data['email']})")
            print(f"   📍 {account_data['city']} | 🎂 {account_data['age']} years old")
            print(f"   💡 {len(account_data['interests'])} interests | 🛠️  {len(account_data['skills'])} skills")
            print()
        
        print("=" * 60)
        print("🎉 All 10 test accounts created successfully!")
        print("\n📋 Login Credentials (all accounts):")
        print("   Password: password123")
        print("\n📧 Test Account Emails:")
        for account in test_accounts:
            print(f"   • {account['email']} - {account['first_name']} from {account['city']}")
        
        print("\n🚀 You can now log in with any of these accounts!")
        
    except Exception as e:
        print(f"❌ Error creating test accounts: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    setup_database()
    create_10_test_users()

