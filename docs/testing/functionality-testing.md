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
| Create recipe required fields | Click submit button on create recipe form before entering a value for each field | Empty fields for title, cooking time, serves, ingredients and method raise validation error and form cannot be submitted | PASS |
| Social media links | Click all social media links in the footer. | Appropriate social media platform websites will open in a new tab. | PASS |
