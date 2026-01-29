cat > README_SQL.md << 'EOF'
# HBnB Database SQL Scripts

This directory contains SQL scripts for creating and populating the HBnB database.

## Files

1. **schema.sql** - Creates the complete database schema
2. **data.sql** - Inserts initial data (admin user, amenities, sample data)
3. **queries.sql** - Sample CRUD operations for testing

## Database Schema

### Tables
1. **users** - User accounts (admin and regular users)
2. **places** - Property listings
3. **amenities** - Features available at places
4. **reviews** - User reviews for places
5. **place_amenity** - Many-to-many relationship between places and amenities

### Relationships
- One **User** can own many **Places** (1:N)
- One **User** can write many **Reviews** (1:N)
- One **Place** can have many **Reviews** (1:N)
- **Places** and **Amenities** have a many-to-many relationship (N:M)

## How to Use

### 1. Create the database schema
```bash
mysql -u username -p < schema.sql
