import json
import dynamodb as db
import copy
import uuid


def t1():

    res = db.get_item("comments",
                      {
                          "comment_id": "984b90ff-0887-4291-afc4-7854bf452ac8"
                      })
    print("Result = \n", json.dumps(res, indent=4, default=str))


def t2():

    res = db.find_by_template("comments", {
        "email": "dff9@columbia.edu",
        "is_cat": "Yes"
    })
    print("Result = \n", json.dumps(res, indent=4, default=str))


def t3():
    table_name = "comments"
    # commenter = "dff9@columbia.edu"
    commenter = "fy2241@columbia.edu"
    response = "To cool for school"
    # res = db.add_response(table_name, "01cdb10e-6d9b-4b23-98bc-db062ae908ec", "dff9@columbia.edu",
    #                      response)
    res = db.add_response(table_name, "a78a7fde-73b9-47db-a348-e7476f952a1f", commenter,
                         response)
    print("t3 -- res = ", json.dumps(res, indent=3))


def t4():
    tag = 'Sports'
    res = db.find_by_tag(tag)
    print("Comments with tag 'science' = \n", json.dumps(res, indent=3, default=str))


def t5():
    print("Do a projection ...\n")
    res = db.do_a_scan("comments",
                       None, None, "#c, comment_id", {"#c": "comment"})
    print("Result = \n", json.dumps(res, indent=4, default=str))


def t6():

    comment_id = "a7f5479c-3d71-44a0-8ec7-d201d2d23ebb"
    original_comment = db.get_item("comments", {"comment_id": comment_id})
    original_version_id = original_comment["version_id"]

    new_comment = copy.deepcopy(original_comment)

    try:
        res = db.write_comment_if_not_changed(new_comment, original_version_id)
        print("First write returned: ", res)
    except Exception as e:
        print("First write exception = ", str(e))

    try:
        res = db.write_comment_if_not_changed(new_comment, original_version_id)
        print("Second write returned: ", res)
    except Exception as e:
        print("Second write exception = ", str(e))


def t7():
    email = "cz2382@columbia.edu"
    comment = "Hello!"
    tags = []
    db.add_comment(email, comment, tags)
    res = db.find_by_template("comments", {
        "email": email
    })
    print("Result = \n", json.dumps(res, indent=4, default=str))


def t8():
    res = db.do_a_scan("comments")
    print("Result = \n", json.dumps(res, indent=4, default=str))

# t1()
# t2()
# t3()
# t4()
# t5()
t6()
# t7()
# t8()
