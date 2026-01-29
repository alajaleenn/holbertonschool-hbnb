# HBnB Database Entity-Relationship Diagram - Task 10

## ER Diagram (Mermaid.js)

```mermaid
erDiagram
    users {
        VARCHAR(36) id PK
        VARCHAR(50) first_name
        VARCHAR(50) last_name
        VARCHAR(120) email UK
        VARCHAR(255) password
        BOOLEAN is_admin
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }
    
    places {
        VARCHAR(36) id PK
        VARCHAR(100) title
        TEXT description
        DECIMAL(10,2) price
        FLOAT latitude
        FLOAT longitude
        VARCHAR(36) owner_id FK
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }
    
    amenities {
        VARCHAR(36) id PK
        VARCHAR(50) name UK
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }
    
    reviews {
        VARCHAR(36) id PK
        TEXT text
        INTEGER rating
        VARCHAR(36) place_id FK
        VARCHAR(36) user_id FK
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }
    
    place_amenity {
        VARCHAR(36) place_id PK,FK
        VARCHAR(36) amenity_id PK,FK
        TIMESTAMP created_at
    }
    
    users ||--o{ places : "owns"
    users ||--o{ reviews : "writes"
    places ||--o{ reviews : "has"
    places }o--o{ amenities : "has"
