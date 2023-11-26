# Functionality Testing

Details of manual testing of the functions of each feature of the website. Chrome DevTools was used to test the website on different screen sizes.

| Test Label | Test Action | Expected Outcome | Test Outcome |
|----------|-----------|----------------|------------|
| Navigation links. | Click all links in navigation menu on each page. | Each link leads to expected page from any page. | PASS |
| Navigation menu responsiveness | Resize the screen below and above 768px wide. | Navigation menu collapses into a toggler on screens lower than 768px wide and expands above 768px. | PASS |
| Hero section content | View hero section logged in and not logged in, and click button. | When logged in text displayed encourages user to browse recipes, button leads to browse page. When not logged in text displayed encourages user to create an account, button leads to sign up page. | PASS |
| Most liked recipes section | View most liked recipes section. | Top three most liked recipes are displayed in decending order of number of likes. | PASS |
| Most liked recipes cards | Click most liked recipe card | Full recipe details are displayed.  | PASS |
| Browse recipes list | View browse page | Recipe cards are displayed | PASS |
| Saved recipes list | View browse page as a logged in user with saved recipes | Recipe cards are displayed in reverse order of date saved | PASS |
| My recipes list | View my recipes page as a logged in user with created recipes | Recipe cards are displayed in reverse order of date created | PASS |
| Pagination | View all list views with more than 12 recipes displayed | 12 recipes are displayed per page with page links below | PASS |
| Recipe cards as links | Click recipe cards | Directed to full recipe details | PASS |
| Recipe form required fields | Click submit button on create recipe form before entering a value for each field | Empty fields for title, cooking time, serves, ingredients and method raise validation error and form cannot be submitted | PASS |
| Submit recipe for publication | Submit a recipe with all required inputs and 'Make public' checkbox checked | Successful form submission, publish_request model instance set to 'True', approval_status model instance set to 'pending approval' and recipe object added to database. User redirected to 'my recipes' page and message informs user the recipe was successfully submitted and awaiting approval. | PASS |
| Submit recipe not for publication | Submit a recipe with all required inputs and 'Make public' checkbox not checked | Successful form submission, publish_request model instance set to 'False', approval_status model instance set to 'unpublished' and recipe object added to database. User redirected to 'my recipes' page and message informs user the recipe was saved. | PASS |
| Submit recipe without ingredients/method for publication | Remove ingredient and method formsets from recipe form, submit form with all other required inputs and 'Make public' checkbox checked | Successful form submission, publish_request model instance set to 'False', approval_status model instance set to 'unpublished', recipe added to database and message displayed to user informing them that the recipe has been saved but requires ingredients and method for publication | PASS |
| Create recipe cancel button | Click cancel button on create recipe form | User returned to 'browse' page, recipe form not submitted | PASS |
| Edit recipe form field population | Click 'edit' button in recipe written by user logged in. | Recipe form loads with the fields populated with the data from the recipe being edited. | PASS |
| Edit recipes and submit for publication | Click 'edit' button in recipe written by user logged in, change data in the fields, and submit form with 'make public' checkbox checked | Successful form submission, publish_request model instance set to 'True', approval_status model instance set to 'pending approval' and recipe object edited in database. User redirected to 'my recipes' page and message informs user the recipe was successfully submitted and awaiting approval. | PASS |
| Edit recipe, remove publication request | Click 'edit' button in recipe written by user logged in and submit form with 'make public' checkbox unchecked | Successful form submission, publish_request model instance set to 'False', approval_status model instance set to 'unpublished' and recipe object edited in database. User redirected to 'my recipes' page and message informs user the recipe was saved. | PASS |
| Edit recipe, without ingredients/method for publication | Remove ingredient and method formsets from recipe form, submit form with all other required inputs and 'Make public' checkbox checked | Successful form submission, publish_request model instance set to 'False', approval_status model instance set to 'unpublished', recipe added to database and message displayed to user informing them that the recipe has been saved but requires ingredients and method for publication | PASS |
| Edit recipe cancel button | Click cancel button on create recipe form | User returned to 'my recipes' page, recipe form not submitted | PASS |
| Delete recipe button | Click 'delete' button in recipe written by user logged in | User is directed to confirm delete page. | PASS |
| Confirm delete | Click 'delete' button in recipe written by user logged in, click 'confirm' button on confirm delete page. | Recipe object is successfully removed from database, the user is redirected to the 'My Recipes' page and a message in displayed confirming successful deletion. | PASS |
| Cancel delete | Click 'delete' button in recipe written by user logged in, click 'cancel' button on confirm delete page. | User is returned to full recipe details page and recipe object is not deleted from database. | PASS |
| Save recipe | As logged in user click save button on full recipe details page of another users recipe. | Saves object is created in database and save button is updated to show recipe saved. | PASS |
| Unsave recipe | As logged in user click save button on full recipe details page of a previously saved recipe. | Saves object is removed in database and save button is updated to show recipe saved. | PASS |
| Like recipe | As logged in user click like button on full recipe details page of another users recipe. | Like object is created in database, like button is updated to show recipe liked and total number of likes is updated. | PASS |
| Unlike recipe | As logged in user click like button on full recipe details page of a previously liked recipe. | Like object is removed in database, like button is updated to show recipe liked and and total number of likes is updated. | PASS |
| Tags | View full recipe details with tags and click tag buttons. | Recipe tags displayed under recipe and direct user to list of recipe that have the clicked tag. | PASS |
| Comment form logged in | View full recipe details as authenticated user. | Comment form is displayed under the recipe. | PASS |
| Comment form not logged in | View full recipe details as anonymous user. | Comment form is not displayed. | PASS |
| Submit comment | View full recipe details as authenticated user and submit a comment. | Comment form successfully submitted and message informing user comment is awaiting approval is displayed. Comment object created in database. | PASS |
| View comments | View full recipe details of recipe with comments. | Comments are displayed in the order they were created. | PASS |
| User sign up | Submit sign up form with required input. | User object created in database. | PASS |
| User login | Login in as registered user. | User is logged in. | PASS |
| User log out | Log out authenticated user. | User is logged out. | PASS |
| Admin login | Log in to admin panel with superuser details. | Login successful, user panel accessed. | PASS |
| Recipe management list | View recipe management page in admin panel. | Recipe model fields displayed in list include title, publish_request, approval_status, created_on and author. | PASS |
| Recipe management approve action | Click checkbox for multiple recipes pending approval, select 'approve recipe' from action dropdown and click go. | All checked recipes approval status set to 'approved'. | PASS |
| Recipe management filter | Click options in filter menu on recipe management page in admin panel. | Recipe can be filtered by approval status choices. | PASS |
| Recipe management search | Enter search terms in search bar and click search. | Recipes can be searched by keywords in title and description | PASS |
| Comment management list | View comment management page in admin panel. | Comment model fields displayed in list include body, recipe, created_on and approved. | PASS |
| Comment management filter | Click options in filter menu on comment management page in admin panel. | Comments can be filtered by approved, recipe and created_on. | PASS |
| Comment management approve action | Click checkbox for multiple comments pending approval, select 'approve comments' from action dropdown and click go. | All checked comments approved. | PASS |
| Comment management search | Enter search terms in search bar and click search. | Comments can be searched by keywords in name and body. | PASS |
| Saves management list | View saves management page in admin panel. | Saves model fields displayed in list include recipe, user and saved_on. | PASS |
| Saves management filter | Click options in filter menu on saves management page in admin panel. | Saves can be filtered by recipe, user and saved_on. | PASS |
| Social media links | Click all social media links in the footer. | Appropriate social media platform websites will open in a new tab. | PASS |
| Alert auto dismissal | Create or edit a recipe and view message displayed on page after redirected. | Message displayed is automatically removed after a few seconds. | PASS |
