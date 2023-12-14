# Table of Contents
1. [Installation Instructions](#installation)
2. [R1 - Identification of the problem you are trying to solve by building this particular app](#rone)
3. [R2 - Why is it a problem that needs solving?](#rtwo)
4. [R3 - Why have you chosen this database system. What are the drawbacks compared to others?](#rthree)
5. [R4 - Identify and discuss the key functionalities and benefits of an ORM](#rfour)
6. [R5 - Document all endpoints for your API](#rfive)
7. [R6 - An ERD for your app](#rsix)
8. [R7 - Detail any third party services that your app will use](#rseven)
9. [R8 - Describe your projects models in terms of the relationships they have with each other](#reight)
10. [R9 - Discuss the database relations to be implemented in your application](#rnine)
11. [R10 - Describe the way tasks are allocated and tracked in your project <a name='R10'></a>](#rten)

# Installation Instructions <a name="installation"></a> 


# R1 - Identification of the problem you are trying to solve by building this particular app <a name="rone"></a>
This is an Online Clothing Store Catalogue, which will help users add data and retrieve data about there products(clothing items). 

The main goal for developing the Online Clothing Store Catalogue API is to help streamline and ehance functionality, accessibility and integration of clothing store catalogues. The API aims to solve some key problems:
1. Integration complexity: This API will simplify the integration process of Online Clothing Stores for multiple platforms including, websites and mobile platforms.
2. Improve User Experience : Provide real time access to product information such as descriptions, prices, reviews etc. Ensuring more consistent shopping for the Store users.
3. Scalability: The API offers a variety of features but is an adaptable and scalable solution being easily updated and able to add new features to this base product as your store grows, without disrupting the core system.
4. Marketing and sales: The API will be an alternative option to using costly third party applications. This App will give the user more control and flexibility to manage their own products for their own websites.

# R2 - Why is it a problem that needs solving? <a name="rtwo"></a>
The problems Listed above are significant issues when it comes to running a online clothing store. These problems can slow growth reduce capital and diminish user experience. 

- Integration complexity can slow down expansion and growth of a store across multiple platforms, restricting customer engagement.
- Outdated product information can lead to customer mistrust and dissatisfaction, which has a negative impact to your brand.
- New business owners need a flexible, easy to use and cost effective way to manage there product information. With a small amount of knowledge in IT a user can simply use this API for there store. Reducing there capital and avoiding using costly third party services.

# R3 - Why have you chosen this database system. What are the drawbacks compared to others? <a name="rthree"></a>
I have chosen to use PostgreSQL as my Database for my project. PostgreSQL is a very popular relational database system that offers multiple advantages making it a great choice for my application. Some of the advantages to using PostgreSQL for my application are:

- Scalability: PostgreSQL offers great flexibility and scalability options allowing for handling of small or large data volumes and user requests which is essential for a Clothing store catalog application. Being able to handle larger data loads as the application grows.
- Reliability: PostgreSQL is known for its stability and reliability. It ensures data integrity and consitant performance which is essential for my application.
- Security: PostgreSQL has many security features including but not limited to SSL support and dataencryption support. This is essential when dealing with customer information and sensitive data.

Some Draw backs of PostgreSQL compared to MySQL:

- MySQL is the better option for using read only commands than PostgreSQL.
- PostgreSQL is more optimized for UNIX -based systems where as MySQL performs well cross-platform.
- PostgreSQL is growing in popularity for more complex uses but MySQL is more used for its speed and reliability.
- PostgreSQL offers more features then MySQL but the disadvantage to this is that MySQL will perform faster processing then PostgreSQL.
- Both MySQL and PostgreSQL are Relational Database Management Systems but PostgreSQL actually a Object-Relational Database Management System this supports the use of Object Relational Mapping, and depending on your application can be positive or negative.

sources : https://www.integrate.io/blog/postgresql-vs-mysql-which-one-is-better-for-your-use-case/#:~:text=PostgreSQL%20is%20preferred%20for%20managing,comes%20to%20read%2Donly%20queries.
# R4 - Identify and discuss the key functionalities and benefits of an ORM <a name="rfour"></a>
An ORM means Object-Raltional mapping. This is used for implicationg OOP or Object Orientated Programming code with Database systems to help simplify relational databases. Using and ORM such as SQLAlchemy with Flask and PostgreSQL allows you to easily import OOP into your Database application while still haveing the functionality of SQL commands and db commands. Some key features and benefits of an ORM such as SQLAlchemy are:

- Allows us to work with Python objects instead of raw SQL commands making our code cleaner and more simplified. eg. Using SQLAlchemy you can define database models tables and data as python classes and objects.
- SQLAlchemy works seamlessly with multiple database systems. It is not reliant on the specific database back end and will work independently meaning you can switch databases using the same SQLAlchemy code.
- SQLALchemy has epic database operation performance and works seamlessly with database querying such as SELECT, INSERT, UPDATE and delete simplifying these CRUD operations into python objects Reduces compexity for developers and makes for better productivity.

There are several benefits to using SQLAlchemy and I have chosen to use it for my application due to its flexibility simplicity and great relation to Python OOP features.

sources: https://vegibit.com/what-is-the-role-of-sqlalchemy-in-python-database-interactions/#advantages-of-using-sqlalchemy

# R5 - Document all endpoints for your API <a name="rfive"></a>
## User Endpoints
### /users/ - GET 
This endpoint allows a user to access all users in the database. This endpoint uses SQL User.query.all() to get all users and serializes them to be returned and Displayed in JSON format. It excludes sensitive information for security purposes.
- HTTP VERBS: GET
- Required Data: N/A
- Expected Response: JSON object containing all users and there information excluding passwords
- Authentication: JWT token required

![Shows users endpoint in insomnia](/docs/all_users.png)

### /users/register - POST
This endpoint is a POST/Create, the endpoint is used for registering as a new user in the database. The user can input the required fields in insomnia/postman in JSON format and register as long as the email address is valid and not already in use. It uses TRY/EXCEPT handling for Integrity errors to ensure this. The register endpoint also uses bcrypt to hash the users password for security. 
- HTTP VERBS: POST
- Required Data: name, email, and password are required to register.
- Expected Response: JSON response showing the user fields with new users details.
- Authentication: No authentication is required to register.

![users endpoint showing registration](/docs/register.png)

### /users/login - POST
This endpoint is used to login as the user, logging in will create a JWT token for the user and depending on there authorisation will allow them to certain features of the API. The endpoint users SQL query select to first select the user where it meets the conditions that email and password match. If both email and password match the it will return the JWT token that that user can use to access certain features. if the details do not match the code will send them a error showing that the email or password are invalid.
- HTTP VERBS: POST
- Required Data: email and password are required to login.
- Expected Response: JSON response showing the user fields with new users details and a JWT token.
- Authentication: No authentication is required to login but login will respond with a JWT token to use on required fields.

![users endpoint showing login system](/docs/login.png)

### /users/{id} - DELETE
This endpoint allows admin to delete a user from the database. Users can also delete themselves. Using JWT tokens we can confirm the identity of the user to see what authorisation they have. using a select query to select the inputted id and fetching it as a scalar if the user is then authorized it will db.session.delete(user) and commit the delete to the database.
- HTTP VERBS: DELETE
- Required Data: An Valid ID must be specified in the route to delete the user.
- Expected Response: JSON message showing successful deletion.
- Authentication: JWT required(bearer token), User must be the owner of the ID or the admin to delete the user.

![users endpoint showing deleting a user successfully](/docs/delete_user.png)

### UPDATE
I decided to leave out update for users for security purposes. Users can Delete and re register if needed. After thinking on this for the scope of my Application I think for now leaving out update for users is the best situation but a function that can be implimented in the future.

## Categories Endpoints
### /categories/ - GET
This endpoint retrieves all categories and displays them in a JSON format, it uses query.all() to retrive all users then serialises the categories schema to display them in JSON format. 
- HTTP VERBS: GET
- Required Data: No data required just endpoint.
- Expected Response: JSON response showing all categories in the database.
- Authentication: JWT token(bearer token required).

![categories endpoint showing all categories](/docs/all_categories.png)

### /categories/{id} - GET
This endpoint uses a select and scalar retrieving 1 selected category by its id from the database and returning it as a JSON object. All details of categories can be displayed as there is no security risk.
- HTTP VERBS: GET
- Required Data: Specific ID for Category in the endpoint.
- Expected Response: JSON response showing the category fields.
- Authentication: JWT required(Bearer token).

![categories endpoint showing one selected category](/docs/one_category.png)

### /categories/ - POST
This endpoint allows for the creation of a new category. Any user can can create a new category as long as the name of category doesnt already exist. The schema checks the database for same names and will throw an error if category exists if not it will accept the name and description add it to the database and return the new category as a JSON object.
- HTTP VERBS: POST
- Required Data: name and description are required to create a new category.
- Expected Response: JSON response showing the details of the new category if successful.
- Authentication: JWT required(bearer token) JWT holder must be ADMIN.

![categories endpoint that creates a new category](/docs/create_category.png)

### /categories/{id} - PUT/PATCH
This enpoint allows and admin to make updates to to the categories. using the category id and db.select and scalar we can get the specific category and cross check with the schema to make updates. Either name or description or both can be updated by the admin. must make sure you use a bearer token of the admin to make changes.
- HTTP VERBS: PUT/PATCH
- Required Data: Must be specific with ID in endpoint. Either name or description or both to be updated.
- Expected Response: JSON response showing the updated information it should match your input.
- Authentication: JWT token(bearer token), Must be an ADMIN.

![categories endpoint showing update method](/docs/update_category.png)

### /categories/{id} - DELETE
This endpoint allows an admin to delete a category from the database. Must be selective with the category id to specify which category to delete. The endpoint uses SQL select to select the id from the categories table and returns with a scalar, It then uses db session command to delete the matching id and details from the database.
- HTTP VERBS: DELETE
- Required Data: ID of category must be specified in route.
- Expected Response: JSON response showing a message for successful deletion.
- Authentication: JWT token and Admin required.

![categories endpoint that deletes category](/docs/delete_category.png)

## Products Endpoints

### /products/ - GET
This endpoint allows a user to get a lst of all products and the information. It uses SQL alchemy query.all() to select all products in the db and return them as a JSON object in insomnia.
- HTTP VERBS: GET
- Required Data: No data required just route.
- Expected Response: JSON response showing the details of all products also the reviews attached to them.
- Authentication: JWT required(bearer token).

![products endpoint that shows all products in DB](/docs/all_products.png)

The products also nests in the reviews for each product and lists them

![reviews nested](/docs/products&reviews.png)

### /products/{id} - GET
This endpoint allows the user to retrieve a specific product by specifying the products ID. users select statment to select the matching ID and returns it with scalar to dump the schema as a JSON object.
- HTTP VERBS: GET
- Required Data: Specific product ID required in route.
- Expected Response: JSON response showing the product details that match the ID.
- Authentication: JWT required (bearer token).

![products endpoint that shows a specific product](/docs/one_product.png)

### /products/ - POST
This endpoint allows the logged in user(must use JWT token as bearer ) to create a new product, user can specify all the product details in JSON and the database will update. If the name of the new product matches an existing product the route will throw an error.
- HTTP VERBS: POST
- Required Data: name, description, price, color, category_id - all of these are required to create a new product.
- Expected Response: JSON response showing the new details input along with and ID for the product.
- Authentication: JWT token(bearer token).

![products endpoint that creates a new product](/docs/Create_product.png)

### /products/{id} - PUT/PATCH
This endpoint updates a product if the user is an admin or the creator of the product. it used .get to retieve the information and changes it to the users input then displays the updated record.
- HTTP VERBS: PUT/PATCH
- Required Data: ID for product wanting to update specified in route, Any fields you want to update will be required.
- Expected Response: JSON response with the updated information displayed.
- Authentication: JWT required(bearer token), must be an admin or the original creater of the product to make an update.

![products endpoint that updates a product](/docs/update_product.png)

### /products/{id} - DELETE
This endpoint allows an admin to delete a product from the database. by specifying the id of the product in the route it will use a SQL stmt deb.select and scalar to retrive the product and deletes it from the database with db.delete.
- HTTP VERBS: DELETE
- Required Data: ID for product you want to delete must be specified in route.
- Expected Response: JSON response message saying deletion was successful.
- Authentication: JWT required(bearer token), must be an ADMIN or the original creator of the product to delete it.

![products endpoint that deletes a product from the database](/docs/delete_product.png)

## Review Endpoints
### /reviews/ - GET
This endpoint gets a list of all reviews in the system and shows who created them and what product id they are created for. It retrieves them from database using query.all() and returns them as a JSON object.
- HTTP VERBS: GET
- Required Data: no data required just the route.
- Expected Response: JSON response showing all the reviews and their fields in the database.
- Authentication: JWT required(bearer token).

![reviews endpoint that shows all reviews in the system](/docs/all_reviews.png)

### /reviews/{id} - GET
This endpoint retrieves a specific review. specifying the review ID it will use select stmt and sclar to find and retrieve the review and return it in JSON format. 
- HTTP VERBS: GET
- Required Data: ID for review must be specified in the route.
- Expected Response: JSON response showing the matching ID's Review .
- Authentication: JWT required(bearer token).

![gets one review](/docs/one_review.png)

### /reviews/ - POST
This endpoint creates a new review on a product it can specify a title a message and a product id to select. it checks if reviews are specific and if product exists to leave reviews on.
- HTTP VERBS: POST
- Required Data: Must provide a title, message and product id for the review you want to create and for what product.
- Expected Response: JSON response showing the new review details matching your input.
- Authentication: JWT required(bearer token).

![enpoint that creates a review](/docs/new_review.png)

### /reviews/{id} - PUT/PATCH
This endpoint allows the admin or owner of the review to update the title or message of the review. So JWT is required to check the authorization function. using the id it selects the review to be updatd with db.select and filters by the ID, If all tests pass it will return the successfully updated review info.
- HTTP VERBS: PUT/PATCH
- Required Data: Valid review ID must be included in route, title and or message or both what you want to update.
- Expected Response: JSON response showing the updated information of the review.
- Authentication: JWT required(bearer token), must also be an admin or the original creator of the review.

![enpoint updates specific review](/docs/update_review.png)

### /reviews/{id} - DELETE
This endpoint deletes a review from the system. it uses db.select to select the specific ID and checks for authorisation. When it is found it will delete from the DB and show a confirmation message. IF not authorised it will throw an error.
- HTTP VERBS: DELETE
- Required Data: Must specify the id or the review you wish to delete.
- Expected Response: JSON response showing message that deletion was successful.
- Authentication: JWT required(bearer token), Must be admin or the original creator of the review to delete.

![enpoint that deletes a review](/docs/success_delete_review.png)
![failed delete](/docs/failed_delete_review.png)
# R6 - An ERD for your app <a name="rsix"></a>
This outlines the ERD for my application. My application uses 4 models that have different relationships with each other. It uses crows foot notation to show the relationships between my entities in the diagram. 
![ERD for Webserver API](/docs/ERD.png)

# R7 - Detail any third party services that your app will use <a name="rseven"></a>

### Bcrypt
Flask Bcrypt is and extension of the Python Framework Flask. It is used for password hashing and verification, It provides a way to hash the passwords before they are stored in the database for security.
### JWT-Extended
Flask-JWT-Extended is an extension of flask that implements JSON Web Tokens(JWT) for authenticating users and autorization on flask applications. With this extension you can create and retrieve JWT tokens and verify them which can help us secure the data.
### marshmallow
Marshmallow is what allows us to use object serialization in our Flask application. such as serialzation of objects, dictionaries and mainly JSON. It allows us to define schemas for validating serialized data and provides a simple way to convert complex data structures into native python data types and back.
### psycopg2-binary
Psycopg2 binary is a python library used to interact with the database(PostgreSQL) from the python application. Psycopg2 binary is essentially a database adapter that allows the communication between our python program and the database.
### SQLAlchemy
SQLAlchemy is a python SQL toolkit and Object-Relational Mapping (ORM) library. It uses a high level interface to interact with relational databases such as PostgreSQL through python. 
It allows us to apply Object Orientated Programming(OOP) to the database and allows us to use database and SQL commands in a more robust manner.

# R8 - Describe your projects models in terms of the relationships they have with each other <a name="reight"></a>
My project consists of four models representing the 4 tables in the database.
### User Model
1. Relationship with Products: One-to-many
    - A user can have many products related to themselves. This is established by the products products db.relationship in the User model.
2. Relationship with Review: One-to-many
    - A user can write as many reviews as they like. This is established by the reviews db.relationship in the User model.
### Product Model
1. Relationship with User: Many-to-one
    - Multiple products can be associated with one user. This is established by the user db.relationship in the Product model.
2. Relationship with Category: Many-to-one
    - Multiple products can belong to one category(T-shirt, Hoodie, Sweater - can all be associated with "Tops" category). This is established by the category db.relationship in the Product model.
3. Relationship with Review: One-to-many
    - A product can have multiple reviews attached to it. This is established through the review db.relationship in the Product model.
### Category Model
1. Relationship with Product: One-to-many
    - A category can have multiple products associated with it. This is established through the product db.relationship in the Category model.
### Review Model
1. Relationship to User: Many-to-one
    - Multiple reviews can be associated with a single user. This is established through the user db.relationship in the Review model.
2. Relationship to Product: Many-to-one
    - Multiple reviews can be attached to one product. This is established through the product db.relationship in the Review model.


# R9 - Discuss the database relations to be implemented in your application <a name="rnine"></a>
The database relations of my application to be implemented consist of four main tables in the database some relating to others. The following relations are linked by using Foreign keys and database relations. Here is a breakdown of what relationships are within the database and what time of relationship they have with each other:

1. Users:
    - Users can be with multiple products and reviews, both products and reviews hold the user_id foreign key to assosicate their relationship with the user table.
    - The Database Relation is a One-to-many with products and One-to_many with reviews.
2. Products:
    - Each product can belong to a single user (the creator of the product).
    - Each product is categorized under a specific category.
    - Each product can have multiple reviews.
    - The database relations are Many-to-one with Users, Many-to-one with Categories and One-to-many with Reviews.
    - Products holds Foreign Keys for category_id and user_id, and db.reltionship is held in each table to connect the relationship
3. Categories:
    - A category can contain multiple products.
    - The database relation is One-to-many with Products.
4. Reviews:
    - Each review is connected to a single user(The creator of the review).
    - Each review is associated with a specific product.
    - Database relation is Many-to-one with Users and Many-to-one with Products.
    - Reviews holds a ForeignKey for both user_id abd product_id. and db.reltionship is held in each table to connect the relationship.


# R10 - Describe the way tasks are allocated and tracked in your project <a name="rten"></a>
For my project I followed an agile methodology. Before Starting my code I carefully planned my ERD and broke my project down into points of documentation/models/blueprints/endpoints. I used trello to track my progress Throughout the development of my project. 

I started by listing out cards on trello for the initial stages of my project.
![Trello board](/docs/Trello_start.png)

I broke it into more simple components and tackled each component as a goal. It was broken up into tasks to do, tasks in progress, and tasks done.

Throught the tried to check my trello board each day and change labels to keep my progess up to date.
![trello board](/docs/trello7:12.png)

I built my file system and outline first, after completing this I tackled each model 1 by 1 for example I would create User model then user schema then user blueprint. I did in this order keeping it simple as to what I was doing as to not get confused between blueprints and models.

![trello board](/docs/trello8:12.png)
![trello board](/docs/trello12:12_1.png)
![trello board](/docs/trello12:12_2.png)

I tried to follow my approach as much as possible and keep the tasks to smaller blocks that were related. I planned my application throughly and throught through the endpoints, relationships and blueprints carefully before starting my app. 

Next time I hope to write more detail in my planning process. 

Here is the final screenshot of everything completed.
![trello board](/docs/completed_trello.png)