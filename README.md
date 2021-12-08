# aws-dynamodb
DynamoDB table "comments"
#### API Paths
> /comments (GET, POST)
>
>/comments/<comment_id> (GET, POST, PUT)
>
#### Request message examples for POST
Add new comment
> /comments (POST)
> 
    {
        "email": "xxxxxx@columbia.edu",
        "comment": "This is a must try!!!",
        "recipe": "Mimosa"
    }
    
Add new response to an existing comment
> /comments/<comment_id> (POST)
>
    {
        "email": "xxxxxx@columbia.edu",
        "response": "Agreed"
    }

Modify comment
> /comments/<comment_id> (PUT)
>
    {
        "comment": "New comment"
    }
#### Other examples
Find comments for a specific recipe
> /comments?recipe=Mimosa (GET)