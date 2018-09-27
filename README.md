# EmojiChecker-Backend

## Dev Environment Setup
1. [Install Pipenv](https://pipenv.readthedocs.io/en/latest/)
2. >git clone https://github.com/ptstory/EmojiChecker-Backend.git
3. >cd EmojiChecker-Backend
4. Install dependencies 
    >pipenv install
5. Activate environment
    >pipenv shell 
6. Make our migrations
    >python manage.py makemigrations api
7. Run migrations
    >python manage.py migrate
8. Run test server 
    >python manage.py runserver
   

[View in action](http://ec2-184-72-136-95.compute-1.amazonaws.com:8080/auth/)

## Running tests
>python manage.py test


## Additional notes
- The developer environment is set to use sqlite for the database, even though we are using MySQL for production. Sqlite should be perfectly fine for development and requires zero configuration to get going.
- Certain settings, like the database and secret key are overridden in a production specific settings file. This will obviously not be committed to github.
## Resources 

[How to send an SMS using AWS](https://docs.aws.amazon.com/sns/latest/dg/sms_publish-to-phone.html)

[Python-Django](https://docs.djangoproject.com/en/2.1/)

[Django-Rest-Framework](http://www.django-rest-framework.org/)


