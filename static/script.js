var count = 0;
var countMeasurement = 0;
var allSteps = [];
var full_recipe = "";
var measurement_recipe = "";
var all_measurement = [];
var full_details = "";

function instructions() 
{
    var step = document.getElementById("step").value;
    this.value = '';
    count++;
    
    var thePhrase = "Step "+ parseInt(count,10) + ":" + step;

    var container = document.getElementById('all_steps');

    var newParagraph = document.createElement('p');
    
    newParagraph.textContent = thePhrase;

    container.appendChild(newParagraph);

    allSteps.push(thePhrase);
}

function makeRecipe() 
{
    var the_step = "";

    if(full_recipe == "")
    {
        full_recipe = allSteps[count-1];
    }
    else
    {
        the_step = allSteps[count-1];
        full_recipe = full_recipe + "\n" + the_step;
    }
}

function handleRecipeFunction() 
{
    instructions();
    makeRecipe();
}

function makeTheingredientsList() 
{
    var quantity = document.getElementById("quantity").value;
    var measurement = document.getElementById("measurement").value;
    var ingredient = document.getElementById("ingredient").value;
    
    measurement_recipe = quantity + " - " + measurement + " - " + ingredient;

    countMeasurement++;

    all_measurement.push(measurement_recipe);

    var ingredient_container = document.getElementById("ingredients_measure_list");

    var newParagraph = document.createElement('p');

    newParagraph.textContent = measurement_recipe;

    ingredient_container.appendChild(newParagraph);
}

function makeMeasurementList() 
{
    var the_step = "";

    if(full_details == "")
    {
        full_details = all_measurement[countMeasurement-1];
    }
    else
    {
        the_step = all_measurement[countMeasurement-1];
        full_details = full_details + "\n" + the_step;
    }
}

function handleMeasurementFunction() 
{
    makeTheingredientsList();
    makeMeasurementList();
}

function submitData() 
{ 
    const nameOfTheRecipe = document.getElementById('nameOfTheRecipe').value; 
    const country = document.getElementById('country').value;
    const teacher = document.getElementById('teacher').value;
    const ingredient = measurement_recipe;
    const recipe = full_recipe;
    

    const data = {
        nameOfTheRecipe: nameOfTheRecipe,
        country: country,
        teacher: teacher,
        ingredient: ingredient,
        recipe: recipe
    };

    fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => {
            // Check if the response is OK (status 200-299)
            if (response.ok) {
                return response.json(); // Parse JSON if the response is OK
            }
            // Handle error responses
            return response.json().then(err => {
                throw new Error(err.message || 'Unknown error occurred');
            });
        })
    .then(data => {
            console.log('Success:', data);
            alert('Data submitted successfully!');
        })
    .catch(error => {
            console.error('Error:', error.message);
            alert(`An error occurred: ${error.message}`);
        });
}