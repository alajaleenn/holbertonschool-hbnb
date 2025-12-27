# HBnB Evolution - Technical Documentation

Project: HBnB Evolution  
Date: December 2024  
Team: Thekra Alhenaki, Najla Alajaleen, Noura Alqahtani

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [High-Level Architecture](#2-high-level-architecture)
3. [Business Logic Layer](#3-business-logic-layer)
4. [API Interaction Flow](#4-api-interaction-flow)

---

## 1. Introduction

HBnB Evolution is a simplified Airbnb-like application that manages property rentals, user reviews, and amenities. The system enables users to register, list properties, write reviews, and browse available rentals.

Core Features:
- User registration and profile management
- Property listings with pricing and location
- User reviews with ratings
- Amenity management for properties

Purpose of This Document:
This technical documentation provides the architectural blueprint for the HBnB Evolution application, detailing the system's design, component interactions, and data flow. It serves as a guide for the implementation phases.

---

## 2. High-Level Architecture

### 2.1 Three-Layer Architecture

The application follows a layered architecture pattern with three distinct layers:

1. Presentation Layer: Handles API requests and user interactions
2. Business Logic Layer: Implements core business rules and entity management
3. Persistence Layer: Manages database operations and data storage

These layers communicate through the Facade Pattern, providing simplified interfaces between layers and reducing coupling.

### 2.2 Package Diagram
classDiagram
    class PresentationLayer {
        <<Interface>>
        +ServiceAPI
        +handleRequests()
    }
    class BusinessLogicLayer {
        +User
        +Place
        +Review
        +Amenity
        +FacadeService
        +processLogic()
    }
    class PersistenceLayer {
        +DatabaseAccess
        +saveData()
        +retrieveData()
    }
    PresentationLayer --> BusinessLogicLayer : Facade Pattern
    BusinessLogicLayer --> PersistenceLayer : Database Operations

### 2.3 Architecture Explanation

Presentation Layer:
- Exposes RESTful API endpoints
- Validates incoming requests
- Formats responses as JSON
- Communicates with Business Logic via Facade

Business Logic Layer:
- Contains domain entities (User, Place, Review, Amenity)
- Enforces business rules and validation
- Independent of presentation and persistence details
- Provides Facade interface for Presentation Layer

Persistence Layer:
- Handles database connections and queries
- Provides data access abstraction
- Ensures data integrity and consistency

Facade Pattern Benefits:
- Simplifies inter-layer communication
- Reduces coupling between layers
- Each layer can be modified independently
- Improves testability

---

## 3. Business Logic Layer

### 3.1 Overview

The Business Logic Layer contains the core entities and business rules. All entities inherit from a BaseModel class to share common attributes (id, timestamps) and methods (save, delete).

### 3.2 Class Diagram
classDiagram
    class BaseModel {
        #String id
        #DateTime createdAt
        #DateTime updatedAt
        +save() bool
        +delete() bool
        +toDict() dict
    }

    class User {
        -String firstName
        -String lastName
        -String email
        -String password
        -Boolean isAdmin
        +register() bool
        +updateProfile(data: dict) bool
        +getPlaces() List~Place~
        +getReviews() List~Review~
    }

    class Place {
        -String title
        -String description
        -Float price
        -Float latitude
        -Float longitude
        +create(ownerID: String) bool
        +update(data: dict) bool
        +addAmenity(amenityID: String) bool
        +removeAmenity(amenityID: String) bool
        +getReviews() List~Review~
        +getAmenities() List~Amenity~
    }

    class Review {
        -Integer rating
        -String comment
        +create(userID: String, placeID: String) bool
        +update(data: dict) bool
        +getPlace() Place
        +getReviewer() User
    }class Amenity {
        -String name
        -String description
        +create(data: dict) bool
        +update(data: dict) bool
    }

    BaseModel <|-- User
    BaseModel <|-- Place
    BaseModel <|-- Review
    BaseModel <|-- Amenity

    User "1" -- "0..*" Place : owns
    User "1" -- "0..*" Review : writes
    Place "1" -- "0..*" Review : has
    Place "0..*" -- "0..*" Amenity : includes

### 3.3 Entity Descriptions

BaseModel:
- Parent class providing common functionality
- Attributes: Unique ID (UUID4), creation timestamp, update timestamp
- Methods: Save to database, delete from database, convert to dictionary

User:
- Represents platform users (regular users and administrators)
- Key attributes: Name, email (unique), hashed password, admin flag
- Key methods: Registration with validation, profile updates, retrieve owned places and reviews
- Business rules: Email must be unique, passwords are hashed

Place:
- Represents rental properties
- Key attributes: Title, description, price, geographical coordinates
- Relationships: Owned by one user, can have multiple amenities and reviews
- Key methods: Create with owner, update details, manage amenities
- Business rules: Price must be positive, coordinates must be valid ranges

Review:
- Represents user feedback for places
- Key attributes: Rating (1-5), comment text
- Relationships: Written by one user, belongs to one place
- Key methods: Create review, update content
- Business rules: Users cannot review own places, one review per user per place

Amenity:
- Represents property features (WiFi, Pool, etc.)
- Key attributes: Name (unique), description
- Relationships: Can be associated with multiple places (many-to-many)
- Key methods: Create amenity, update details

### 3.4 Key Relationships

Inheritance (BaseModel → All Entities):
- All entities inherit common attributes and methods
- Implements DRY principle
- Ensures consistency

Associations:
- User → Place (1 to many): One user owns multiple places
- User → Review (1 to many): One user writes multiple reviews
- Place → Review (1 to many): One place has multiple reviews
- Place ↔️ Amenity (many to many): Places share amenities, requiring junction table

### 3.5 Design Decisions

- Encapsulation: Private attributes with public methods ensure data validation
- Loose Coupling: Entities reference each other by ID, not full objects
- Single Responsibility: Each entity has one clear purpose
- toDict() Method: Enables JSON serialization for API responses

---

## 4. API Interaction Flow

### 4.1 User Registration
sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Database
    User->>API: Register User (email, password, etc.)
    API->>BusinessLogic: Validate and Process Request
    BusinessLogic->>Database: Store User Data
    Database-->>BusinessLogic: Confirm Save
    BusinessLogic-->>API: Return Success/Failure
    API-->>User: Registration Successful/Error

Flow:
1. User submits registration data (name, email, password)
2. API validates request format and forwards to Business Logic
3. Business Logic validates email uniqueness, hashes password, generates UUID
4. Data is saved to database
5. Success/error response returned to user

Key Points: Email must be unique, password is hashed before storage, validation at multiple layers.

---

### 4.2 Place Creation
sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Database
    User->>API: Create Place (title, location, description)
    API->>BusinessLogic: Validate and Process Request
    BusinessLogic->>Database: Store Place Data
    Database-->>BusinessLogic: Confirm Save
    BusinessLogic-->>API: Return Success/Failure
    API-->>User: Place Created Successfully/Error

Flow:
1. Authenticated user submits place details (title, description, price, coordinates)
2. API authenticates user and validates request
3. Business Logic validates data (positive price, valid coordinates), verifies owner exists
4. Place is saved with owner link
5.Success/error response with place details returned

Key Points: User must be authenticated, coordinates validated, owner ID extracted from authentication token.

---

### 4.3 Review Submission
sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Database
    User->>API: Submit Review (place_id, rating, comment)
    API->>BusinessLogic: Validate and Process Request
    BusinessLogic->>Database: Store Review Data
    Database-->>BusinessLogic: Confirm Save
    BusinessLogic-->>API: Return Success/Failure
    API-->>User: Review Submitted Successfully/Error

Flow:
1. Authenticated user submits review (place ID, rating, comment)
2. API authenticates and forwards to Business Logic
3. Business Logic validates: place exists, user not owner, rating in range (1-5), no duplicate review
4. Review is saved
5. Success/error response returned

Key Points: Users cannot review own places, one review per user per place, rating must be 1-5.

---

### 4.4 Fetching List of Places
sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Database
    User->>API: Request Places (filters: location, price, etc.)
    API->>BusinessLogic: Process Request & Apply Filters
    BusinessLogic->>Database: Fetch Matching Places
    Database-->>BusinessLogic: Return Places List
    BusinessLogic-->>API: Return Places Data
    API-->>User: Display List of Places

Flow:
1. User requests places with optional filters (price range, location, amenities)
2. API parses query parameters and forwards to Business Logic
3. Business Logic builds filtered query with pagination
4. Database returns matching places
5. Places converted to JSON and returned with pagination metadata

Key Points: Public endpoint (no authentication required), supports filtering and pagination, efficient database queries.

---

## 5. Conclusion

This documentation provides the architectural foundation for the HBnB Evolution application. The three-layer architecture ensures separation of concerns, maintainability, and scalability. The Business Logic Layer's well-defined entities and relationships form the core of the system, while the Facade pattern enables clean communication between layers.

Next Steps:
- Part 2: Implement Business Logic in Python
- Part 3: Implement Persistence Layer with database
- Part 4: Implement Presentation Layer (API endpoints)
- Part 5: Testing and deployment

---

Repository: holbertonschool-hbnb/part1  
Version: 1.0  
Last Updated: December 2025
