# Import necessary modules and functions
import app
import result

# Test cases for the web application

def test_index_route_renders_template():
    # Make a request to the index route
    response = app.client.get('/')
    
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Assert that the response contains the index.html template
    assert b'index.html' in response.data

def test_template_receives_correct_data():
    # Make a request to the index route
    response = app.client.get('/')
    
    # Assert that the dietlabels and healthlabels dictionaries are passed correctly to the template
    assert b'dietlabels' in response.data
    assert b'healthlabels' in response.data

def test_split_dict_function():
    # Create a sample dictionary
    sample_dict = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
    
    # Split the dictionary into two columns
    result = app.split_dict(sample_dict, 2)
    
    # Assert that the split_dict function splits the dictionary into multiple columns correctly
    assert result == ({'a': 1, 'b': 2, 'c': 3}, {'d': 4, 'e': 5})

def test_len_hl_len_ct_calculation():
    # Create sample values
    len_hl = 10
    len_ct = 5
    
    # Calculate the total length
    total_length = app.len_hl_len_ct_calculation(len_hl, len_ct)
    
    # Assert that the len_hl and len_ct variables are calculated correctly
    assert total_length == 15


# Test cases for the result module

def test_result_route_renders_template():
    # Make a request to the result route
    response = result.client.get('/result')
    
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Assert that the response contains the result.html template
    assert b'result.html' in response.data

def test_api_request_parameters():
    # Make a sample request to the API
    params = {
        'q': 'chicken',
        'diet': 'balanced',
        'health': 'vegan',
        'number': 5
    }
    response = result.api_request(params)
    
    # Assert that the API request is made with the correct parameters
    assert response['q'] == 'chicken'
    assert response['diet'] == 'balanced'
    assert response['health'] == 'vegan'
    assert response['number'] == 5

def test_lookup_function():
    # Create a sample recipe ID
    recipe_id = '12345'
    
    # Look up the recipe
    recipe = result.lookup(recipe_id)
    
    # Assert that the lookup function is called correctly
    assert recipe['id'] == '12345'

def test_recipes_list_passing():
    # Create a sample list of recipes
    recipes = [{'id': '12345', 'label': 'Recipe 1'}, {'id': '67890', 'label': 'Recipe 2'}]
    
    # Make a request to the result route
    response = result.client.get('/result')
    
    # Assert that the recipes_list is passed correctly to the template
    assert b'recipes' in response.data
    for recipe in recipes:
        assert recipe['label'].encode() in response.data

def test_readable_ingredients_generation():
    # Create a sample list of ingredients
    ingredients = ['Ingredient 1', 'Ingredient 2', 'Ingredient 3']
    
    # Generate the readable ingredients
    readable_ingredients = result.generate_readable_ingredients(ingredients)
    
    # Assert that the readable_ingredients variable is generated correctly
    assert 'Ingredient 1, Ingredient 2, Ingredient 3' == readable_ingredients

def test_saved_recipes_retrieval():
    # Create a sample list of saved recipes
    saved_recipes = [{'id': '12345', 'label': 'Recipe 1'}, {'id': '67890', 'label': 'Recipe 2'}]
    
    # Save the recipes in the session
    with result.client.session_transaction() as session:
        session['saved_recipes'] = saved_recipes
    
    # Make a request to the result route
    response = result.client.get('/result')
    
    # Assert that the saved recipes are retrieved correctly from the session
    assert b'saved_recipes' in response.data
    for recipe in saved_recipes:
        assert recipe['label'].encode() in response.data

def test_remove_route():
    # Create a sample recipe ID to remove
    recipe_id = '12345'
    
    # Save the recipe in the session
    with result.client.session_transaction() as session:
        session['saved_recipes'] = [{'id': '12345', 'label': 'Recipe 1'}, {'id': '67890', 'label': 'Recipe 2'}]
    
    # Make a request to the remove route
    response = result.client.post('/result/remove', data={'recipe_id': recipe_id})
    
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Assert that the recipe is removed from the session
    with result.client.session_transaction() as session:
        saved_recipes = session['saved_recipes']
        assert len(saved_recipes) == 1
        assert recipe_id not in [recipe['id'] for recipe in saved_recipes]
