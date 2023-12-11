# R1 - Identification of the problem you are trying to solve by building this particular app
This is an Online Clothing Store Catalogue, which will help users add data and retrieve data about there products(clothing items). 

The main goal for developing the Online Clothing Store Catalogue API is to help streamline and ehance functionality, accessibility and integration of clothing store catalogues. The API aims to solve some key problems:
1. Integration complexity: This API will simplify the integration process of Online Clothing Stores for multiple platforms including, websites and mobile platforms.
2. Improve User Experience : Provide real time access to product information such as descriptions, prices, reviews etc. Ensuring more consistent shopping for the Store users.
3. Scalability: The API offers a variety of features but is an adaptable and scalable solution being easily updated and able to add new features to this base product as your store grows, without disrupting the core system.
4. Marketing and sales: The API will be an alternative option to using costly third party applications. This App will give the user more control and flexibility to manage their own products for their own websites.

# R2 - Why is it a problem that needs solving?
The problems Listed above are significant issues when it comes to running a online clothing store. These problems can slow growth reduce capital and diminish user experience. 

- Integration complexity can slow down expansion and growth of a store across multiple platforms, restricting customer engagement.
- Outdated product information can lead to customer mistrust and dissatisfaction, which has a negative impact to your brand.
- New business owners need a flexible, easy to use and cost effective way to manage there product information. With a small amount of knowledge in IT a user can simply use this API for there store. Reducing there capital and avoiding using costly third party services.

# R3 - Why have you chosen this database system. What are the drawbacks compared to others?
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
# R4 Identify and discuss the key functionalities and benefits of an ORM
An ORM means Object-Raltional mapping. This is used for implicationg OOP or Object Orientated Programming code with Database systems to help simplify relational databases. Using and ORM such as SQLAlchemy with Flask and PostgreSQL allows you to easily import OOP into your Database application while still haveing the functionality of SQL commands and db commands. Some key features and benefits of an ORM such as SQLAlchemy are:

- Allows us to work with Python objects instead of raw SQL commands making our code cleaner and more simplified. eg. Using SQLAlchemy you can define database models tables and data as python classes and objects.
- SQLAlchemy works seamlessly with multiple database systems. It is not reliant on the specific database back end and will work independently meaning you can switch databases using the same SQLAlchemy code.
- SQLALchemy has epic database operation performance and works seamlessly with database querying such as SELECT, INSERT, UPDATE and delete simplifying these CRUD operations into python objects Reduces compexity for developers and makes for better productivity.

There are several benefits to using SQLAlchemy and I have chosen to use it for my application due to its flexibility simplicity and great relation to Python OOP features.

sources: https://vegibit.com/what-is-the-role-of-sqlalchemy-in-python-database-interactions/#advantages-of-using-sqlalchemy

# R5 Document all endpoints for your API
## User Endpoints
### /users/ - GET 
This endpoint allows a user to access all users in the database. This endpoint uses SQL User.query.all() to get all users and serializes them to be returned and Displayed in JSON format. It excludes sensitive information for security purposes.

![Shows users endpoint in insomnia](/docs/all_users.png)

### /users/register - POST
This endpoint is a POST/Create, the endpoint is used for registering as a new user in the database. The user can input the required fields in insomnia/postman in JSON format and register as long as the email address is valid and not already in use. It uses TRY/EXCEPT handling for Integrity errors to ensure this. The register endpoint also uses bcrypt to hash the users password for security. 

![users endpoint showing registration](/docs/register.png)

### /users/login - POST
This endpoint is used to login as the user, logging in will create a JWT token for the user and depending on there authorisation will allow them to certain features of the API. The endpoint users SQL query select to first select the user where it meets the conditions that email and password match. If both email and password match the it will return the JWT token that that user can use to access certain features. if the details do not match the code will send them a error showing that the email or password are invalid.

![users endpoint showing login system](/docs/login.png)

### /users/{id} - DELETE
This endpoint allows admin to delete a user from the database. Users can also delete themselves. Using JWT tokens we can confirm the identity of the user to see what authorisation they have. using a select query to select the inputted id and fetching it as a scalar if the user is then authorized it will db.session.delete(user) and commit the delete to the database.

![users endpoint showing deleting a user successfully](/docs/delete_user.png)

### UPDATE
I decided to leave out update for users for security purposes. Users can Delete and re register if needed. After thinking on this for the scope of my Application I think for now leaving out update for users is the best situation but a function that can be implimented in the future.

## Categories Endpoints
### /categories/ - GET
This endpoint retrieves all categories and displays them in a JSON format, it uses query.all() to retrive all users then serialises the categories schema to display them in JSON format. 

![categories endpoint showing all categories](/docs/all_categories.png)

### /categories/{id} - GET
This endpoint uses a select and scalar retrieving 1 selected category by its id from the database and returning it as a JSON object. All details of categories can be displayed as there is no security risk.

![categories endpoint showing one selected category](/docs/one_category.png)

### /categories/ - POST
This endpoint allows for the creation of a new category. Any user can can create a new category as long as the name of category doesnt already exist. The schema checks the database for same names and will throw an error if category exists if not it will accept the name and description add it to the database and return the new category as a JSON object.

![categories endpoint that creates a new category](/docs/create_category.png)

### /categories/{id} - PUT/PATCH
This enpoint allows and admin to make updates to to the categories. using the category id and db.select and scalar we can get the specific category and cross check with the schema to make updates. Either name or description or both can be updated by the admin. must make sure you use a bearer token of the admin to make changes.

![categories endpoint showing update method](/docs/update_category.png)

### /categories/{id} - DELETE
This endpoint allows an admin to delete a category from the database. Must be selective with the category id to specify which category to delete. The endpoint uses SQL select to select the id from the categories table and returns with a scalar, It then uses db session command to delete the matching id and details from the database.

![categories endpoint that deletes category](/docs/delete_category.png)

## Products Endpoints

### /products/ - GET
This endpoint allows a user to get a lst of all products and the information. It uses SQL alchemy query.all() to select all products in the db and return them as a JSON object in insomnia.

![products endpoint that shows all products in DB](/docs/all_products.png)

### /products/{id} - GET
This endpoint allows the user to retrieve a specific product by specifying the products ID. users select statment to select the matching ID and returns it with scalar to dump the schema as a JSON object.

![products endpoint that shows a specific product](/docs/one_product.png)

### /products/ - POST
This endpoint allows the logged in user(must use JWT token as bearer ) to create a new product, user can specify all the product details in JSON and the database will update. If the name of the new product matches an existing product the route will throw an error.

![products endpoint that creates a new product](/docs/Create_product.png)

# R6 An ERD for your app

# R7 Detail any third party services that your app will use

# R8 Describe your projects models in terms of the relationships they have with each other

# R9 Discuss the database relations to be implemented in your application

# R10 Describe the way tasks are allocated and tracked in your project