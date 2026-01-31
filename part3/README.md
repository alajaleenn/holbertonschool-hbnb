
# HBnB Evolution Project - Part 3

## 📋 Project Overview
HBnB Evolution is a simplified Airbnb-like web application built with Flask, SQLAlchemy, and REST API principles. Part 3 focuses on database integration, authentication, and advanced features.

## ✅ Tasks Completed (Part 3)

### Task 4: Administrator Access Endpoints
- ✅ JWT-based authentication with role-based access control
- ✅ Admin-only endpoints for user management
- ✅ Admin bypass for place and review ownership restrictions
- ✅ Protected endpoints with `@admin_required` decorator

### Task 5: SQLAlchemy Repository Implementation  
- ✅ Replaced in-memory repository with SQLAlchemy-based repository
- ✅ `SQLAlchemyRepository` generic implementation
- ✅ `UserRepository` specialized for user operations
- ✅ `RepositoryFactory` for creating model-specific repositories
- ✅ Database session management and transactions

### Task 6: Map User Entity to SQLAlchemy Model
- ✅ User model with SQLAlchemy ORM mapping
- ✅ Password hashing with bcrypt
- ✅ Unique email constraint and indexing
- ✅ Admin flag for role-based access
- ✅ Complete CRUD operations through repository

### Task 7: Map Place, Review, and Amenity Entities
- ✅ Place model with location data (latitude, longitude)
- ✅ Review model with rating validation (1-5)
- ✅ Amenity model with unique name constraint
- ✅ All models inherit from SQLAlchemy BaseModel
- ✅ Data validation and business logic in models

### Task 8: Map Relationships Between Entities
- ✅ **One-to-Many**: User → Places (owns), User → Reviews (writes), Place → Reviews (has)
- ✅ **Many-to-Many**: Place ↔ Amenity through association table
- ✅ Foreign key constraints with cascade delete
- ✅ SQLAlchemy relationship() and backref configurations

### Task 9: SQL Scripts for Database Schema
- ✅ `schema.sql` - Complete database schema with tables, constraints, and indexes
- ✅ `data.sql` - Initial data including admin user and amenities
- ✅ `queries.sql` - Sample CRUD operations for testing
- ✅ Support for UUID primary keys and foreign key relationships

### Task 10: Generate ER Diagrams with Mermaid.js
- ✅ `er_diagram.mmd` - Mermaid.js ER diagram source code
- ✅ `ER_DIAGRAM.md` - Complete documentation with visual diagram
- ✅ Shows all tables, relationships, and attributes
- ✅ Professional database documentation

## 🗄️ Database Schema

### Tables
1. **users** - User accounts with authentication
2. **places** - Property listings with geolocation
3. **amenities** - Features available at properties  
4. **reviews** - User reviews with ratings
5. **place_amenity** - Many-to-many association table

### Key Features
- **UUID Primary Keys**: All tables use UUID for distributed compatibility
- **Foreign Keys**: Relationships with CASCADE delete
- **Indexes**: Optimized for common queries (email, price, rating)
- **Constraints**: Data validation at database level
- **Timestamps**: Automatic created_at and updated_at tracking

## 🔧 Technology Stack

### Backend
- **Python 3.10+** - Primary programming language
- **Flask 3.0** - Web framework
- **SQLAlchemy 3.0** - ORM and database toolkit
- **Flask-RESTX** - REST API framework with Swagger UI
- **Flask-JWT-Extended** - Authentication and authorization
- **bcrypt** - Password hashing

### Database
- **SQLite** - Development database (can be replaced with PostgreSQL in production)
- **SQLAlchemy ORM** - Object-relational mapping
- **Alembic** - Database migrations (ready for use)

## 🚀 Getting Started

### 1. Installation
```bash
# Clone repository
git clone https://github.com/alajaleenn/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part3

# Install dependencies
pip install -r requirements.txt
