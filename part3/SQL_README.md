# Create README
cat > SQL_README.md << 'EOF'
# SQL Scripts for HBnB Database - Task 9

## Files
1. **schema.sql** - Creates all database tables with relationships
2. **data.sql** - Inserts initial data including admin user and amenities
3. **queries.sql** - Sample CRUD operations for testing

## Database Schema
- **users** - User accounts (admin and regular)
- **places** - Property listings with location data
- **amenities** - Features available at places
- **reviews** - User reviews with ratings
- **place_amenity** - Many-to-many relationship table

## Initial Data
- Admin: admin@hbnb.com
- User: john@example.com
- 10 amenities (WiFi, Pool, Parking, etc.)
- 3 sample places with reviews

## How to Use
Run in sequence:
```bash
mysql -u username -p < schema.sql
mysql -u username -p < data.sql
mysql -u username -p < queries.sql
