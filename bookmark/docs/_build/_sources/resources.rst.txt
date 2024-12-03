.. _`Resources`:

Resources
=========
This section describes class and functions private to Bookmark. It is intended to document how the application works

User Class
----------
The User Class is designated for all users with authenticated accounts. Users create their account through
the sign-up page and provide First and Last name, email adderss and create a password. THe User class will
assign a userID when the user is created an added to the database.

Book Class
----------
The Book Class is designated for all books that are entered in the Bookmark database. Users will add booksto the database 
as they read more and add the books to their profile. Authors will add books to the databaase as they write more.
The Book Class will include the name of the book, the author, the ISBN number, the publication date, the cover art jpeg,
a description of the book provided by the user and a rating provided by the user when they add the book.

Post Class
----------
The Post Class is used to catalog al the poists created by Users. Users will create new posts that are
associated with books they are reading or have previously read. The Post class will inlude the User name, userID
the name of the book and its author and the text of their post. There are no current limits on the length of the post.

