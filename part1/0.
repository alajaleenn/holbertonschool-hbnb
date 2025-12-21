classDiagram
    class PresentationLayer {
        <<Interface>>
        +ServiceAPI
        +handleRequests()
    }

    class HBnBFacade {
        <<Facade>>
        +createUser()
        +createPlace()
        +createReview()
        +getUser()
    }

    class BusinessLogicLayer {
        +User
        +Place
        +Review
        +Amenity
        +processLogic()
    }

    class PersistenceLayer {
        +DatabaseAccess
        +saveData()
        +retrieveData()
    }

    PresentationLayer --> HBnBFacade : uses
    HBnBFacade --> BusinessLogicLayer : coordinates
    BusinessLogicLayer --> PersistenceLayer : CRUD operations
