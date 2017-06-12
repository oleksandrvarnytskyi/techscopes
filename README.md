# techscopes
Web-based django application with custom user model(custom fields: birthday, country, city).
Each user need to be able to sign-up/sign-in via email/password. (also sign-out)
After sign-up user will get an confirmation email with verification code(or link, or both).
Only after verify email he can sign in to the website.
Website must be protected from anonymous users and be available only for logged users.
On the main page:
    - show all list Posts(e.g. title/body/image etc) with pagination. That list also need to have sorting form. (Country, city, search by keyword)
    - below each post user see number of the likes and the "like" button which add +1 like. User can like post only once, then it marked as liked, but he can to delete his like, and like again and so on. (Reference to social network likes.)
    - User can go to a single post page and see the post details and comments to the post also with pagination.
    
