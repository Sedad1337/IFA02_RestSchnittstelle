from crypt import methods
import uuid 

from flask import Flask, request, jsonify, abort


# initialize Flask server
app = Flask(__name__)

# create unique id for lists, users, entries
user_id_david = uuid.uuid4()
user_id_marko = uuid.uuid4()
user_id_kevin = uuid.uuid4()
todo_list_1_id = '376f4792-c8a2-48be-b0fe-e06a2236e757'
todo_list_2_id = '8ade3145-20db-4dce-8d8f-f003049fb529'
todo_list_3_id = '245c1c3a-68bd-44e6-b104-50761264ee70'
todo_1_id = uuid.uuid4()
todo_2_id = uuid.uuid4()
todo_3_id = uuid.uuid4()
todo_4_id = uuid.uuid4()

# define internal data structures with example data
user_list = [
    {'id': user_id_david, 'name': 'justin'},
    {'id': user_id_marko, 'name': 'Alvin'},
    {'id': user_id_kevin, 'name': 'Calvin'},
]
todo_lists = [
    {'id': todo_list_1_id, 'name': 'Einkaufsliste'},
    {'id': todo_list_2_id, 'name': 'Arbeit'},
    {'id': todo_list_3_id, 'name': 'Privat'},
]
todos = [
    {'id': todo_1_id, 'name': 'Milch', 'description': '', 'list': todo_list_1_id, 'user': user_id_david},
    {'id': todo_2_id, 'name': 'Hausaufgaben erledigen', 'description': '', 'list': todo_list_2_id, 'user': user_id_marko},
    {'id': todo_3_id, 'name': 'Küche putzen', 'description': '', 'list': todo_list_3_id, 'user': user_id_kevin},
    {'id': todo_3_id, 'name': 'Zucker', 'description': '', 'list': todo_list_1_id, 'user': user_id_kevin},
]

# add some headers to allow cross origin access to the API on this server, necessary for using preview in Swagger Editor!
@app.after_request
def apply_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# define endpoint for getting and deleting existing todo lists
@app.route('/todo-lists/<list_id>', methods=['GET', 'DELETE'])
def handle_list(list_id):
    # find todo list depending on given list id
    list_item = None
    for l in todo_lists:
        if l['id'] == list_id:
            list_item = l
            break
    # if the given list id is invalid, return status code 404
    if not list_item:
        abort(404)
    if request.method == 'GET':
        # find all todo entries for the todo list with the given id
        print('Returning todo list...')
        return jsonify([i for i in todos if i['list'] == list_id])
    elif request.method == 'DELETE':
        # delete list with given id
        print('Deleting todo list...')
        todo_lists.remove(list_item)
        return '', 200


# define endpoint for adding a new list
@app.route('/todo-lists', methods=['POST'])
def add_new_list():
    # make JSON from POST data (even if content type is not set correctly)
    new_list = request.get_json(force=True)
    print('Got new list to be added: {}'.format(new_list))
    # create id for new list, save it and return the list with id
    new_list['id'] = uuid.uuid4()
    todo_lists.append(new_list)
    return jsonify(new_list), 200


# define endpoint for getting all lists
@app.route('/todo-lists', methods=['GET'])
def get_all_lists():
    return jsonify(todo_lists)

#
@app.route('/todo-lists/<list_id>/entry/', methods=['POST'])
def add_new_entry():
    # make JSON from POST data (even if content type is not set correctly)
    new_entry = request.get_json(force=True)
    print('Got new Entry to be added: {}'.format(new_entry))
    # create id for a new Entry, save it and return the Entry with id
    new_entry['id'] = uuid.uuid4()
    todos.append(new_entry)
    return jsonify(new_entry), 200

#
@app.route('/todo-list/<list_id>/entry/<entry_id>', methods=['PUT', 'DELETE'])
def handle_entry(entry_id):
    if request.method == 'DELETE':
        # delete entry with given id
        print('Deleting entry...')
        user_list.remove(entry_id)
        return 200, 404

    elif request.method == 'PUT':
        todos.append(entry_id)
        return jsonify(entry_id), 200


@app.route('/user', methods=['GET', 'POST'])
def handle_user():
    if request.method == 'GET':
        # find all users
        print('Returning users...')
        return jsonify(user_list)

    elif request.method == 'POST':
        # make JSON from POST data (even if content type is not set correctly)
        new_user = request.get_json(force=True)
        print('Got new user to be added: {}'.format(new_user))
        # create id for new list, save it and return the list with id
        new_user['id'] = uuid.uuid4()
        todo_lists.append(new_user)
    return jsonify(new_user), 200

@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
     # delete list with given id
        print('Deleting user...')
        user_list.remove(user_id)
        return 200, 404

if __name__ == '__main__':
    # start Flask server
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
